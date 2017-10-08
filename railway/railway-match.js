var linematch = require('./linematch');
var fs = require('fs');


// read input geojson
var json = fs.readFileSync(process.argv[2]);
var geojson = JSON.parse(json);


var railways = filter(geojson);
var matched = match(railways.lines);

writeGeojson(geojson.crs, matched, railways.props);



function filter(geojson){
    var railway = {};
    var railway_prop = {};

    var jrlist = readJRList();

    for (i in geojson.features){
        var feature = geojson.features[i];
        var name = geojson.features[i].properties.NAME;

        if (!name) continue;

        if (name.match("旅客鉄道")){
            name = name.replace(/.*旅客鉄道/, "JR");
        }

        // normalize
        name = name.split(/ |;|-/)[0];

        if (name.match("新幹線") || name.match("JR") || jrlist[name]){
            //console.log(name);
            if (!railway[name]){
                railway[name] = [];
                railway_prop[name] = feature.properties;
            }
            railway[name].push([feature.geometry.coordinates]);
        }
    }
    console.log(Object.keys(railway).length);

    return { lines: railway, props: railway_prop };
}


function match(railway){
    var matched = {};

    // for each railway lines
    for (name in railway){
        matched[name] = [];
        var lines = railway[name];

        // sort with length
        lines.sort(function(a, b){ return b[0].length - a[0].length });

        // for each line segments
        // pre-merged with names (ST_LineMerge)
        for (l in lines){
            var line = lines[l];
            if (l == 0){
                matched[name] = line;
                continue;
            }

            // linematch
            // https://github.com/mapbox/linematch
            // linematch will return a new array 
            // that contains all segments in a that are not matched with segments in b
            //var result = linematch(line, matched[name], 0.01);
            var result = linematch(line, matched[name], 20);
            //var result = linematch(line, matched[name], 100); // web mercator (m)

            if (result.length) matched[name].push(result[0]);
        }

        console.log(name, matched[name].length);
    }
    return matched;
}

function writeGeojson(crs, matched, props){
    var data = {
        type: "FeatureCollection",
        src: crs,
        features: []
    };

    for (name in matched){
        var line = matched[name];
        for (m in line){
            data.features.push({
                type: "Feature",
                geometry: {
                    type: "LineString",
                    coordinates: line[m]
                },
                properties: props[name]
            });
        }
    }

    fs.writeFile('railway-match.geojson', JSON.stringify(data));
}

function readJRList(){
    var csv = fs.readFileSync('jr.csv', 'utf-8');
    var data = csv.split('\r\n');
    
    var list = {};
    for (i in data){
        var d = data[i].substr(2);
        list[d] = true;
    }

    return list;
}



