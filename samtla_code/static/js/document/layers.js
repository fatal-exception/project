
var Layers = function(){
    this.current_id = null;
    this.objects = {};
};

Layers.prototype.add = function(id, objs){
    this.objects[id] = objs;
    this.current_id = id;
    //console.log("added layer", id)
};

Layers.prototype.clear = function(){
    this.objects = {};
    this.current_id = null;
};

Layers.prototype.draw = function(controller){
    //console.log(controller.state)
    for (var l in this.objects){
        if(this.objects[l].draw){ // this.current_id
            this.objects[l].draw(controller);        
        }
    }
};

