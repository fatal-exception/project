function getDocument(docID, element, highlighted_flag){
    $('.tool-menu').css('visibility', 'visible');
//    $('#google_map').css('visibility', 'hidden');
    $('#loader').show();
    if(highlighted_flag == undefined){
        highlighted_flag = false;
    }
//    console.log("get document", docID, element, highlighted_flag);
    $.getJSON('/document', {
        docID: docID,
        corpus: _samtla.settings.corpus,
        highlighted: highlighted_flag,
        async: true
    }, (function(element) {
          $(element).fadeOut('fast');
          return function(data) {
             _samtla.settings['docID'] = docID;
             drawDocument(data, element, docID);
             getMetadata(docID, '#metadata');
             getRelatedDocuments(docID);
            // getNER(docID, '#doc', false, false);
             $('#loader').hide();
          };
       }(element))
    );
    return false;
};

function drawDocument(data, element, docID){
    $('#doc').css('height', (window.innerheight*.80) + 'px');
    $('#doc').css('overflow', 'auto');

    $('#NER-menu-load').bind('click', function(e) {
         console.log("NER menu", docID)
         getNER(_samtla.settings['docID'], '#doc', false, false);
    });
    $('#related-menu-load').unbind('click', function(e) {
         getRelatedDocuments(_samtla.settings['docID']);
    });

    $('#related-menu-load').bind('click', function(e) {
         getRelatedDocuments(_samtla.settings['docID']);
    });
  //  console.log("draw document", data, element);
    _samtla.settings['document_data'] = data;

    var text = data['document']['text'].replace(/{/g, '<span class="highlight">').replace(/}/g, '</span>');
    var text = text.replace(/\*/g, '</br>');
    var img = ""; 

    if (data['document']['image'] != undefined){
        img = data['document']['image'][0]; 
    }
    console.log("img", img)
    _samtla.settings['imgwidget'] = img; 
    var title = data['title']; 
    title = '<div id="doc-title"><h4>' + title + '</h4></div>';
    $('#result-header').html(title);


//<script async defer src= type="text/javascript"></script>

    var html = '<div class="row"><div id="img-layer" class="col-xs-8 col-sm-8 col-md-8" style="position:relative;top:10px;display: none;height: 90%;" ><canvas id="img-canvas-layer" title="" alt=""></canvas></div><hr>';


    html += '<div id="doc" class="col-xs-8 col-sm-8 col-md-8"></div>';

    html += '<div class="col-xs-4 col-sm-4 col-md-4" style="height: 100%;">';

html += '<ul class="nav nav-tabs" role="tablist">';
html += '  <li class="nav-item">';
html += '    <a class="nav-link active" href="#metadata" role="tab" data-toggle="tab">Metadata</a>';
html += '  </li>';
html += '  <li class="nav-item">';
html += '    <a class="nav-link" href="#related_docs" role="tab" data-toggle="tab">Similar</a>';
html += '  </li>';
html += '  <li class="nav-item">';
html += '    <a class="nav-link" href="#NERS-menu" role="tab" data-toggle="tab" id="NER-menu-load" onClick=getNER("'+docID+'","#doc")>Entities</a>';
html += '  </li>';
html += '</ul>';

html += '<div class="tab-content" style="overflow:auto;width:100%;">';
html += '  <div role="tabpanel" class="tab-pane fade in active" id="metadata">No Metadata found for this document.</div>';
html += '  <div role="tabpanel" class="tab-pane fade" id="related_docs">No related documents found.</div>';
html += '  <div role="tabpanel" class="tab-pane fade" id="NERS-menu">Retrieving Named Entities...</div>';
html += '</div>';


    html += '</div>';

    $('#result').html(html);
    //window.location.href = window.location.href.replace('#','');
    text = text.replace('*', '<br><br>')//utils.lineBreaker(text, {'line_break':'*'}, "<br><span class='num'>", ". </span>", "</br>");
    if ((img !=undefined && img.length > 1) || _samtla.settings['document_view'] =='img' && img != _samtla.settings['imgwidget']){
        $('#document-toolbar').show();
        $('#doc').html(text.replace(title, ""));

        $('#img-layer').fadeIn('fast');
        $(element).fadeIn('fast');
        _samtla.settings['document_view'] = 'img';
        drawImageContainer(data, '#img-layer');

    } else {
        $('#document-toolbar').hide();
        $('#doc').html(text.replace(title, ""));
        _samtla.settings['document_view'] = 'text';
        $(element).fadeIn('fast');
        $('#img-layer').fadeOut('fast');
//        drawImageContainer(data, '#img-layer');
    }


   // var script = document.createElement("script")
   // var url = "https://maps.googleapis.com/maps/api/js?key=AIzaSyBc3dfjdO8FF29mkdGYkZL6-FoMU1OzvaI&callback=initMap";
   // script.setAttribute("src", url);
   // document.getElementsByTagName("body")[0].appendChild(script);

};

function getMetadata(docID, element){
   // console.log("get document", docID, element);
    $.getJSON('/document_metadata', {
        docID: docID,
        corpus: _samtla.settings.corpus,
        async: true
    }, (function(element) {
          return function(data) {
             drawMetadata(data,element);
          };
       }(element))
    );
    return false;
};

function drawMetadata(data, element){
  //  console.log("draw metadata", data, element);
    var html = '';
    for (var field in data){
        console.log(field, data[field])
        var val = data[field];
        if (field == 'image'){
            html += '<img id="meta-img" src="static/img/' + val + '" />';

        } else {
            html += '<p href="#">'
            html += '<b>' + field.toTitleCase() + '</b>:<p>' + val +'</p>';
            html += '</p>';
        //console.log(field)
        }
    }
    $(element).html(html);
};

function getRelatedDocuments(docID, element){     
        $.getJSON('/document_related', {
            docID: docID,
            corpus: _samtla.settings.corpus
        }, (function(element) {
               return function(data) {
                   drawRelatedDocuments(docID, data, element);

               };
        }(docID, element))
    );
    return false;
};

function drawRelatedDocuments(docID, data, status, e, element){
    if (element == undefined){
        element = '#related_docs'//'#result-header';
    }
//    console.log(docID, data, status);
    var html = '';
    for (var i=0; i < data.length; i++){
        var score = data[i][0];
        var doc2 = data[i][1];
        var title2 = data[i][2];
        html += '<li class="" onClick=_samtla.getDocumentComparison(' + docID + ',' + doc2 + ')><a>' + title2 + '</a></li>';
       // html += '<a style="text-decoration: ellipse;" onClick="getDocument(' + doc2 + ')">' + title2.slice(0,41) + '...</a><br>';
    }
    $(element).html(html);
};


function drawImageContainer(data, element){
    $('#loader').hide();
    var html = "";
    html += '<div class="row">';
    html += '<span id="rawtext-view" class="btn btn-primary" onClick="window._samtla.imgwidget.hideAll()" >Text</span>';
    html += '<span id="zoom-tool">';

    html += '    <span id="zoom-out" class="btn btn-info" onClick=window._samtla.imgwidget.ZoomOut()><span id="zoom-out" class="glyphicon glyphicon-zoom-out" ></span></span>';
    html += '    <span id="magnify-tool"><span id="zoom"></span></span>';
    html += '    <span id="zoom-in" class="btn btn-info" onClick=window._samtla.imgwidget.ZoomIn()><span id="zoom-in" class="glyphicon glyphicon-zoom-in"></span></span>';
    html += '</span>';
   

    html += '</div>';    

    $('#document-toolbar').html(html);

    $(element).html(html);
    window._samtla.imgwidget = new ImageWidget('img-layer');
    window._samtla.imgwidget.Init(data, _samtla.settings['docID']);
    var self = window._samtla.imgwidget;
    window._samtla.imgwidget.ScrollInToView(self, self.current_doc);
  //  $('#img-layer').css('width', parseInt($('#result').width())+'px');
//    var html = "";
//    html += '<canvas id="img-canvas-layer" title="" alt=""></canvas>';
//    $(element).html(html);
//    window._samtla.imgwidget = new ImageWidget('doc');
//    window._samtla.imgwidget.Init(data);

    return html;
};

