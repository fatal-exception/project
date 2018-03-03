function browse(path, element){
    $('#document-toolbar').hide();
    $('.tool-menu').css('visibility', 'hidden');
    $('#google_map').css('visibility', 'hidden');
    //console.log("fetching browse view", path)
    $('#result').css('height', '100%'); 
    $('#loader').show();
    //$('#dashboard-header').html('');
    $('#result-header').html('');
    console.log("Browser", path)
    $.getJSON('/browse', {
        path: path.replace(",",""),
        corpus: _samtla.settings.corpus,
    }, (function(element) {
          return function(data) {
             $('#loader').hide();
             _samtla.settings['browser_response'] = data;
             var colour_path = path.split('%2C');
             var current_colour = null;
             for (var c=0; c < colour_path.length; c++){
                 var colour = data[2][colour_path[c]];
                 console.log(c, colour_path, colour);
                 if (colour != undefined){current_colour = colour}
                 break;
             }
             drawBrowse(data, element, current_colour);
             
          };
       }(element))
    );
    return false;
};

function getPreview(temp, limit){
    if (limit == undefined){
        limit = 15;
    }
    if (temp.length <= limit){
        return temp.join(', ').toTitleCase()
    }
    var prefix = temp.slice(0,limit);
    var mid = ' ... '
    var suffix = temp.slice(temp.length-limit,temp.length);
    var result = prefix.concat(mid, suffix)
    result = uniq(result)
    var junkstr = result.indexOf("");

//    result.pop(junkstr)
//    console.log(result)
    // remove trailing '...' 
    if (result[result.length-1] == mid){
        result.pop(result.indexOf(mid));
    
    }
    for (var r=0; r < result.length; r++){
        result[r] = result[r].toTitleCase()
    }
    return prefix.concat(mid, suffix).join(', ').toTitleCase();
};


function drawTreemap(response, element, colour){
    $('#result-header').html('');
    //$('#dashboard-header').html('');
    t = new Tree();
    
    //console.log("treemap", response, window._samtla.settings['palette']);
    var html = t.draw(response, colour);//[['edition', 0.22657215181124674, '1'], ['issue', 0.3038211993192166, '1'], ['section', 0.3038211993192166, '1'], ['source', 0.07566372063689535, '10'], ['supplement', 0.09012172891342474, '10184']]);
    $(element).html(html);
//    $('#result').css('height', parseInt($('#grid').height()) + 'px');
    utils.resizeFont('.cell-title')
    return t;
};

function drawBrowse(response, element, colour){
    window._samtla.settings['palette'] = response[2];
    var breadcrumb = "";
    var paths = response[0];
    
    if (paths.length == 1){
        breadcrumb += '<li><a href="#" onClick=browse("' + escape(paths)+'","#result")>Home</a></li>';
    } else {
        for (var p=0; p < paths.length; p+=1){
            var crumb = paths[p];
            var path = paths.slice(0, p + 1);
       //     console.log("breadcrumbs:", crumb, window._samtla.settings['palette'], window._samtla.settings['palette'][crumb]);
            path.filter(function (val) {return val;}).join(',');
            breadcrumb += '<li><a href="#" onClick=browse("' + escape(path) + '","#result")>' + unescape(crumb).toTitleCase() + '</a></li>'; 
        }
    }
    $('#breadcrumb-nav').html(breadcrumb);
	// Run beauty tables plugin on every table with class .beauty-table
	$('.beauty-table').each(function(){
		// Run keyboard navigation in table
		$(this).beautyTables();
		// Nice CSS-hover row and col for current cell
		$(this).beautyHover();
	});
	// Attach to click action for create JSON data from tables.
/*	$('.beauty-table-to-json').on('click', function(e){
		e.preventDefault();
		var table = $(this).closest('.box').find('table');
		Table2Json(table);
	});*/
	// Add Drag-n-Drop feature
	//WinMove();


    
    $('#result-header').html('');
//    if (paths[paths.length-1] == paths[paths.length-2]){
        // Don't duplicate path elements at the end of the path array
  //      return;
    //}
    console.log("Browser:", response)

    if(_samtla.settings['browser_view'] == 'treemap'){
        drawTreemap(response, element, colour);

    } else {
        var section = response[1];
        console.log("section", response)
        var html = '<table id="browser-window" class="table beauty-table table-hover"><thead></thead><tbody>';
        var total_rows = section.length//section.length > 50 ? 50 : section.length;

        for (var i=0; i < total_rows; i++){
            var row = section[i];
//            console.log("BROWSING SECTION",row);
            var item = row[0];

            if (item != undefined){
                var temp = row[3];
                var description = getPreview(temp, 15)//.replace(/\,/g, ", ").toTitleCase();        
                var path = paths + "," + item;
                //console.log("description", description)    
                if (temp[0] != undefined && temp[0].split('-')[0] == "getDocument"){
                   //console.log("getDocument!", item, row[2]+"-0")
                   $("html, body").animate({ scrollTop: 0 }, "fast");
                   description = "";

                   var docID = escape(row[2]);
                   _samtla.settings.current_document = docID;
                   html += '<tr class="m-ticker" onClick=browseDocument("'+docID+'")><td>' + item.toTitleCase() + '</td><td>'+description+'</td></tr>';
                  
                } else {
                    html += '<tr id="' + item + '" class="m-ticker" onClick=browse("'+escape(path)+'","#result")><td>' + item.toTitleCase() + '</td><td>'+description+'</td></tr>';    
                }  
           }
            //console.log('<tr id="' + item + '" class="m-ticker" onClick=browse("'+escape(path)+'","#result")><td>' + item.toTitleCase() + '</td><td>'+description+'</td></tr>') 
//        var width = parseInt($('#result').width()) * prob;
//        var height = parseInt($('#result').height()) * prob;
        }
        html += '</tbody></table>';
    }
    $(element).html(html);
};



function browseDocument(docID){
    getDocument(docID, '#result');
}

