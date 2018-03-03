var Slider = function(){
    this.x = 0;
    this.y = 0;
    this.items = {}
    this.update_required = false;
};

Slider.prototype.Init = function(doc_comparison){
    this.doc_comparison = doc_comparison;
//    console.log("slider init", doc_comparison) 
    this.items = doc_comparison.data.largest;

    this.docID = doc_comparison.doc1;

    this.map = doc_comparison.map;

    this.value = 0;
    this.offset = 5;
    this.radius = 5;
    this.seedHTML_labels = [];
    
    this.num_seeds_by_length = this.size(this.items[this.doc_comparison.current_doc]);
    this.maximum = this.GetFields(this.items[this.doc_comparison.current_doc]);
    var field =  Object.keys(this.lengths).length-1;
    var data = this.items[this.doc_comparison.current_doc][this.maximum.toString()];  
    this.seed_length = Object.keys(this.lengths)[field];
    //console.log("Original Seed data:", this.seed_length)
    this.GetData(data);
    this.userAction(); 
    this.draw(this.seedHTML_labels, true);

};

Slider.prototype.draw = function(seed_lengths, drawlargest) {
//    console.log('draw', seed_lengths, seed_lengths[seed_lengths.length],seed_lengths.length)
    var html = '';
    html += '<li class="row">';
    html += '<a href="#" aria-label="Previous">';
    html += '<span aria-hidden="true">&laquo;</span>';
    html += '</a>';
    html += '</li>';
    for(var i=0; i < seed_lengths.length; i++){
        var seed_label = "&nbsp&nbsp"//seed_lengths[i];
        if(seed_lengths[i] == seed_lengths[seed_lengths.length-1] && drawlargest==true){
            html += '<li id="seed'+seed_lengths[i]+'" class="active" rel="' + seed_lengths[i] + '" onClick="_samtla.doc_comparison.slide.userAction(this)" style="color: transparent;"><a>' + seed_label + '</a></li>';
        } else {
            html += '<li id="seed'+seed_lengths[i]+'" rel="' + seed_lengths[i] + '" onClick="_samtla.doc_comparison.slide.userAction(this)" style="color: transparent;"><a>' + seed_label + '</a></li>';
        }
    }
    html += '<li>';
    html += '<a href="#" aria-label="Next">';
    html += '<span aria-hidden="true">&raquo;</span>';
    html += '</a>';
    html += '</li>'
    html += '</div>';

    $('#doc-title').html('<div id="slidingbar" class="pagination"></div>');
    $('#slidingbar').html(html);
};

Slider.prototype.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

Slider.prototype.Debug = function(){
    this.Init();
};

Slider.prototype.userAction = function(value){
    this.map.selected = {}
    this.previous_element = 'seed'+this.current_length;
    if(value){
        this.draw(this.seedHTML_labels);
        this.current_element = value.getAttribute('id');
        this.current_length = parseInt(value.getAttribute('rel'));
        $('#'+this.previous_element).removeClass('active');
        $('#'+this.previous_element).addClass('seed_length');
        $('#'+this.current_element).removeClass('seed_length');
        $('#'+this.current_element).addClass('active');
    } else {
        this.current_element = this.previous_element;
        $('#'+this.previous_element).removeClass('active');
        $('#'+this.previous_element).addClass('seed_length');
    }
    var data = this.items[this.doc_comparison.current_doc][this.current_length];

    this.GetData(data);
  //  console.log("slider get data for seedIDs and index", data)
    this.map.current_length = this.current_length;
    this.map.Get(this.doc_comparison.data);
    this.map.update_required = true;
    this.map.draw();
    this.draw(this.seedHTML_labels, true);
};

Slider.prototype.GetFields = function(data){
    var rnd_pointer = 0, 
        step = 5,
        intervals,
        seed_length, 
        seeds, 
        seed, 
        maximum, 
        i;

    //game.map.update_required = true;

    intervals = Object.keys(data).length
    if (intervals <= step){
        step = Object.keys(data).length
    }

    this.lengths = [];
    this.fields = {};

    this.rnd_step = Math.floor(intervals/step);
    //console.log(intervals, this.rnd_step, intervals/step)
    var maxSeed = Math.max(Object.keys(data));
    seeds = data[maxSeed];
    for (seedID in seeds){
        seed_list = eval(seeds[seedID]);
        this.lengths.push(maxSeed)//] = seed_length;      
        this.fields[maxSeed] = eval(seed_list);
    }


    for (seed_length in data){
        if(rnd_pointer % step==0){
            this.seedHTML_labels.push(seed_length);  
            seeds = data[seed_length];
            for (seedID in seeds){
                seed_list = eval(seeds[seedID]);
                this.lengths.push(seed_length)//] = seed_length;      
                this.fields[seed_length] = eval(seed_list);
               // console.log(this.fields[seed_length])
            }
        }
        rnd_pointer += 1;
     //   console.log(rnd_pointer, this.rnd_step, rnd_pointer % this.rnd_step)
    }
    maximum = 0;
    for(i in this.fields){
        maximum = i;
    }
    this.current_length = maximum;
 //   console.log("Get Fields", data, this.current_length)
    return maximum;
};

Slider.prototype.GetSeeds = function(docID, seedIDs){
    var seed_object = [];
    for(var seedID in seedIDs){
        var list = seedIDs[seedID];
      //  console.log("GET SEEDS", seedID, seedIDs, seedIDs[seedID], list)
        for (var j = 0; j < list.length; j++){
            var seed_data = JSON.parse(list[j]);
        //    console.log("seed_data", docID, seedID, seed_data, seed_data[docID].length);
//            i = 0;
            // Get doc data
            for (var i = 0; i < seed_data[docID].length; i++){              
                var start = seed_data[docID][i][0];
                var end = seed_data[docID][i][1];
                var seed = this.doc_comparison.seed.getSeedData(seedID, docID, [start, end]);

          //      console.log(docID, seedID, start, end, seed);
   //             if(end-start == this.current_length){
                    seed_object.push(seed);
    //            }
            }
        }
//        if(seedID == this.doc_comparison.currentSelection){
//            var width = this.map.data[docID].width;
//        }
    }

    //console.log("GetSeeds", docID, seedIDs, seed_object)
    return seed_object;
};

Slider.prototype.GetData = function(seedIDs){
    this.seedIDs = seedIDs;
    if(this.seedIDs){
        var doc1 = this.doc_comparison.doc1;
        var doc2 = this.doc_comparison.doc2;
        var seed_object1 = [];
        var seed_object2 = [];
        
        this.map.highlighted_sequences[doc1] = [];
        this.map.highlighted_sequences[doc2] = [];

        var seeds1 = this.GetSeeds(doc1, this.seedIDs);
        //console.log("seeds1", seeds1)         
        for (var i=0; i < seeds1.length; i++){
            var start = seeds1[i].start;
            var end = seeds1[i].end;
          //  console.log(doc1, start, end) 
            this.map.highlighted_sequences[doc1].push([start, end]);
        }
        
        var seeds2 = this.GetSeeds(doc2, this.seedIDs);
       // console.log("seeds2", seeds2)               
        for (var i=0; i < seeds2.length; i++){
            var start = seeds2[i].start;
            var end = seeds2[i].end;
            this.map.highlighted_sequences[doc2].push([start, end]);
        }
        console.log("slide getDATA",this.doc_comparison.text.doc1)
        var doc1_text = this.doc_comparison.text.doc1.text;
        var doc2_text = this.doc_comparison.text.doc2.text;
        var text1 = new Corpusline(this.doc_comparison.doc1, doc1_text, this.doc_comparison.markers);
        var text2 = new Corpusline(this.doc_comparison.doc2, doc2_text, this.doc_comparison.markers);	
         
        var sorted_seeds1 = seeds1.sort(this.doc_comparison.seed.sortSeedIdx("start"))
//        console.log('sortedSeeds', sorted_seeds1, this.doc_comparison.seed, this.doc_comparison.seed.sortSeedIdx)
        //console.log(this.doc_comparison.seed, sorted_seeds1)
        var sorted_seeds2 = seeds2.sort(this.doc_comparison.seed.sortSeedIdx("start"))
        this.snippet = new Snippet(this.doc_comparison);

        highlightdoc1 = this.snippet.Process(text1, sorted_seeds1);        
        highlightdoc2 = this.snippet.Process(text2, sorted_seeds2);
        console.log(text1)
        console.log(highlightdoc1, sorted_seeds1)

//        highlightdoc1 = utils.handleHighlightTags(highlightdoc1, this.markers);
//        highlightdoc1 = utils.lineBreaker(highlightdoc1, this.markers, "<br><span class='num'>", ". </span>", "<br>");
        
//        highlightdoc2 = utils.handleHighlightTags(highlightdoc2, this.markers);
//        highlightdoc2 = utils.lineBreaker(highlightdoc2, this.markers, "<br><span class='num'>", ". </span>", "<br>");

        $('#doc1layer').html(highlightdoc1);
        $('#doc2layer').html(highlightdoc2);
        this.map.current_length = this.current_length;
    }
};

Slider.prototype.calculateOffset = function(text, index){
    var span = new RegExp("(<\/?[^>]+>)","g");
    var linenum = new RegExp("[0-9]\. ", "g");
    var start_offset = text.slice(0, parseInt(index.start)).match(span);
    var end_offset = text.slice(0, parseInt(index.end)).match(span);
    var offset = this.calculateLength([start_offset])
    var start = index.start + offset;	 
    var offset = this.calculateLength([end_offset])
    var end = index.end + offset;
    return {start: start, end: end};
};

Slider.prototype.calculateLength = function(sequences){
    var joined = sequences.join('').toString().replace(new RegExp(",", "g"), "");
    return joined.length;
};

