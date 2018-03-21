function initMap() {
    map = new google.maps.Map(document.getElementById("google_map"), mapOptions);
};

window.onload=function(){
    $('.show-sidebar').click();
    _samtla.fetchScripts([
        "static/js/browse/tree.js",
        "static/js/document/imgwidget.js",
        "static/js/document/viewport.js",
        "static/js/document/layer_AABB.js",
        "static/js/document/layer_NER.js",
        "static/js/document/layers.js",
        "static/js/document/NER.js",
        "static/js/document/googlemap.js",
    ]);

    _samtla.settings.corpus = window.location.search.replace("#", '').replace("?", '').split('=')[1];
    _samtla.browse = browse(_samtla.settings.corpus, '#result');
    console.log("window_ref", window.location.href, window.location.search, _samtla.settings.corpus)
//        google.maps.event.addDomListener(window, "load", initMap);
};


(function( _samtla, undefined ) {
    var timeSinceLastFrame = 0;
    _samtla.doc_comparison = null;
    _samtla.settings = {};
    _samtla.data = {};
    _samtla.settings['browser_view'] = 'list'; // One of: 'list', 'treemap'

    _samtla.Tick  = function(){
        var thisFrame = new Date().getTime();
        var dt = (thisFrame - timeSinceLastFrame)/1000;


        if(_samtla.imgwidget && _samtla.imgwidget.updateRequired === true){
            _samtla.imgwidget.update();
            _samtla.imgwidget.draw();
            timeSinceLastFrame = thisFrame;

        }
//            console.log("running");
        window.requestAnimationFrame(_samtla.Tick);
    };



    _samtla.fetchScripts = function (urls){
        for (var u=0; u < urls.length; u ++){
            var url = urls[u];
            var script = document.createElement("script");
            script.setAttribute("src", unescape(url));
            console.log(url, script.src, unescape(url));
            document.getElementsByTagName("body")[0].appendChild(script);
        }
        _samtla.load_settings('.show-sidebar','width');
        console.log('loaded');
    };

    _samtla.setBrowserType = function(){
        var browser_view = $("browser-view");
        if(_samtla.settings['browser_view'] === 'list'){
            _samtla.settings['browser_view'] = 'treemap';
            _samtla.settings['document_view'] ='text';

            browser_view.removeClass("fa fa-th-large");
            browser_view.addClass("fa fa-list");


        } else if(_samtla.settings['browser_view'] === 'treemap'){
            _samtla.settings['browser_view'] = 'list';
            _samtla.settings['document_view'] ='img';


            browser_view.removeClass("fa fa-list");
            browser_view.addClass("fa fa-th-large");


        }
        drawBrowse(_samtla.settings['browser_response'], '#result');

    };
    _samtla.load_settings = function(objName){
        if(localStorage && localStorage[objName]){
            var row = localStorage[objName].split(','),

            attr = row[0],
            val = row[1];
            $(objName).css(attr, val);
            return [objName, attr, val];
        }
    };
    _samtla.save_settings = function(objName, attr){
        if(localStorage){
            localStorage[objName] = attr + "," + $(objName).css(attr);
        }
    };

    _samtla.getDocumentComparison = function(docID, doc2){
        $.getJSON('/document_compare', {
          docID: docID,
          doc2: doc2,
          corpus: _samtla.settings.corpus,
          async: true,
        }, function(data) {
                _samtla.drawDocumentComparison(data);
        });
        return false;
    };

    _samtla.drawDocumentComparison = function(response){
       // console.log("draw document comparison", response);
        _samtla.doc_comparison = new DocComp('#doc', response);
        _samtla.doc_comparison.direction = 'ltr';

        self = _samtla.doc_comparison;
        $('#doc1layer').bind("hover", function(){
            self.highlightMap;
        });
        $('#doc2layer').bind("hover", function(){
            self.highlightMap;
        });

    };


    function replaceAll(str, find, replacewith) {
        return str.replace('/'+find+'/g', replacewith);
    }

    function sortranks(ob){
        ob.sort(function(a, b){return parseInt(a[0]) - parseInt(b[0]);});
        return ob;
    }

}( window._samtla = window._samtla || {} ) );



