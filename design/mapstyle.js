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
    
    var b4 = gui.addColor(styledef, 'park');
    b4.onChange(function(){
        style.layers[7].paint['fill-color'] = styledef.park;
        style.layers[8].paint['fill-color'] = styledef.park;
        gl._glMap.setStyle(style);
    });

    return gui;
}



