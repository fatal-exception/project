var Resize = function(){};

var DocComp = function(element, data){
//    if(element){
//        this.main_window = element;
//        this.map_window = element;//
//    } else {
        this.main_window = element;
        this.map_window = element;
//    }
    this.direction = "";
    this.state = {
        _current: 0,
        CONSUME: false,
    }
   // console.log(data)
    this.Init(data);
   console.log("ready comp")
};

DocComp.prototype.restoreText = function(){

};

DocComp.prototype.Init = function(data){
    $('#document-toolbar').hide();
    $('#result-header').html('');
//    $('#dashboard-header').html('');
    this.slide = null;
    this.map = null;
    this.data = data;
    this.doc1 = data.doc1;
    this.doc2 = data.doc2;
    this.scrolldocID = "";
    this.html = ""; 
   // console.log("doc_comp, init", data)
    if(this.data==undefined){
        //this.html = '<div class="title" style="margin-top: 50px;">Sorry we do not have the data for that comparison.</div>';
        this.map_html = "";
        $(this.main_window).html(this.html);
    } else {
        this.doc1_title = this.data['docnames'][this.doc1]
        this.doc2_title = this.data['docnames'][this.doc2]     


        this.html += '<table id="comparison_docs" class="table">';
        this.html += '<thead>';
        this.html += '<tr>';
        this.html += '<td class="col-md-1"><h4>' + this.doc1_title + '</h4></td>';
        this.html += '<td class="col-md-1"><h4>' + this.doc2_title + '</h4></td>';       
        this.html += '</tr>';       
        this.html += '<tr>';    
       // this.html += '<td class="col-md-1"><span id="doc1map" style="border: solid 1px grey;"></span></td>';
       // this.html += '<td class="col-md-1"><span id="doc2map" style="border: solid 1px grey;"></span></td>';       
        this.html += '</tr>';       
        this.html += '</thead>'         

        this.html += '<tbody>';
        this.html += '<tr>';
        this.writing_direction = 'ltr';
//        $('#result-header').html('')


        if (this.writing_direction == 'ltr'){
            this.html += '<td><div id="doc1layer" class="col-xs-12 col-sm-12 col-md-12 col-lg-12" style="text-align: left;" onClick="_samtla.doc_comparison.setScroll(2)"></div></td>';
        } else {
            this.html += '<td><div id="doc1layer" class="col-xs-12 col-sm-12 col-md-12 col-lg-12" style="text-align: right;" onClick="_samtla.doc_comparison.setScroll(2)"></div></td>';
        }


        if (this.writing_direction == 'rtl'){
            this.html += '<td><div id="doc2layer" class="col-xs-12 col-sm-12 col-md-12 col-lg-12" style="text-align: right;" onClick="_samtla.doc_comparison.setScroll(1)"></div></td>';
        } else {
            this.html += '<td><div id="doc2layer" class="col-xs-12 col-sm-12 col-md-12 col-lg-12" style="text-align: left; onClick="_samtla.doc_comparison.setScroll(1)"></div></td>';

        }

        this.html += '</tr>';

        this.html += '</tbody>';
        this.html += '</table>';

        $(this.main_window).html(this.html); 


        ///this.html = '<table class="table">';
        //this.html += '<tr id="slider" class="container-fluid">';
        //this.html += '<td id="slidingbar" class="pagination"></td>';
        //this.html += '</tr>';
        //this.html += '</table>';
        //$('#result-header').html(this.html); 


//        var offsetY = parseInt($('#slidingbar').offset().Top) + (parseInt($('#slidingbar').height()) * 0.5);
        //$('#slideaxis').css('top', offsetY + 'px');
        $('#description').html('');
        this.previousSelection = undefined;
        this.currentSelection = undefined;
        this.current_doc = this.doc1;
        this.text = this.data.text;
        this.html = this.data.html;
        this.largest_seeds = this.data.largest;
//        this.snippet = new Snippet(this);

        this.state = {
            _current: 0,
            LOADED: 0,
            ERROR: 3
        }
        this.markers = {line_break: "*", begin_highlight: "{", end_highlight: "}", begin_largest: "{", end_largest: "}"};
       // console.log("largest seeds (doc_comp)",this.largest_seeds[this.doc1], this.largest_seeds[this.doc2])
        this.document1_html = document.getElementById('doc1layer'); 
        this.document2_html = document.getElementById('doc2layer'); 
        this.document2_map_overlay = document.getElementById('doc1_mapoverlay'); 
        this.document2_map_overlay = document.getElementById('doc2_mapoverlay'); 

        this.doc1_textarea_lined = ''//utils.lineBreaker(this.text.doc1, this.markers, "\r", ". ", " \r");
        this.doc2_textarea_lined = ''//utils.lineBreaker(this.text.doc2, this.markers, "\r", ". ", " \r");

        // Get largest seeds
        this.text1 = new Corpusline(this.doc1, this.text.doc1.text, this.markers);
        this.text2 = new Corpusline(this.doc2, this.text.doc2.text, this.markers);
        this.seed = new Seed(this);
        this.doc1_largest = this.seed.getLargestSeeds(this.doc1, this.largest_seeds[this.doc1], this.text1);
        this.doc2_largest = this.seed.getLargestSeeds(this.doc2, this.largest_seeds[this.doc2], this.text2);
      //  console.log("doc1 largest", this.doc1_largest, this.largest_seeds[this.doc1])
      //  console.log("doc2 largest", this.doc2_largest, this.largest_seeds[this.doc2])

        this.setupDocs();

    }
    //$('.num').hide();
};

DocComp.prototype.setupDocs = function(){
    this.map = new DocMap(this);
    this.slide = new Slider(this);
    this.slide.Init(this);

//    this.setupElementPosition();
    this.renderLargest();

//    $('#ex1').slider({
//    	formatter: function(value) {
//		    return 'Current value: ' + value;
//	    }
//    });
    //$('#doc1layer').css('width', parseInt((window.innerWidth * (1-0.2)) * 0.39) + 'px');
    //$('#doc2layer').css('width', parseInt((window.innerWidth * (1-0.2)) * 0.39) + 'px');
    $('#doc1layer').css('height', (parseInt($('#doc').height()) * 0.70) + 'px');
    $('#doc2layer').css('height', (parseInt($('#doc').height()) * 0.70) + 'px');
//    $('#canvas1').css('width', parseInt($('#doc1layer').css('width'))+'px');
//    $('#canvas2').css('width', parseInt($('#doc2layer').css('width'))+'px');
    //$('#doc').css('background-color', '#f1f1f1');
    //$('#doc').css('border', 'none');
//    $('#NER-container').hide();
//    $('#doc-title').hide();
//    $('#doc-toolset').hide();
//    $('#result_window').css('overflow', 'hidden');
    //$('#doc1layer').css('height', (parseInt($('#doc_wrapper').height()) - parseInt($('#doc_wrapper').offset().top)) + 'px');
    //$('#doc2layer').css('height', (parseInt($('#doc_wrapper').height()) - parseInt($('#doc_wrapper').offset().top)) + 'px');
    //$('#result_window').css('height', (parseInt($('body').height())-offsetY) + 'px');
   // $('#result_window').css('height', (parseInt($('body').height())-offsetY) + 'px');
//    $('#doc1layer').scrollTo($('#' + this.seed.largestseedID));
//    $('#doc2layer').scrollTo($('#' + this.seed.largestseedID));
    $('preloader').hide();
};

DocComp.prototype.setScroll = function(element){
    this.scrolldocID = '#doc' + element + 'layer';
  //  console.log(this.scrolldocID)
//    this.highlightMap;
    this.Scroll('.highlight', this.scrolldocID);
};

DocComp.prototype.setupElementPosition = function(){
    // Calculate negative offset for overlay
    var height = $('#doc1layer').height();
    var lineheight = parseInt($('#doc1layer').css('line-height'));
    var doc1line_count = parseInt(Math.floor(height/lineheight));

    var height = $('#doc2layer').height();
    var lineheight = parseInt($('#doc2layer').css('line-height'));
    var doc2line_count = parseInt(Math.floor(height/lineheight));

};

DocComp.prototype.getValue = function(element){
    this.slide.map.selected = {}
    this.slide.map.selected[this.doc1] = [];
    this.slide.map.selected[this.doc2] = [];

    this.currentSelection = element.getAttribute('id');
    //console.log("get value", element, this.currentSelection)
    var self = this;
    $('#doc1layer').find('span').each(function(i, e){
        var ID = $(this).attr('id');          
        if(ID == self.previousSelection){
            $(this).removeClass('highlight_select');
            $(this).addClass('highlight');
            $(this).children().removeClass('highlight_select');
            $(this).children().addClass('highlight');
        }
        if(ID == this.currentSelection){
            $(this).removeClass('highlight');
            $(this).addClass('highlight_select');
            $(this).children().removeClass('highlight');
            $(this).children().addClass('highlight_select');
            self.Scroll('.highlight_select', '#doc2layer');            
      //      console.log("doc1 filterBY", this, i, this.currentSelection, ID);
        }
    });
    $('#doc2layer').find('span').each(function(i, e){
        var ID = $(this).attr('id');          
        if(ID == self.previousSelection){
            $(this).removeClass('highlight_select');
            $(this).addClass('highlight');
            $(this).children().removeClass('highlight_select');
            $(this).children().addClass('highlight');
        }
        if(ID == this.currentSelection){
            $(this).removeClass('highlight');
            $(this).addClass('highlight_select');
            $(this).children().removeClass('highlight');
            $(this).children().addClass('highlight_select');
            self.Scroll('.highlight_select', '#doc1layer');
        //    console.log("doc2 filterBY", this, i, this.currentSelection, ID);
        }
    });

//    $("#"+this.currentSelection).removeClass('highlight');
//    $("#"+this.currentSelection).addClass('highlight_select');
    //$("#"+this.currentSelection).removeClass('highlight');
    //$("#"+this.currentSelection).addClass('highlight_select');
    this.previousSelection = this.currentSelection;

  //  this.slide.map.seedID = currentSelection;
    var list = eval(this.slide.seedIDs[this.currentSelection]);
    var i, j, start1, end1, start2, end2, seed_data;
    //console.log(map.seedID, list)
    for (j = 0; j<list.length; j++){
        seed_data = $.parseJSON(eval(list[j]));
        //console.log(seed_data)
        doc1seeds = seed_data[this.doc1];
        doc2seeds = seed_data[this.doc2];

        for (i = 0; i < doc1seeds.length; i++){              
            start1 = doc1seeds[i][0];
            end1 = doc1seeds[i][1];
            this.slide.map.selected[this.doc1].push([start1, end1]);
           // console.log("mapping doc1", this.slide.map.selected)//, this.doc2, start1, end1);
        }
        for (i = 0; i < doc2seeds.length; i++){              
            start2 = doc2seeds[i][0];
            end2 = doc2seeds[i][1];
            this.slide.map.selected[this.doc2].push([start2, end2]);
            //console.log("mapping doc2", this.slide.map.selected)//this.doc2, start2, end2);
        }
    }
    this.slide.map.update_required = true;
};

DocComp.prototype.Scroll = function(tag, element){
    console.log("scrolling to ", '#'+$(tag)[0].id + ' ' + tag, " -> ",tag, $(tag)[0].id, "in", this.scrolldocID);
    $(this.scrolldocID).scrollTo($('#'+$(tag)[0].id));
};


DocComp.prototype.renderLargest = function(){
  //  console.log("RENDER LARGEST");
    // Replace markers with html tags
    var highlighted_text = this.doc1_largest;
    var map_overlay = utils.handleHighlightTags(highlighted_text, this.markers);
    var doc_html = utils.lineBreaker(map_overlay, this.markers, "</br><span class='num'>", ". </span>", "</br>");

   // console.log("map overlay", map_overlay);
//    $('#doc1layer').html(map_overlay);
    $('#doc1layer').html(doc_html.replace(this.doc1_title, ""));

    var highlighted_text = this.doc2_largest; //this.replaceMarkers(this.text.doc2).replace('</span>', '');
    var map_overlay = utils.handleHighlightTags(highlighted_text, this.markers);
    var doc_html = utils.lineBreaker(map_overlay, this.markers, "<br><span class='num'>", ". </span>", "</br>");

//    $('#doc2layer').html(map_overlay);
    $('#doc2layer').html(doc_html.replace(this.doc2_title, ""));
};
