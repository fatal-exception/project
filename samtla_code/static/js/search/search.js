$(function() {
    $('#search-button').bind('click', function() {
        getSearch($('input[name="q"]').val(), '#result');
    });

    $('#query').bind('keydown', function(e) {
//        console.log(e.keyCode);
        if (e.keyCode == 13){ 
            getSearch($('input[name="q"]').val(), '#result');
        }
    });
});

    function getSearch(query, element){
        $('#document-toolbar').hide();
        $('.tool-menu').css('visibility', 'hidden');
        $('#google_map').css('visibility', 'hidden');
    //    $('#dashboard-header').html('');
        $('#result-header').html('');
        $('#loader').show();
        console.log("Searching", query, element)
        if (query == null){
           query = $('input[name="q"]').val();
        };
        $.getJSON('/search', {
          q: query,
          corpus: _samtla.settings.corpus 
        }, (function(element){
               return function(data) {
                   $('#loader').hide();
                   console.log("search", query, data, element)
                   drawSearchResults(data, element, 3);
                   $('input[name="q"]').val(query);
                   getRelatedQueries(query, '#result-header')

               };
           }(element))
        );
        return false;
    };


    function drawSearchResults(data, element, num_snippets){
        var ranking = data['ranking'];
        html = '<div>';
       // console.log("drawing search result", ranking)
        for (var r=0; r < ranking.length; r++){

            var title = ranking[r][4];
            //console.log("title",title)
            var docID = ranking[r][2]//#['docID'];
            var snippets = ranking[r][3]//['snippets'];
            //console.log("RNAKING", docID, snippets)

            html += '<hr>';
            html += '<h4><a onClick=getDocument("' + docID + '","#result",true)>' + title + '</a></h4>';
//            html += '<h4><span>' + (parseInt(r)+1) + '</span>: <span onClick=getDocument("' + docID + '","#result",true)>' + title + '</span></h3>';

            if (num_snippets == undefined){
                num_snippets = 1;
            } 
            num_snippets = 10
            i = 0;
            for (var s=0; s < snippets.length; s++){
             //  if (i > num_snippets){
             //     break; 
              // } 
         //      console.log("snippets", s, snippets[s])
               snippet = snippets[s];
               snippet = snippet.replace(/{/g, '<span class="highlight">').replace(/}/g, '</span>');
      
               html += '<ul class="list-inline"><li>'; 
               html += snippet;
               html += '</li></ul>';
               i += 1;
            }
        }

        html += '</div>';
        $('#result').html(html);
    };

   function getRelatedQueries(query, element){
        $.getJSON('/relatedqueries', {
            q: query,
            async: true
        }, (function(element) {
               return function(data) {
                   console.log("related", query, data, element)
                   drawRelatedQueries(data, element);
               };
        }(element))
    );
    return false;
    };

    function drawRelatedQueries(data, status, e, element){
        if (element == undefined){
            element = '#result-header'//'#result-header';
        }
        var limit = 10;
        //var html = '<div class="row">';
        //html += "<p>Related queries</p>";
        var keys = Object.keys(data);
        for (var i in utils.SortDesc(keys).slice(0, limit)){
            var score = keys[i];
            var rq = data[score][1];
      //      console.log(element,  score, data, rq)
          //  html += '<span style="padding: 3px;margin: 3px;" onClick=getSearch("' + rq + '","#result")><a class="btn btn-primary">' + rq + '</a></span>';
           
        }
        //html += '</div>';
        $(element).html(html);
    };
