function initGUI(){
    var gui = new dat.GUI();

    var b1 = gui.addColor(styledef, 'background');
    b1.onChange(function(){
        style.layers[0].paint['background-color'] = styledef.background;
        gl._glMap.setStyle(style);
    });

    var b2 = gui.addColor(styledef, 'water');
    b2.onChange(function(){
        style.layers[17].paint['fill-color'] = styledef.water;
        style.layers[15].paint['line-color'] = styledef.water;
        style.layers[16].paint['line-color'] = styledef.water;
        gl._glMap.setStyle(style);

    });
    
    var b3 = gui.addColor(styledef, 'landcover');
    b3.onChange(function(){
        style.layers[1].paint['fill-color'] = styledef.landcover;
        style.layers[2].paint['fill-color'] = styledef.landcover;
        style.layers[3].paint['fill-color'] = styledef.landcover;
        style.layers[4].paint['fill-color'] = styledef.landcover;
        style.layers[6].paint['fill-color'] = styledef.landcover;
        gl._glMap.setStyle(style);
    });
    
    var b4 = gui.add(styledef, 'hillshade', 0, 1);
    b4.onChange(function(){
        style.layers[14].paint['hillshade-exaggeration'] = styledef.hillshade;
        gl._glMap.setStyle(style);
    });
    
    var b5 = gui.addColor(styledef, 'park');
    b5.onChange(function(){
        style.layers[7].paint['fill-color'] = styledef.park;
        style.layers[8].paint['fill-color'] = styledef.park;
        gl._glMap.setStyle(style);
    });
    
    var b6 = gui.addColor(styledef, 'highway');
    b6.onChange(function(){
        style.layers[40].paint['line-color'] = styledef.highway; // case
        style.layers[41].paint['line-color'] = styledef.highway; // case
        style.layers[42].paint['line-color'] = styledef.highway;
        style.layers[43].paint['line-color'] = styledef.highway;
        style.layers[49].paint['line-color'] = styledef.highway; // bridge case
        style.layers[50].paint['line-color'] = styledef.highway; // case
        style.layers[51].paint['line-color'] = styledef.highway;
        style.layers[52].paint['line-color'] = styledef.highway;
        gl._glMap.setStyle(style);
    });

    var b7 = gui.addColor(styledef, 'national-road');
    b7.onChange(function(){
        style.layers[36].paint['line-color'] = styledef['national-road']; // case
        style.layers[37].paint['line-color'] = styledef['national-road']; // case
        style.layers[38].paint['line-color'] = styledef['national-road'];
        style.layers[39].paint['line-color'] = styledef['national-road'];
        style.layers[44].paint['line-color'] = styledef['national-road'];
        style.layers[45].paint['line-color'] = styledef['national-road'];
        style.layers[46].paint['line-color'] = styledef['national-road'];
        style.layers[48].paint['line-color'] = styledef['national-road'];
        gl._glMap.setStyle(style);
    });
    
    var b8 = gui.addColor(styledef, 'city-label');
    b8.onChange(function(){
        style.layers[77].paint['text-color'] = styledef['city-label'];
        gl._glMap.setStyle(style);
    });

    return gui;
}



