install:
	npm install turf-polygon-to-line
	git clone https://github.com/stepankuzmin/turf-polygon-to-line

toline:
	mkdir -p line
	find data/pref -name "*.geojson" -exec ./toline.sh {} \;

vtile:
	tippecanoe -o pref.mbtiles -l pref -z 12 line/*.geojson
