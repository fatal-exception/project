var Snippet = function(document_comparison){
  this.doc_comp = document_comparison;
  this.raw_snippet = undefined;
  this.markers = this.doc_comp.markers//{line_break: "*", begin_highlight: "@", end_highlight: "$", begin_largest: "{", end_largest: "}"};

};

Snippet.prototype.Process = function(text, seeds){ 
    this.seed = new Seed(this);
    this.text = text.corpusline;
    var temp = [];
    console.log("Process: Go through seeds and highlight documents", text, seeds)
    if (seeds) {
        // Clear previous seed data and highlighting
        text.offset = 0;
        // Go through seeds and highlight documents
 	    for (var i = 0; i < seeds.length; i ++) {
  	        var seed = seeds[i];
            console.log("seed:", seed)
            if (seed.docID == text.docID){ 
		        temp.push({idx: seed.start, bracket: "{", ID: seed.ID, offset: 0})
		        temp.push({idx: seed.end, bracket: "}", ID: seed.ID, offset: 0})                
            }    
	    }
        text.corpusline = this.createSnippet(temp, text);
	    return utils.handleHighlightTags(text.corpusline, this.markers);
    }
};

Snippet.prototype.checkSnippet = function(indices, text){
    var indices = indices.sort(this.seed.sortSeedIdx("idx"));
    //console.log("checkSnippet", text)
    var tag = null;
    for(var i = 0; i < indices.length; i++){ 
        indices[i].idx = this.checkWordBoundary(indices[i], text);
    }

    var indices = indices.sort(this.seed.sortSeedIdx("idx"));
    seeds = {};
    seeds[text.docID] = [];
    for(var i = 0; i < indices.length; i++){ 
        var index = indices[i];
       // if (index.bracket == this.markers.begin_highlight){
       //     tag = '<span class="highlight" id="'+index.ID+'" onClick="_samtla.doc_comparison.getValue(this)">';
       //     text.offset += tag.length-1;
	   // } else 
	   // if (index.bracket == this.markers.end_highlight){
       //     tag = '</span>';
       //     text.offset += tag.length-1;
       // }
        if (index.bracket == this.markers.begin_largest){
            tag = '<span class="highlight" id="'+index.ID+'" onClick="_samtla.doc_comparison.getValue(this)">';
            text.offset += tag.length-1;
	    } 
	    if (index.bracket == this.markers.end_largest){
            tag = '</span>';
            text.offset += tag.length-1;
        }
     //   con
        console.log("check snippet", text.docID, index.bracket)//text.corpusline.slice(index.idx[0], index.idx[1]-index.idx));
        seeds[text.docID].push({docID: text.docID, position: index.idx, offset: text.offset, marker: tag, length: tag.length});
  //        seeds[text.docID].push({docID: text.docID, position: index.idx, offset: text.offset, marker: index.bracket, length: tag.length});
        }
    //}
    return seeds; 
};

Snippet.prototype.GetSnippet = function(seed, text){
//    console.log(seed.position)
    var beginningof = text.corpusline.slice(0, (seed.position + text.offset)) + seed.marker;   
    var endof = text.corpusline.slice((seed.position + text.offset), (text.corpusline.length + text.offset));
    text.corpusline = beginningof + endof;
    text.offset += seed.length;
    return text;
};

Snippet.prototype.createSnippet = function(indices, text){
    console.log("createSnippet", text.docID, indices, text)
    var seeds = this.checkSnippet(indices, text);
    text.offset = 0;
    var history = {};
    for(var docID in seeds){ 
        if(docID == text.docID){
            var index = seeds[docID];
            for(seed in index){
                var data = index[seed];
//                console.log(seed, data)
                text = this.GetSnippet(data, text);
            }
        } 
    }
    return text.corpusline; 
};

Snippet.prototype.checkWordBoundary = function(index, text){
    if(index.bracket == this.markers.begin_highlight){
        // Check for space left
        for (var i=index.idx; i > 0; i--){
            
            var beginning = text.corpusline.slice(i, i + 1);
            if(beginning == "."|| beginning == " "|| beginning == "*"){
                return i+1;
            }
        }
        return index.idx;        
    } 
    // Check for space right
    if(index.bracket == this.markers.end_highlight){
        var ending = text.corpusline.slice(index.idx - 1, index.idx);
//        console.log("'"+ending+"'")
        if(ending == "." || ending == " "){
            return index.idx-1;
        }
//        console.log(index, text);
        return index.idx; 
    }
};

Snippet.prototype.calculateOffset = function(text, index){
    return {start: start, end: end, offset: {start: (offset - l_start_offset), end: (l_end_offset-offset)}};
};

Snippet.prototype.calculateLength = function(sequences){
    if (sequences == null) return 0
    var joined = sequences.join('').toString().replace(new RegExp(",", "g"), "");
 //   console.log(sequences, joined.length, joined)
    return joined.length;
};

Snippet.prototype.count = function(str, value){
   var regExp = new RegExp(value, "gi");
   return str.match(regExp) ? str.match(regExp).length : 0;  
}
