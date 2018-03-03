var NER_color = {
   'people': 'danger',
   'location': 'success',
   'city': 'success',
   'country': 'success',
   'commodity': 'warning',
   'occupation': 'info',
   'diseases': 'info',
}

var NER = function(Game){
    this.game = Game;
    this.NER = undefined;
    this.docID = null;
    this.UPDATEMENU = false;
    this.geo = {};
//    this.mouse = utils.captureMouse(document.body);
};


NER.prototype.buildPixelIndex = function(docID){
    url = this.game.ROOT + 'getNERPixelData?docID='+docID;
    this.game.SAMTLA.Search(url, false, false, game.NER.processPixelData);
};

NER.prototype.processPixelData = function(response){
    //console.log("NERS", response.docID, response)
    window._samtla.imgwidget.loadLayer('NER', response, NERLayer);

//    this.processPixelData(type, ner);

};


NER.prototype.draw = function(docID){
    getNER(docID, false);
};

NER.prototype.browseNER = function(response){
    //game.document.Draw(response.docID, response);  
    //console.log("BROWSE NER", response)
    //$('#doc').html(response['html']);
    this.processPixelData(response);
};

NER.prototype.drawDoc = function(querystr, reload){
    //console.log("NER get data", querystr)

    var data;
    var url = game.ROOT;
    var data = querystr.split(':')//$.parseJSON(element.getAttribute('rel')); TODO: hook this up in the NER menu to read the 'rel' attribute

    var docID = data[0];
    var type = data[1];
    var ner = data[2].replace('_', ' ');
    url += 'getNERHTML?docID=' + game.document.docID + '&typeof=' + type + '&NER=' + ner;
    game.SAMTLA.Search(url, false, false, game.NER.processRequest, true);
};

NER.prototype.getNERMenu = function(){
    //console.log("getting NER menu")
    var url = game.ROOT;

    url += 'getNERMenu?docID=' + game.document.docID;
    game.SAMTLA.Search(url, false, false, game.NER.drawMenu, true);

};

NER.prototype.processRequest = function(response){
    //console.log("NER got data", response)
    game.NER.named_entities = response['NERmenu'];
    game.NER.response = response;
    game.NER.geo = response.KML;
    UPDATE_REQUIRED = true;
    
    game.NER.processPixelData(response);    

    
    game.googlemap.drawAll(response, undefined);
   // $('#NER').html('<a class="list-group-item">No named entities found</a>');
//    game.NER.drawMenu(response);
    game.document.imgwidget.updateRequired = true; // Img-layer/Imagewidget.js in document view
    $('#doc').html(response['html']);
    $('#doc-title').html(response['title']);
    $('#thebreadcrumb').html(response.breadcrumb);
};

NER.prototype.drawMenu = function(response){
        var docID = game.document.docID //response.docID;
        var html = '<div class="list-group panel">';
        console.log("drawNERMenu", response, response['NERmenu'], typeof(response['NERmenu']))
//        if (Object.keys(response['NERmenu']).length == 0){
//            $('#NER-group-menu').hide();
//            return; 
//        }
        var NER = 'False'
        var NERS = response.NERmenu;
      //  if(NERS == undefined){
      //      $('#NER-group-menu').hide();
       //     return "";
       // } else {
        //    $('#NER-group-menu').show();
        //}
        for (var NERtype in NERS){ 
            if (NERS[NERtype] != undefined){
                var querystr = docID + ":" + NERtype + ":" + NER;
                var callback = 'game.NER.drawDoc("' + docID + ':' + NERtype + ':' + 'False")' 
                var color = NER_color[NERtype];
                html +=  '<a href="#NER-' + NERtype + '" ';
                html += 'class="list-group-item list-group-item-'+color+' highlight-' + NERtype + '" ';
                html += 'onClick='+ callback +' rel="' + querystr
                html += '" data-toggle="collapse" data-parent="#NER" >';
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

        game.document.imgwidget.updateRequired = true;
        return html;
};

NER.prototype.showInfo = function(description){
    $('#NER-container').html(description); 
};

NER.prototype.hideInfo = function(){
    $('#NER-container').html(''); 
};
