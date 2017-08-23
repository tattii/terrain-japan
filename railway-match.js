var linematch = require('./linematch');
var fs = require('fs');

var json = fs.readFileSync("railway2/railway.geojson");
var geojson = JSON.parse(json);

var railway = {};
for (i in geojson.features){
	var feature = geojson.features[i];
	var name = geojson.features[i].properties.NAME;

	if (name.match("新幹線") || name.match("JR")){
		//console.log(name);
		if (!railway[name]) railway[name] = [];
		railway[name].push([feature.geometry.coordinates]);
	}
}


var matched = {};
for (name in railway){
	matched[name] = [];
	var lines = railway[name];
	for (l in lines){
		if (l == 0){
			matched[name] = lines[0];
			continue;
		}
		var line = lines[l];

		// linematch
		// https://github.com/mapbox/linematch
		//var result = linematch(line, matched, 0.0001);
		var result = linematch(line, matched[name], 20);

		if (result.length) matched[name].push(result[0]);
	}
	console.log(name, matched[name].length);
}


var data = {
	type: "FeatureCollection",
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
			}
		});
	}
}

fs.writeFile('railway-match.json', JSON.stringify(data));


