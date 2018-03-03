var Seed = function(doc_comparison){
    this.doc_comparison = doc_comparison;
    //console.log("Seed object", doc_comparison)
    this.seedIDs = this.doc_comparison.seedIDs;
    this.index = this.doc_comparison.index;

};

Seed.prototype.getSeedData = function(seedID, docID, data){
    // Pull back the data from the Seed object.
    var doc = docID,
        start = data[0]
        end = data[1],
        ID = seedID;
   // console.log(data, {docID: doc, start: start, end: end, ID: ID, length: end-start})
    return {docID: doc, start: start, end: end, ID: ID, length: end-start};
};

Seed.prototype.sortSeedIdx = function(property){
    //console.log("sortseedIDx", prop)
    return function (a, b){
    	return (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
    }
};

Seed.prototype.getLargestSeeds = function(docID, data, text){
    var seedIDs = [], 
        seedID,
        first_seedID,
        seedlength,
        seed_data,
        seed_object,
        ID,
        single_seed,
        largest_seed,
        seed = undefined;

    if(data){
        this.slider_range = [];

        this.largest_seedIDX = {};
        
        // Get length of largest seeds
        for(seedlength in data){
              this.slider_range.push(parseInt(seedlength));
        }
//        var largest_seed_length = seedlength;  
        // filter data for the largest seed of them all
        data = data[seedlength];
  	    // Stores the longest seed data
        for (seedID in data){
            seedIDs.push(seedID);
        }
        // starting seed for largest preview
        first_seedID = seedIDs[0];
        this.largestseedID = first_seedID;
        if (data == undefined){
            return false;
        } else {

            var firstID = data[first_seedID];
            seed_data = JSON.parse(firstID);
        }
        //console.log("seedIDs - getLargestSeeds (seed.js)", data[first_seedID], data, seedIDs, seedlength, first_seedID, seed_data); 

      //  console.log("seed data", seed_data);

        seed_object = [];
        if(seed_data){
            for(ID in seed_data){ // change to for var docID in seed_data
              //  console.log("ID", seed_data, ID, seed_data[ID])
                if(ID == docID){
                    for (var j=0; j<seed_data[ID].length; j++){
                        single_seed = this.getSeedData(first_seedID, docID, seed_data[ID][j]);
                        seed_object.push(single_seed);
                    }
                }
            }
        }
        largest_seed = seed_object[0]//this.checkWordBoundary(seed_object, text)[0];
        //console.log("render largest", largest_seed, seed_object) 
        var beginning = text.corpusline.slice(0, largest_seed.start) + this.doc_comparison.markers.begin_largest,
            middle = text.corpusline.slice(largest_seed.start, largest_seed.end) + this.doc_comparison.markers.end_largest,
            end = text.corpusline.slice(largest_seed.end, text.size),
            snippet = beginning + middle + end;
//        console.log("largest snippet", seed_object, largest_seed, snippet)
        return snippet; 
    }
};

Seed.prototype.checkWordBoundary = function(largest_seed, text){
//        console.log("largest seed", largest_seed)
        for (var i=largest_seed.start; i>0; i--){
            var beginning = text.corpusline.slice(i, i + 1);
            if(beginning == " "){ 
                largest_seed.start = i+1;
                break
            }
        }
        for (var i=largest_seed.end; i<largest_seed.end + 30; i++){
            var ending = text.corpusline.slice(i, i + 1);
            if(ending == " "){
                largest_seed.end = i-1;
                break
            }
        }
        return largest_seed;
};

