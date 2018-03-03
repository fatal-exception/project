var NER = function(Game){
    this.game = Game;
    this.NER = undefined;
    this.docID = null;
    this.UPDATEMENU = false;
//    this.mouse = utils.captureMouse(document.body);
};


NER.prototype.buildPixelIndex = function(docID){
    url = this.game.ROOT + 'getNERPixelData?docID='+docID;
    this.game.SAMTLA.Search(url, false, false, game.NER.processPixelData);
};

NER.prototype.processPixelData = function(response){
    //console.log("NERS", response.docID, response)
    game.document.imgwidget.loadLayer('NER', response, NERLayer);

//    this.processPixelData(type, ner);

};


NER.prototype.draw = function(docID){
    this.docID = game.document.docID;
    var url = this.game.ROOT + 'getNERdata?docID=' + this.docID;
    this.game.SAMTLA.Search(url, false, false, this.processRequest, true);
};

NER.prototype.browseNER = function(response){
    game.document.Draw(response.docID, response);  
    $('#doc').html(response['html']);
    game.NER.processPixelData(response);
};

NER.prototype.drawDoc = function(querystr){
    console.log("NER get data", querystr)
    
    var data;
    var url = game.ROOT;
    var data = querystr.split(':')//$.parseJSON(element.getAttribute('rel')); TODO: hook this up in the NER menu to read the 'rel' attribute

    var docID = data[0];
    var type = data[1];
    var ner = data[2].replace('_', ' ');
    url += 'getNERHTML?docID=' + docID + '&typeof=' + type + '&NER=' + ner;
    game.SAMTLA.Search(url, false, false, game.NER.processRequest, true);
};



NER.prototype.processRequest = function(response){
    console.log("NER got data", response)
    game.NER.named_entities = response['NERmenu'];
    game.NER.response = response;
    console.log("Draw Menu")
    console.log("Draw Menu DONE")
    game.NER.processPixelData(response);    
    game.googlemap.drawAll(response, undefined);
    game.document.imgwidget.updateRequired = true; // Img-layer/Imagewidget.js in document view
    //$('#NER').html('<a class="list-group-item">No named entities found</a>');
    console.log("NER drawDoc");
    $('#doc').html(response['html']);
    if(game.NER.UPDATEMENU == false){
        game.NER.drawMenu(response);
    }
};

NER.prototype.drawMenu = function(response){
        var html = '<div class="list-group panel">';
        var docID = response.docID;
        var NERS = response.NERmenu;
        console.log(NERS)
        for (var NERtype in NERS){
            if (NERS[NERtype] != undefined){
                var querystr = docID + ":" + NERtype + ":" + NER;
                var callback = ''//'game.NER.drawDoc("' + docID + ":" + NERtype + ':' + 'False' + '")' 
                html +=  '<a href="#NER-' + NERtype + '" ';
                html += 'class="list-group-item list-group-item-success highlight-' + NERtype + '" ';
                html += 'onClick="'+ callback +'" rel=' + querystr
                html += ' data-toggle="collapse" data-parent="#NER" >';
                html += NERtype;
                html += '</a>';   
                html += '<div id="NER-' + NERtype  + '" class="collapse">';
                for (var NER in NERS[NERtype]){
                    html += '<a class="list-group-item" onClick=game.NER.drawDoc("' + docID + ':' + NERtype + ':' + NER + '")>' + NER + '</a>';
                }
                html+='</div>';
            }
        }
        game.NER.UPDATEMENU = true;
        html+='</div>';
        $('#NER').html(html);
        return html;
};

NER.prototype.showInfo = function(description){
    $('#NER-container').html(description); 
};

NER.prototype.hideInfo = function(){
    $('#NER-container').html(''); 
};
