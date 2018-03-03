
var AABB = function(data){
    this.id = 'AABB';
    this.target = {'click': null, 'hover': null};
    //console.log("imagelayer Meta", data);
    this.current_doc = _samtla.settings['docID'];
    this.currentdoc_obj = null; 
    this.getBoundingBox(data);
    //console.log("AAABBBB", data)
    //window._samtla.imgwidget.ScrollInToView(window._samtla.imgwidget, this.currentdoc_obj);
    return this//.currentdoc_obj;
};

AABB.prototype.getBoundingBox = function(data){
    //console.log("getBoundingbox", data)        
    var ID = data['ID'], // newspaper id
        bounding_boxes = data['AABB'], // article bounding boxes
        clip,
        coords,
        img_coord,
        temp = [];

    for (var docID in bounding_boxes){
        if (temp == undefined){   
            temp = [];
        }
        for (var i=0; i < bounding_boxes[docID].length; i++){
            var clip = bounding_boxes[docID][i];
            coords = clip.split(',');
            ///console.log("COORDS", coords) 
            if (coords != ""){
                img_coord = getHW(coords);
                img_coord['docID'] = docID;
               // console.log(img_coord)
                if (docID == data['docID']){
                    img_coord.current_doc = true;
                    this.current_doc = img_coord.docID; 
                    game.document.imgwidget.current_doc = img_coord;
                    this.currentdoc_obj = img_coord;
                    temp.push(img_coord);
                } else {
                    temp.push(img_coord);
                    img_coord.current_doc = false;
                    //img_coord.current_doc = true;
                }
            }
        }
    }
    this.data = temp;
};

AABB.prototype.setClickTarget = function(controller, col, mouse){
    if(col.type == 'AABB'){
        this.target.click = col.docID;
        this.current_doc = col.docID;
        //game.document.docID = col.docID;
        //game.metadata.docID = col.docID;
        //if (controller.state._current == controller.state.NEWSPAPER){
        controller.updateRequired = true;
        controller.current_doc = col.docID; 

        getDocument(col.docID, '#doc', false);
        controller.ScrollInToView(controller, col, mouse);

       // game.events.trigger("view_document",col.docID,false)
    } 
};

AABB.prototype.setHoverTarget = function(controller, col, mouse){
    //console.log("hover article", col, controller.viewport);
    if (col){
        this.target.hover = col.docID;
        controller.updateRequired = true;
        //console.log("mouse coords", mouse)
        //var offsetX = parseInt($('#' + controller.container_element).offset().left);
        //var offsetY = parseInt($("#img-layer").scrollTop())// + parseInt($("#img-layer").offset().top);
        //$("#img-layer").attr('title', mouse.x - offsetX + ":" + ((mouse.y-parseInt($("#img-layer").offset().top))))//tooltip({
        
       // game.document.imgwidget.camera.Anchor({
       //     x: col.x, 
        //    y: (col.y + (col.h * 0.5)), 
        //});

        $("#" + self.container_element).tooltip({
            content: col.docID,
            position: { my: "left+15 center", at: "left center" }
        });
//        controller.metadata.docID = col.docID;

        //if (controller.state._current == controller.state.NEWSPAPER){
        //    game.events.trigger("show_metadata", col.docID); 
        //} 
    } else {
       // window._samtla.imgwidget.draw(); 

    }

};

AABB.prototype.draw = function(controller, xScroll, yScroll){
//    console.log(controller.context, controller.state);
    if (controller){
        var context = controller.dblbuffer_context;
        var strokecolor = null;
        context.lineWidth = 10+0.5// controller.zoom);
            for (var d in this.data){
                var color = null;
                var clip = this.data[d];
               // console.log(clip.docID, this.target.hover, clip.docID == this.target.hover)
                if (clip.docID == this.target.hover && clip.docID != this.current_doc){
                    strokecolor = "rgba(255,255,0,1)";//"rgba(155,255,255,0.4)";
                    context.strokeStyle = strokecolor;
                    context.strokeRect(
                        Math.round(clip.x), 
                        Math.round(clip.y), 
                        Math.round(clip.w), 
                        Math.round(clip.h)
                    );
//                    color = "rgba(255,255,255,0.1)";
//                    context.fillStyle = color;
//                    context.fillRect(
//                        Math.round(clip.x), 
//                        Math.round(clip.y), 
//                        Math.round(clip.w), 
//                        Math.round(clip.h)
//                    );

                }

 
//                if (controller.zoom < 0.70){
                if (this.target.click == clip.docID || this.current_doc == clip.docID){
                    color = "rgba(0,255,0,1)";
                    context.strokeStyle = color;
                    context.strokeRect(
                    Math.round(clip.x), 
                    Math.round(clip.y), 
                    Math.round(clip.w), 
                    Math.round(clip.h)
                    );
                }
//                }
            }
        } 
  //  }
};

