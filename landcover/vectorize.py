import fiona, json, rasterio, click
from rasterio import features, Affine
from shapely.geometry import Polygon, MultiPolygon, mapping
from fiona.crs import from_epsg
import numpy as np
from scipy.ndimage import zoom
from scipy.ndimage.filters import median_filter, maximum_filter
from makesurface.scripts import tools


def classifyMappingValue(inArr, mapping):
    outRas = np.zeros(inArr.shape)
    for key, value in mapping.items():
        outRas[np.where(inArr == key)] = value
    outRas[np.where(inArr.mask == True)] = 0
    return outRas.astype(np.uint8)


def vectorizeRaster(infile, outfile=None, nosimple=False):
    weight = 1.0
    smoothing = 1
    setNoData = 255
    band = 1

    with rasterio.drivers():
        with rasterio.open(infile, 'r') as src:
            inarr = src.read(band)
            oshape = src.shape
            oaff = src.affine

            if (type(setNoData) == int or type(setNoData) == float) and hasattr(inarr, 'mask'):
                inarr[np.where(inarr.mask == True)] = setNoData
                nodata = True

            simplest = ((src.bounds.top - src.bounds.bottom) / float(src.shape[0]))

            # nodata
            maskArr = np.zeros(inarr.shape, dtype=np.bool)
            maskArr[np.where(inarr == setNoData)] = True
            inarr = np.ma.array(inarr, mask=maskArr)
            del maskArr

    # mapbox-terrain-v2 levels
    # https://www.mapbox.com/vector-tiles/mapbox-terrain/#landcover
    # 0 background
    # 1 crop
    # 2 grass
    # 3 scrub
    # 4 wood
    mappingvalue = {
        10: 1,
        20: 1,
        50: 4,
        60: 3,
        160: 2
    }
    classes = ["", "crop", "grass", "scrub", "wood"]
    breaks= [0, 1, 2, 3, 4]
    classRas = classifyMappingValue(inarr, mappingvalue)
    print classRas

    #print classRas, breaks
    print 'nosimple:', nosimple, simplest

    # filtering for speckling
    classRas = median_filter(classRas, size=2)


    outputHandler = tools.dataOutput(True)

    for i in breaks:
        if i == 0:
            continue

        else:
            cl = classes[i]
            tRas = (classRas >= i).astype(np.uint8)
 
        print i, cl #, tRas

        for feature, shapes in features.shapes(np.asarray(tRas,order='C'),transform=oaff):
            if shapes == 1:
                featurelist = []
                for c, f in enumerate(feature['coordinates']):
                    if len(f) > 5 or c == 0:
                        if nosimple:
                            poly = Polygon(f)
                        else:
                            poly = Polygon(f).simplify(simplest / float(smoothing), preserve_topology=True)
                        featurelist.append(poly)

                if len(featurelist) != 0:
                    oPoly = MultiPolygon(featurelist)
                    outputHandler.out({
                        'type': 'Feature',
                        'geometry': mapping(oPoly),
                        'properties': {
                            'class': cl
                        }
                    })
    if outfile:
        with open(outfile, 'w') as ofile:
            ofile.write(json.dumps({
                "type": "FeatureCollection",
                "features": outputHandler.data
            }))

    else:
        # retrun geojson
        return outputHandler.data


if __name__ == '__main__':
    import sys
    vectorizeRaster(sys.argv[1], sys.argv[2])

