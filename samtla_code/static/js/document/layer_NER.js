
var NERLayer = function(pixel_data){
    this.id = 'NER';
    this.highlight = {
        'people': "rgba(255,0,0,0.4)",
        'country': "rgba(0,255,0,0.4)",
        'city': "rgba(0,255,0,0.4)",
        'occupation': "rgba(0,100,255,0.4)",
        'commodity': "rgba(250,200,0,0.4)",
        'diseases': "rgba(250,200,0,0.4)",

    }
    var AABB = null,
        type,
        cat,
        NE,
        indices,
        idx;
    this.pixel_data = pixel_data['pixel_idx'];

    this.data = {};
    this.target = {'click': null, 'hover': null};
    this.processPixelData();
    return this;
};

NERLayer.prototype.processPixelData = function(){
    //console.log("Process pixeldata", this.pixel_data)//, this.pixel_data[type], this.pixel_data[type][NER])
    var indices = null;
    this.data = [];
    for (var type in this.pixel_data){
        for (var NE in this.pixel_data[type]){ 
            this.data = this.getIndices(type, NE);    
        }
    }
    //controller.updateRequired = true;
};

NERLayer.prototype.getIndices = function(type, NE){
    //var temp = [];
    var color = this.highlight[type];
    var indices = this.pixel_data[type][NE];
   // console.log("getindices", type, NE, indices, color)
    for (var i=0; i < indices.length; i++){
        var box = indices[i];
        if (box!=undefined && box.length > 0){  
            idx = box.split(',');
            var pos = {
                    x: parseInt(idx[0]),
                    y: parseInt(idx[1]),
                    w: (parseInt(idx[2]) - parseInt(idx[0])),
                    h: (parseInt(idx[3]) - parseInt(idx[1])),
                    color: color,
                    NERtype: type,
                    NER: NE 
                }
      

//            pos = {
//                x: parseInt(idx[0]),
//                y: parseInt(idx[1]), 
//                w: parseInt(idx[2]), 
//                h: parseInt(idx[3]),
//                color: color, 
//            }
//            console.log(indices, box, pos);
            this.data.push(pos);
        } else {
            continue;
        }
    }
//    controller.updateRequired = true;
    return this.data;
};

NERLayer.prototype.setClickTarget = function(controller, col, event){
    if(col && col.type == 'NER'){
        var query = col.NER;
      //  console.log("submitting query") 
        getSearch();
//        controller.updateRequired = true;
    }
};

NERLayer.prototype.setHoverTarget = function(controller, col, event){
    if (col){
       // console.log("setting target NER", col);
        var lat, long = window._samtla.data['KML'][col.NER].split(':')
        //game.googlemap.drawAll(game.NER.response, undefined);
        getGoogleMap(col.NER, lat+":"+long, col.NER);
        $("#"+controller.container_element).attr('title', col.NER.charAt(0).toUpperCase() + col.NER.slice(1, col.NER.length) + " (" + col.NERtype + ")")//tooltip({
        controller.updateRequired = true;
    }
};

NERLayer.prototype.draw = function(controller){
    if(controller.dblbuffer_context && this.data.length > 0 && controller.updateRequired == true){
        var context = controller.dblbuffer_context;
     //   console.log("drawing NER layer", this.data)
        var scale = controller.getScale(controller.canvas, controller.dblbuffer);
        for (var i=0; i < this.data.length; i++){
            var NE = this.data[i],
                x = NE.x,// * scale, 
                y = NE.y,// * scale, 
                w = NE.w,// * scale) - (NE.x * scale), 
                h = NE.h;// * scale;
            context.fillStyle = NE.color;
            context.fillRect(
                x,
                y,
                w,
                h
            );
        }
    }  
};

