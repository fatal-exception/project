function Camera(canvas){
    this.canvas = canvas;
    this.zoom = 1;
    this.amount = 0.1;
    this.xScroll = 0;
    this.yScroll = 0;
    this.width = this.canvas.width;
    this.height = this.canvas.height;
    this.state = {
        _current: 0,
        FOLLOW: 0,
        PAN: 1,
    }
    this.cameraPosition = [this.xScroll, this.yScroll];

    // these will be used to lerp to the next position 
    this.prevCameraPosition = [this.xScroll, this.yScroll]; 
    this.curCameraPosition = [this.xScroll, this.yScroll]; 
    this.lerpAmount = 1.0;
    this.target = undefined; 
    this.boundary = {x: this.width, y: this.height};
};

Camera.prototype.Anchor = function(obj){
    this.target = obj;
    console.log("set camera target", obj)
};

Camera.prototype.Lerp = function(A, B, t){
    return (A * t) + ((1 - t) * B);
};


// Update Method
Camera.prototype.update = function(dt){
    this.x = this.canvas.width * 0.5;
    this.y = this.canvas.height * 0.5

    if(this.target){
        this.dx = (this.target.x - this.x);
        this.dy = (this.target.y - this.y);

        //the camera moved 
        this.cameraPosition = [this.xScroll, this.yScroll];
        if(this.cameraPosition != this.curCameraPosition){ 
            this.lerpAmount = 0.0; 
            this.curCameraPosition = this.cameraPosition; 
        } 
 
        if(this.lerpAmount < 1.0){
            this.lerpAmount += 0.05; 
        } else {
            this.prevCameraPosition = this.curCameraPosition; 
        }

        this.xScroll = (this.Lerp(this.dx, this.curCameraPosition[0], this.lerpAmount)); 
        this.yScroll = (this.Lerp(this.dy, this.curCameraPosition[1], this.lerpAmount));

        if(this.xScroll < 0){
            this.xScroll = 0; 
        }
        
        if(this.xScroll >= (this.boundary.x - this.canvas.width)){
            this.xScroll = (this.boundary.x - this.canvas.width); 
        }

        if(this.yScroll < 0){
            this.yScroll = 0; 
        }

        if(this.yScroll >= this.boundary.y){
            this.yScroll = this.boundary.y; 
        }
        console.log(this.xScroll, this.yScroll) 
    }
};

Camera.prototype.keydown = function (event) {
    switch (event.keyCode) {
        case 187: //+  
            if(this.zoom < 0.9 ){
                this.zoom += this.amount;
            }
            break;
        case 189: //-
            if(this.zoom > 0.1 ){
                this.zoom -= this.amount;
            }
            break;
        case 107: //+  
            if(this.zoom < 0.9 ){
                this.zoom += this.amount;
            }
            break;
        case 109: //-
            if(this.zoom > 0.1 ){
                this.zoom -= this.amount;
            }
            break;
    }
};

Camera.prototype.keyup = function (event) {
    switch (event.keyCode) {
        case 187: //+        
            break;
        case 189: //-
            break;
    }
};
