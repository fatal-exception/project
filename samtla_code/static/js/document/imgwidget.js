var mousePosition,
    default_zoom = 0.20,
    offset = [0,0],
    div,
    isDown = false,
    VIEW_TYPE = 1,
    controller;

var getHW = function(pos){
    var x1 = parseInt(pos[0]),
        y1 = parseInt(pos[1]),    
        x2 = parseInt(pos[2]),
        y2 = parseInt(pos[3]),
        w = x2 - x1,
        h = y2 - y1;
    return {x: x1, y: y1, w: w, h: h};
};


var curYPos, curXPos, curDown;
var ImageWidget = function(parent_element){
    this.dblbuffer = null;
    this.canvas = null;
    this.canvas_id = null;
    this.parent_element = parent_element;
    this.canvas_element = 'img-canvas';
    this.page = {};
    this.state = {
        _current: 0,
        NEWSPAPER: 0,
        ARTICLE: 1
    }   
    this.imageObj = new Image();
    this.imageObj.src = null;
    this.layers = new Layers();
    this.onHover_docID = null;
    this.current_doc = {x:0,y:0,w:1, h:1};
    this.scale = {x: 0, y: 0};
    this.zoom = default_zoom;
    this.viewport = {};
    this.border_size = 5;
    this.camera = null;
    this.updateRequired = true;
};

ImageWidget.prototype.Init = function(data, docID){
    //$('#doc').hide();
    data = data.document;
    this.xLast = 0;  // last x location on the screen
    this.yLast = 0;  // last y location on the screen
    this.xImage = 0; // last x location on the image
    this.yImage = 0; // last y location on the image
    var self = this;
    $('#' + this.parent_element).html('<div id="' + this.parent_element + '"></div>');
    this.createCanvas(this.canvas_element);
    this.layers = new Layers();
    this.crop_areas = this.getCropAreas(data.area);    
    this.setUpCanvas(this.crop_areas);
    this.setCanvasDimensions('result');



    this.scale = this.getScale(this.canvas, this.dblbuffer);
    this.camera = new Camera(this.canvas);
    this.camera.boundary.x = Math.round(parseInt($('#' + this.parent_element).width()) * 0.95),
    this.camera.boundary.y = Math.round(parseInt($('#' + this.parent_element).height()) * 0.70);

    this.viewport = {x: 0, y: 0, w: this.canvas.width, h: this.canvas.height};
    //console.log("create canvas", data, this.canvas, this.canvas_element, '#' + this.parent_element, this.camera, this.viewport);
    var imagefile = null;
    if (data.image){
        imagefile = data.image[0];
    }
    this.loadImage({
        src: 'static/'+imagefile,
        callback: function(){
            //$('#' + this.parent_element).show();
            self.setCanvasDimensions(this.parent_element);
            //console.log("loading image", imagefile);
            self.open();  
            self.setZoom(self.zoom);
            self.setView();
          //  console.log("everything ready for canvas", self)
            self.updateRequired = true;
            $('#'+this.parent_element).fadeIn('fast');
            $('#img-layer').fadeIn('fast');
            $('#doc').fadeOut('fast');
//            self.ScrollInToView(self, self.current_doc);
        },
   
    });
    var col = this.loadLayer('AABB', data, AABB);
    this.setUpEvents();
//    self.ScrollInToView(self, self.current_doc);
};



ImageWidget.prototype.setView = function(id){
    this.state._current = this.state.NEWSPAPER;
    var crop_area = {x: 0, y: 0, w: this.imageObj.width, h: this.imageObj.height};
    this.setViewport(crop_area); 
    this.setZoom(default_zoom);
};

ImageWidget.prototype.ZoomIn = function(value){
    var self = window._samtla.imgwidget;
    self.zoom += 0.05; 
    self.setZoom(self.zoom);
};

ImageWidget.prototype.ZoomOut = function(value){
    var self = window._samtla.imgwidget;
    self.zoom -= 0.05 
    self.setZoom(self.zoom);
};

ImageWidget.prototype.setZoom = function(value){
    var self = window._samtla.imgwidget;
  //  self.canvas.width = self.dblbuffer.width;
    //self.canvas.height = self.dblbuffer.height;
    var scaleX = self.canvas.width * self.zoom;
    var scaleY = self.canvas.height * self.zoom;
    var w = parseInt($(self.parent_element).width());
    if (scaleX >= w){
        //$('#' + self.canvas_element).css('width', scaleX + 'px');
        //$('#' + self.canvas_element).css('height', scaleY + 'px');
        $('#zoom').html(parseInt(self.zoom * 100)+'%');
    } else { 
        //$('#' + self.canvas_element).css('width', w + 'px');
    }
    self.updateRequired = true;

    self.update();
    self.draw();

    self.ScrollInToView(self, self.current_doc);
//    self.ScrollInToView(self, self.currentdoc_obj);
};

ImageWidget.prototype.ScrollInToView = function(controller, obj, mouse){
    var element = '#' + this.parent_element;

    var x = (obj.y * controller.zoom) - ((parseInt($('#'+controller.parent_element).height()) * 0.7) * controller.zoom);
    var y = (obj.x * controller.zoom) - ((parseInt($('#'+controller.parent_element).width()) * 0.5) * controller.zoom)
    if (obj && obj.x != undefined){  
        $(element).animate({
            scrollTop: y,
            scrollLeft: x
        }, 'fast');
        //console.log("scroll in to view", obj.x, obj.y, obj.x*controller.zoom, obj.y*controller.zoom);
//        window.scrollTo(x, y);
    }
    this.prev_offset = offset;
};


ImageWidget.prototype.setUpEvents = function(){
    var self = this;
    this.canvas.addEventListener('click', function(event){
        var cols = self.checkCollisions(event);
        for (var c in cols){
            var col = cols[c]; 
          //  console.log("Mouse click", col);
            var mouse = getMouseXY(event, document.getElementById('img-canvas'))
            self.layers.objects[col.type].setClickTarget(self, col, mouse);
        }
    });

    this.canvas.addEventListener('mousedown', function(event){
        curYPos = event.pageY; 
        curXPos = event.pageX; 
        curDown = true; 
    });

    this.canvas.addEventListener('mouseup', function(event){
        curDown = false; 
    });    

    this.canvas.addEventListener('mousemove', function(event){

        var cols = self.checkCollisions(event);
        var mouse = getMouseXY(event, document.getElementById('img-canvas'))
        var element = document.getElementById(self.parent_element);
        curXPos = event.pageX; 
        curYPos = event.pageY; 

        for (var c in cols){ 
            var col = cols[c]; 
            self.current_doc = col;
            self.layers.objects[col.type].setHoverTarget(self, col, mouse);
//            console.log(mouse, document.getElementById('img-layer').scrollLeft + (curXPos - event.pageX), document.getElementById('img-layer').scrollLeft, curXPos, event.pageX)
            if(curDown){
                var x = element.scrollLeft + (curXPos - event.pageX);  
                var y = element.scrollTop + (curYPos - event.pageY);
                //window.scrollTo(x, y);
            }
        }
    });
};

ImageWidget.prototype.getCropAreas = function(crop_data){
    var temp = [];
    for(var i in crop_data){
        var dims = getHW(crop_data[i].split(','));
        temp.push(dims);
    }

    return temp;
};

ImageWidget.prototype.createCanvas = function(canvas_id){
    this.canvas_id = canvas_id;
    // create main window
    this.canvas = document.getElementById(canvas_id);
    if (this.canvas == undefined || this.canvas == null){
        $('#' + this.parent_element).html('<canvas id="' + canvas_id + '"></canvas>');
    }

    this.canvas = document.getElementById(canvas_id);

    // create backing canvas
    this.dblbuffer = document.getElementById('dblbuffer');
    if (this.dblbuffer == undefined){
        this.dblbuffer = document.createElement('canvas');
        this.dblbuffer.id = 'dblbuffer';
        $('#dblbuffer').hide();
    }
  //  console.log("backcanvas", this.dblbuffer, '#'+this.parent_element)
    return this.dblbuffer;
};

ImageWidget.prototype.setCanvasDimensions = function(parent_element){
    
    var w = Math.round(parseInt($('#' + this.parent_element).width()) * 0.97),//w = Math.round(parseInt($('#' + parent_element).width())*0.95),
        h = Math.round(parseInt($('#' + this.parent_element).height()) * 0.97);
    //$('#' + this.parent_element).css('width', w + 'px');
    //$('#' + this.parent_element).css('height', h + 'px');//'75%');
    $('#' + this.parent_element).css('overflow', 'auto');
    if (this.canvas == undefined){
        this.createCanvas(this.canvas_element);
    }
    $('#' + this.parent_element).css('display', 'block');
    $('#' + this.canvas_element).css('display', 'block');
    this.setZoom(default_zoom);
    this.update_required = true;
};

ImageWidget.prototype.getPageDimensions = function(crop_areas){
    var w,
        h,
        temp = null,
        minX = null,
        minY = null,
        maxW = null,
        maxH = null,
        prev_sect = null,
        section;
        if (crop_areas==undefined){return}
        for (var i=0; i < crop_areas.length; i++){
            section = crop_areas[i];
            if (minX == null){
                minX = section.x; 
            } else 
            if (section.x < minX){
                minX = section.x;
            }
            if (minY == null){
                minY = section.y; 
            } else 
            if (section.y < minY){
                minY = section.y;
            }
            if (maxW == null){
                maxW = section.w; 
            } else 
            if (section.x + section.w > maxW) {
                maxW = (section.x + section.w);
            }
            if (maxH == null){
                maxH = section.h; 
            } else 
            if (section.y + section.h > maxH){
                maxH = (section.y + section.h);
            }
            prev_sect = section;
            //console.log("section", crop_areas, section, minX, minY, maxW, maxH)
        }
        this.page = {x: minX, y: minY, w: maxW, h: maxH};
        return this.page; 
};

ImageWidget.prototype.update = function(){
//    if(this.camera){
       // this.camera.update();
//    }
};

ImageWidget.prototype.setUpCanvas = function(crop_areas){
    var maxW, maxH = this.getPageDimensions(crop_areas);

    this.canvas.width = maxH.x//parseInt($('#' + this.parent_element).width());
    this.canvas.height =  maxH.y//parseInt($('#' + this.parent_element).height())//maxH;
    //console.log("MAXIMUM", maxW, maxH, this.imageObj.width, this.imageObj.height)
    this.context = this.canvas.getContext('2d');

    this.dblbuffer.width = maxH.x//this.imageObj.width;
    this.dblbuffer.height = maxH.y//this.imageObj.height;
    this.dblbuffer_context = this.dblbuffer.getContext('2d');

    this.context.font = "1.2em Arial";
    this.context.textAlign = 'center';

    this.context.strokeStyle = "green";

    //$('#result').css('overflow', 'hidden');

};

ImageWidget.prototype.setViewport = function(view){
    if (view != undefined){
        this.viewport = view;
        this.dblbuffer.width = this.viewport.w;
        this.dblbuffer.height = this.viewport.h;
    }
//    $('#result_window').css('overflow', 'auto');
};

ImageWidget.prototype.loadImage = function(obj){
    
    if(obj.src == undefined){
        $('#doc').fadeIn('fast');
        $('#zoom-tool').hide();
        $('#rawtext-view').hide();
        $('#doc-toolset').hide();
    } else {
        if(obj.src){//"/static/interface/" + obj.src != this.imageObj.src){ 
            this.imageObj.src = obj.src;    
            //console.log("Loading image", obj.src, this.imageObj) 
            this.imageObj.onload = obj.callback;
            this.imageObj.onerror = function(err){
                console.log("Problem loading image", obj.src, err) 
                //game.events.bind("show_rawtext", undefined);
                $('#doc').fadeIn('fast');
                $('#zoom-tool').hide();
                $('#rawtext-view').hide();
                $('#doc-toolset').hide();
                this.updateRequired = true;
                self.ScrollInToView(self, self.current_doc);

            };
        }
    }
};

ImageWidget.prototype.loadLayer = function(id, objs, callback){
    if (objs == undefined) {
        return;
    }
    //console.log("load layer", objs)
    var id = id,
        data = new callback(objs);
    this.layers.add(id, data);
    this.updateRequired = true;
//    console.log("Added layer", this.layers);
};


ImageWidget.prototype.draw = function(){
    this.resize();
  //  $('#' + this.parent_element).css('height', '100%');

    if (this.context && this.updateRequired == true){
  //      console.log("DRAW CANVAS!", this.imageObj) 
        //this.dblbuffer_context.clearRect(0,0,this.dblbuffer.width, this.dblbuffer.height); 
        //this.context.clearRect(0,0,this.canvas.width, this.canvas.height); 
        this.dblbuffer_context.drawImage(
            this.imageObj, 
            this.viewport.x, 
            this.viewport.y, 
            this.viewport.w, 
            this.viewport.h, 
            0, 
            0, 
            this.dblbuffer.width, 
            this.dblbuffer.height
        );
           
        this.drawLayer(this, this.viewport.x, this.viewport.y);

        this.context.drawImage(
            this.dblbuffer, 
            0, 
            0, 
            this.dblbuffer.width, 
            this.dblbuffer.height, 
            this.viewport.x,//-window._samtla.imgwidget.camera.xScroll, 
            this.viewport.y,//-window._samtla.imgwidget.camera.yScroll, 
            this.canvas.width, 
            this.canvas.height
        );

        this.updateRequired = false;
    } 
//    $('#img-layer').scrollTop(+=window._samtla.imgwidget.camera.yScroll);
};

ImageWidget.prototype.drawLayer = function(context){
    this.layers.draw(this);
};

ImageWidget.prototype.getScale = function(objA, objB){
    this.scale.x = objA.width/objB.width;
    this.scale.y = objA.height/objB.height;
    return this.scale;
};


ImageWidget.prototype.checkCollisions = function(event){
    var self = this;
    this.scale = this.getScale(this.canvas, this.dblbuffer);
    var rect = this.canvas.getBoundingClientRect();
    var temp = {};
    var coords = {
        x: Math.round(event.clientX - rect.left),
        y: Math.round(event.clientY - rect.top),
        width: 2,
        height: 2
    };
    var colx;
    var coly;
    var colw;
    var colh;
    var mouse = {x:coords.x, y: coords.y, width: 2, height: 2};
    this.mouse = mouse;
    //$("#img-layer").attr('title', mouse.x + ":" + mouse.y)//tooltip({

    for (var type in this.layers.objects){
        if(temp[type] == undefined){
            temp[type] = [];
        }  
        var collision_layer = this.layers.objects[type].data;
        //for (var docID in collision_layer){
            for (var i in collision_layer){
                var box = collision_layer[i];

                colx = box.x// this.zoom
                coly = box.y// * this.zoom
                colw = box.w// * this.zoom
                colh = box.h// * this.zoom
                mouse.x = coords.x / this.zoom
                mouse.y = coords.y / this.zoom

                mouse.width = 5
                mouse.height = 5
                var coll_boundary = { 
                    x: colx, 
                    y: coly,
                    width: colw,
                    height: colh,
                }
                var col = utils.intersects(coll_boundary, mouse, 1);
                //if (type != 'AABB'){
                    //console.log(type, coll_boundary.x, coll_boundary.y, mouse.x, mouse.y, col)
                //}
                //console.log(mouse)//, coords)
                if(col == true){
                    box.type = type;
                    temp[type].push(box);
                }
            }
        //}
    }
    if(temp['NER'] && temp['NER'].length > 0){
        return temp['NER'];
    } else {
        return temp['AABB'];
    }
   
};



ImageWidget.prototype.resize = function(){

//console.log(game.document.imgwidget.zoom)
    var self = window._samtla.imgwidget;
//    self.zoom = parseInt(slider.value)/100;
    self.canvas.width = self.dblbuffer.width;
    self.canvas.height = self.dblbuffer.height;
    var scaleX = self.canvas.width * self.zoom;
    var scaleY = self.canvas.height * self.zoom;
    var w = parseInt($('#' + self.parent_element).width());
//    console.log(scaleX, w, scaleX >= w);
    if (scaleX >= w){
        $('#' + self.canvas_element).css('width', scaleX + 'px');
        $('#' + self.canvas_element).css('height', scaleY + 'px');
        //$('#mouse_debug').html(slider.value + '%');
        document.getElementById('zoom').value = self.zoom * 100;
    } else { 
        $('#' + self.canvas_element).css('width', w + 'px');
    }
//    self.ScrollInToView(self, self.current_doc);
//    self.ScrollInToView(self, self.currentdoc_obj);
    return




    var canvas = document.getElementById(this.canvas_id);
    var widthToHeight = 3 / 4;
    var newWidth = parseInt($('#' + this.parent_element).width());
    var newHeight = parseInt($('#' + this.parent_element).height());
    var newWidthToHeight = newWidth / newHeight;
    if (canvas.width != newWidth){// && canvas.height != newHeight){
        if (newWidthToHeight > widthToHeight) {
            newWidth = newHeight * widthToHeight;
            canvas.style.height = newHeight + 'px';
            canvas.style.width = (newWidth) + 'px';
        } else {
            newHeight = newWidth / widthToHeight;
            canvas.style.width = newWidth + 'px';
            canvas.style.height = newHeight + 'px';
        }
        var canvas = document.getElementById(this.canvas_element);
        canvas.width = newWidth;
        canvas.height = newHeight;
    }
};

ImageWidget.prototype.open = function(){
   // $('#doc').hide();
 //   this.breadcrumb// = //$('.breadcrumb').html();
    $('#' + this.parent_element).css('display', 'block');

    
    this.display = true;
    this.updateRequired = true;
    this.setView('newspaper');
    $('#' + this.parent_element).show();
    //console.log("sizes", this.canvas.width, this.canvas.height, $('#' + this.parent_element).width(), $('#' + this.parent_element).height())
//    window._samtla.imgwidget.ScrollInToView(window._samtla.imgwidget, window._samtla.imgwidget.current_doc);
};

ImageWidget.prototype.close = function(){
    $('#' + this.parent_element).css('display', 'block');
//    this.state._current = this.state.HIDE;    
    this.display = false;
};

ImageWidget.prototype.hideAll = function(element){
    //console.log("hideAll", VIEW_TYPE, element, element.checked)
    if(VIEW_TYPE == 1){
        //element.checked = true
        $("#rawtext-view").html('Text');
        $('#' + this.parent_element).show();
        $('#zoom-tool').show();
        VIEW_TYPE = 0;
        window._samtla.imgwidget.ScrollInToView(window._samtla.imgwidget, window._samtla.imgwidget.current_doc);
        $('#doc').fadeOut('fast');
        $('#'+this.canvas_element).fadeIn('fast');

        $('#doc').css('display', 'none');
        $('#' + this.parent_element).css('display', 'block');
        $('#' + this.canvas_element).css('display', 'block');
    } else if (VIEW_TYPE == 0){
        //element.checked = false
        $("#rawtext-view").html('Image');
        //$('#' + this.parent_element).hide();
        $('#zoom-tool').hide();
        VIEW_TYPE = 1;
        $('#doc').fadeIn('fast');
        $('#'+this.canvas_element).fadeOut('fast');

        $('#doc').css('display', 'block');
        $('#' + this.parent_element).css('display', 'none');
        $('#' + this.canvas_element).css('display', 'none');

        window._samtla.imgwidget.ScrollInToView(window._samtla.imgwidget, window._samtla.imgwidget.current_doc);
    }
};




