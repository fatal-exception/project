var googlemap_data = {};
var map = null;

function getNERmetadata(element, NER, data){
    //if (data == undefined){return};
     
    //if (typeof(data) == 'object'){return}
    var meta = data.replace(':', ': ').replace('\n', '<br>');
    element.setAttribute('title', meta);
    var row = data.split('point:')[1];
    console.log("mydata",data);
    if (row === undefined){geo=row}
    var geo = row.split('\n')[0].split(' ');
    console.log("hover google map", element, meta, typeof(meta), geo);
    var myLatlng = new google.maps.LatLng(parseFloat(geo[0]), parseFloat(geo[1]));
    var mapOptions = {
        zoom: 4,
        center: myLatlng
    };
    map = new google.maps.Map(document.getElementById("google_map"), mapOptions);
    var marker = new google.maps.Marker({
        position: myLatlng,
    });
    var infowindow = new google.maps.InfoWindow({
        content: meta
    });

    marker.addListener('click', function() {
        infowindow.open(map, marker);
    });
    // To add the marker to the map, call setMap();
    marker.setMap(map);
             $('#google_map').show();
             $('#google_map').focus();
    
};

function getKML(element){
   // console.log(element)
    var entity = element.target.attributes.name.value;
    if (entity != undefined){
        NER = entity.split('_')[1];
    }
    console.log("get entity", NER.split('_')[1])
    $.getJSON('/KML', {
        corpus: _samtla.settings.corpus,
        NER: unescape(NER),
        cat: unescape(entity.split('|')[0]),
        async: true,
        dataType: "json",
    }, (function(element) {
          return function(data) {
             console.log("KML data", NER, data)
             window._samtla.data['KML'] = data.KML;
             getNERmetadata(element.target, NER, data);
          };
       }(element))
    );
    return false;
};

function getNER(docID, element, NERtype, NER, reload){
    //console.log(docID, element, NERtype, NER, reload)
    $('#loader').show();
    $.getJSON('/NER', {
        docID: docID,
        corpus: _samtla.settings.corpus,
        NERtype: unescape(NERtype),
        NER: unescape(NER),
        async: true,
        dataType: "json",
    }, (function(element) {
          return function(data) {
             //console.log("getNER", data);
//             window._samtla.data['KML'] = data.KML;
             var elem = document.getElementById('doc');
//             console.log("elem", elem)

             drawNER(data, element, reload);
             addEvent('NER');

             //filterNER(elem, 'NER')
             //console.log("getNER", docID, element, unescape(NERtype), unescape(NER), data.KML);
          };
       }(element))
    );
    return false;
};


function addEvent(classof){
    var e = document.getElementsByClassName(classof);

    for(i in e){
        //console.log("filterNER", classof, e[i], e[i].style);
        if(e[i]){
            if (e[i] != undefined && e[i].dataset != undefined){
                e[i].addEventListener('hover', getKML);   
                e[i].addEventListener('click', getKML);   
            }

        }
    }
    $('#loader').hide();
};

function filterNER(filterby){
//    var e = document.getElementsByClassName('NER');
//    $('.NER').fadeOut('fast');
//    $('.'+filterby).fadeIn('fast');
//    return;
    return
    for(i in e){
        //console.log("filterNER", e[i].classList);
        var classes = e[i].classList.value.split(' ');
        var style = e[i].style;
        for (var c = 0; c < classes.length; c++){ 
          //  console.log("classes", filterby, classes[c] == filterby)
            if(classes[c] == filterby){
                style.borderBottomWidth="2px";
            } else {
                style.borderBottomWidth="0px";
            }
        }
    }
};



function drawNERMenu(docID, element, data){
    //console.log("draw NER menu", data);
    var temp = {};
    var scores = [];
    var sortable = [];
    for (var rowid in data){
        item = rowid.split('|');
        var type = item[0]
        if (type == 'Animal'){continue}
        temp[type] = {}
        var category = item[1]

        var NERs = data[rowid];
        temp[type][category] = []
        //console.log(rowid, type, category)
        for (var NER in NERs){
            //console.log(type,category, NER, NERs)
            temp[type][category][NER] = NER.length;
            sortable.push({'ner': NER, 'value': NERs[NER].length,'type':type,'cat':category})
        }
    }

    //for (var rowid in data){
      //  item = rowid.split('|');
        //var type = item[0]
        //var category = item[1]
        //var NER_data = temp[type][category];
        //console.log("NERs", temp)  
        //console.log(NER_data)
   // }
    sortable.sort(function(a, b) {
        return b.value - a.value;
    });

    var menu = {} 
    for (var i=0; i < sortable.length; i++){
        var obj = sortable[i]; 
        if (menu[obj.type] === undefined){
            menu[obj.type] = {};
        }
        if (menu[obj.type][obj.cat] === undefined){
            menu[obj.type][obj.cat] = {};
        }
        var NER = obj.ner;
        var NERcount = obj.value;
        menu[obj.type][obj.cat][NER] = NERcount;

    } 
//    console.log("TEMP", menu)

    var html = "";
    for(var type in menu){
        var option = type.toLowerCase().split('|')[0];
        var background = "";
        html += '<div>';
	html += '<hr>';
	html += '<h4><a class="hidden-xs" href="#' + type + ' class="' + type + '">' + type.toTitleCase() + '</a></h4>';

	html += '<hr>';
	html += '<ul>';

    	for(var cat in menu[type]){
    	    // console.log("draw NER menu", type, NER, data[type][NER].length);
            if (cat !== type) {
                html += '<br>';
    	        html += '<ul><a href="#' + type + '|' + cat + '" class="'+type.toTitleCase+'"><b>' + cat.toTitleCase() +'</b></a>';
    	    }
            if (cat === 'Mammal'){continue}
    	    for(var NER in menu[type][cat]){
  
    	        html += '<li><a href="#' + type + '|' + cat +'_'+ NER + '">' + NER.toTitleCase() +'</a><span class="NERstat"> ('+menu[type][cat][NER]+')</span></li>';
    	    }
    	    html += '</ul>';
    	}
    	html += '</ul>';
	html += '</div>';
    };
    $("#NERS-menu").html(html);
};


function drawNER(data, element, reload){
    $('#google_map').css('visibility', 'visible');
    $('#doc').html(data.NER.html.replace(/\*/g, '</br>')); //.replace(/\*/g, '</br></br>'));
    //console.log("kml",data.NER.kml)
    //getNERmetadata(element, data.NER.kml);
    if (reload != false){
        drawNERMenu(data.docID, element, data.NER.idx);
    }
    if(window._samtla.imgwidget){
        VIEW_TYPE = 1;
        window._samtla.imgwidget.hideAll();        
        window._samtla.imgwidget.loadLayer('NER', data, NERLayer);
    }
};

