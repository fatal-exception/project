// Stores the highlighted document
var Corpusline = function(docID, text, markers){
    this.docID = docID;
    this.corpusline = text.replace(markers.line_break, "<br>")
    this.size = text.length;
    this.offset = 0;
    this.markers = markers;
};
