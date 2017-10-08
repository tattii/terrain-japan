var linematch = require('./linematch');
var fs = require('fs');

var json = fs.readFileSync("railway/all2/railway.geojson");
var geojson = JSON.parse(json);

var railway = {};
var railway_prop = {};
for (i in geojson.features){
	var feature = geojson.features[i];
	var name = geojson.features[i].properties.NAME;

	if (!name) continue;

	if (name.match("旅客鉄道")){
		name = name.replace(/.*旅客鉄道/, "JR");
	}

	if (name.match("新幹線") || name.match("JR")){
		//console.log(name);
		if (!railway[name]){
			railway[name] = [];
			railway_prop[name] = feature.properties;
		}
		railway[name].push([feature.geometry.coordinates]);
	}
}

console.log(railway.length);

var matched = {};
for (name in railway){
	matched[name] = [];
	var lines = railway[name];

	// sort with length
	lines.sort(function(a, b){ return b[0].length - a[0].length });

	for (l in lines){
		if (l == 0){
			matched[name] = lines[0];
			continue;
		}
		var line = lines[l];

		// linematch
		// https://github.com/mapbox/linematch
		//var result = linematch(line, matched, 0.0001);
		//var result = linematch(line, matched[name], 20);
		var result = linematch(line, matched[name], 100);

		if (result.length) matched[name].push(result[0]);
	}
	console.log(name, matched[name].length);
}


var data = {
	type: "FeatureCollection",
	src: geojson.crs,
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
			properties: railway_prop[name]
		});
	}
}

fs.writeFile('railway/railway-match.json', JSON.stringify(data));


