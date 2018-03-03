function createContext(ID, targetID, height) {
    var canvas = document.createElement('canvas');
    canvas.id = ID;
    canvas.height = height;
    console.log("Map create context", document, canvas, ID, targetID, height)
    try {
    document.getElementById(targetID).appendChild(canvas);
    canvas = document.getElementById(ID);
    
    return canvas, canvas.getContext("2d");
    } catch(err){return false, false}
}

// DocMap Objects
function DocMap(doc_comparison){
    this.doc_comparison = doc_comparison;
    this.doc1 = doc_comparison.doc1;
    this.doc2 = doc_comparison.doc2;

    this.current_length = 0;
    this.seedID = 0;
    this.selected = {};

    this.Init();
    this.Get();
};

DocMap.prototype.Init = function(){
    this.data = {}
    this.highlighted_sequences = {};
    this.selected_sequences = {};
    this.selected = {};
    this.canvas1, this.context1 = createContext('canvas1', 'doc1map', 8) 
    this.canvas2, this.context2 = createContext('canvas2', 'doc2map', 8) 
    //$('#doc1map').html(this.canvas1);
    //$('#doc2map').html(this.canvas2);
    
    this.update_required = true;
    this.fps = 60;
    this.timeSinceLastFrame = new Date().getTime();
    this.timeBetweenFrames = 1/this.fps;
    this.mouse1 = {}//utils.captureMouse(this.canvas1);
    this.mouse2 = {}//utils.captureMouse(this.canvas2);
    this.rtl = undefined;

    this.update_required = true;
};

DocMap.prototype.Get = function(){
    var data = this.doc_comparison.data;
    this.data = {};
    this.data[this.doc1] = {}
    this.data[this.doc2] = {}
    console.log("get map", this.doc_comparison)
    this.data[this.doc1].map = data.docmap[this.doc1];
    this.data[this.doc2].map = data.docmap[this.doc2];
    this.data[this.doc1].seeds = data.largest[this.doc1];
    this.data[this.doc2].seeds = data.largest[this.doc2];

    this.data[this.doc1].width = data.text['doc1'].length;
    this.data[this.doc2].width = data.text['doc2'].length;
};

DocMap.prototype.onMouseDown = function(e){

};

DocMap.prototype.onMouseUp = function(e){
//    console.log(this.mouse1.x, this.mouse1.y);
//    console.log(this.mouse2.x, this.mouse2.y);
//    this.background = [];
//    this.foreground = [];
//    this.selected = [];
};

DocMap.prototype.update = function(){
    if(this.update_required){

    }
}; 

DocMap.prototype.drawSelected = function(){

};

DocMap.prototype.GetSequenceTypes = function(docID){
    this.background = [];
    this.foreground = [];
    //
  //  console.log(this.data, this.data[docID], this.data[docID].map)
    var i, j, k,
        start, 
        end,
        high_start, 
        high_end,
        high_start, 
        high_end,
        pos,
        width = this.data[docID].width;

    // Get all
    for (i = 0; i < this.data[docID].map.length; i++){
        if(this.rtl){ 
            start = width - this.data[docID].map[i][0];
            end = width - this.data[docID].map[i][1]; 
        } else {
            start = this.data[docID].map[i][0];
            end = this.data[docID].map[i][1]; 
        }
        this.background.push([start, (end-start)]); 
    }
    if(this.highlighted_sequences[docID]){
    // Get foreground
    for (j = 0; j < this.highlighted_sequences[docID].length; j++){
        if(this.rtl){ 
            high_start = width - this.highlighted_sequences[docID][j][0];
            high_end = width - this.highlighted_sequences[docID][j][1];
        } else {
            high_start = this.highlighted_sequences[docID][j][0];
            high_end = this.highlighted_sequences[docID][j][1];
        }
        this.foreground.push([high_start, (high_end - high_start)]);
    }
    }
    var temp = [];
   // console.log("selected", this.selected)
    if(this.selected!=undefined && this.selected[docID]){
        for(k = 0; k < this.selected[docID].length; k++){
            pos = this.selected[docID][k];
            if(this.rtl){ 
                start = width - pos[0];
                end = width - pos[1];
            } else {
                start = pos[0];
                end = pos[1];
            }
            temp.push([start, (end - start)]);
            console.log("Select", docID, start, end, width, pos, temp)
        }
    }
    this.update_required = true;
    return {background: this.background, foreground: this.foreground, selected: temp};
};

DocMap.prototype.draw = function(){
    if(this.update_required){
    this.seedID = this.doc_comparison.currentSelection;
    var sequences = this.GetSequenceTypes(this.doc1);
    this.canvas1 = document.getElementById('canvas1')
    this.canvas2 = document.getElementById('canvas2')
    this.context1 = this.canvas2.getContext('2d')
    this.context2 = this.canvas2.getContext('2d')

    for (var i = 0; i < sequences.background.length; i++){
        this.context1.fillStyle = 'rgba(195,239,253,0.5)';
        this.context1.fillRect(sequences.background[i][0], 0, sequences.background[i][1], this.canvas1.height);
    }
    for (var i = 0; i < sequences.foreground.length; i++){ 
        this.context1.fillStyle = '#20abff';
        this.context1.fillRect(sequences.foreground[i][0], 0, sequences.foreground[i][1], this.canvas1.height);     
    }
    if(sequences.selected!=[]){
        for (var i = 0; i < sequences.selected.length; i++){
            this.context1.fillStyle = '#fa0';
            this.context1.fillRect(sequences.selected[i][0], 0, sequences.selected[i][1], this.canvas1.height);
        }
    }
    var sequences = this.GetSequenceTypes(this.doc2);
    for (var i = 0; i < sequences.background.length; i++){
        this.context2.fillStyle = 'rgba(195,239,253,0.5)';
        this.context2.fillRect(sequences.background[i][0], 0, sequences.background[i][1], this.canvas2.height);
    }
    for (var i = 0; i < sequences.foreground.length; i++){
        this.context2.fillStyle = '#20abff';
        this.context2.fillRect(sequences.foreground[i][0], 0, sequences.foreground[i][1], this.canvas2.height);
     
    }
    if(sequences.selected!=[]){  
        for (var i = 0; i < sequences.selected.length; i++){
            this.context2.fillStyle = '#fa0';
            this.context2.fillRect(sequences.selected[i][0], 0, sequences.selected[i][1], this.canvas2.height);
        }
    }
    }
};

