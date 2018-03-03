var TreemapUtils={};

function propertyFromStylesheet(selector, attribute) {
    var value;
    [].some.call(document.styleSheets, function (sheet) {
        return [].some.call(sheet.rules, function (rule) {
            if (selector === rule.selectorText) {
                return [].some.call(rule.style, function (style) {
                    if (attribute === style) {
                        value = rule.style.getPropertyValue(attribute);
                        return true;
                    }

                    return false;
                });
            }

            return false;
        });
    });
    //console.log("value", typeof(value))
    return value.replace(' ','').replace('rgba(','').replace('rgb(','').replace(' )','').replace(')','').split(',');
};

TreemapUtils.squarify = function(rect,  vals) {
    //console.log("squarify", rect, vals)
    var Subrectangle = function(rect) {
        this.setX = function(x) {
            rect[2] -= x - rect[0];
            rect[0] = x;
        };
        this.setY = function(y) {
            rect[3] -= y - rect[1];
            rect[1] = y;
        };
        this.getX = function() {
            return rect[0];
        };
        this.getY = function() {
            return rect[1];
        };
        this.getW = function() {
            return rect[2];
        };
        this.getH = function() {
            return rect[3];
        };
        this.getWidth = function() {
            return Math.min(rect[2],rect[3]);
        };
    };
    //
    // The function worst() gives the highest aspect ratio of a list 
    // of rectangles, given the length of the side along which they are to
    // be laid out.
    // Let a list of areas R be given and let s be their total sum. Then the function worst is
    // defined by:
    // worst(R,w) = max(max(w^2r=s^2; s^2=(w^2r)))
    //              for all r in R 
    // Since one term is increasing in r and the other is decreasing, this is equal to
    //              max(w^2r+=(s^2); s^2=(w^2r-))
    // where r+ and r- are the maximum and minimum of R. 
    // Hence, the current maximum and minimum of the row that is being laid out.
    // 
    var worst = function(r,w) {
        var rMax = Math.max.apply(null,r);
        var rMin = Math.min.apply(null,r);
        var s = TreemapUtils.sumArray(r);
        var sSqr = s*s;
        var wSqr = w*w;
        //console.log(Math.max((wSqr*rMax)/sSqr,sSqr/(wSqr*rMin)), [wSqr,rMax,sSqr,sSqr,wSqr,rMin]) 
        return Math.max((wSqr*rMax)/sSqr,sSqr/(wSqr*rMin));
    };

    // Take row of values and calculate the set of rectangles 
    // that will fit in the current subrectangle.
    var layoutrow = function(row) {
        var x = subrect.getX(),
            y = subrect.getY(),
            maxX = x + subrect.getW(),
            maxY = y + subrect.getH(),
            rowHeight,
            i,
            w;       
//        console.log("layout", x, y, maxX, maxY, subrect.getW(),subrect.getH())   
        if (subrect.getW() < subrect.getH()) {
            rowHeight = Math.ceil(TreemapUtils.sumArray(row)/subrect.getW());
            //console.log('ceil', rowHeight) 
            if (y+rowHeight >= maxY) { rowHeight = maxY-y; }
            for (i = 0; i < row.length; i++) {
                w = Math.ceil(row[i]/rowHeight);
                if (x+w > maxX || i+1 === row.length) { w = maxX-x; }
                layout.push([x,y,w,rowHeight]);
                x = (x+w);
                //console.log(rowHeight, maxY, row[i], y, Math.ceil(row[i]/rowHeight))
            }
            subrect.setY(y+rowHeight);
        } else {
            rowHeight = Math.ceil(TreemapUtils.sumArray(row)/subrect.getH());
            if (x+rowHeight >= maxX) { rowHeight = maxX-x; }
            for (i = 0; i < row.length; i++) {
                w = Math.ceil(row[i]/rowHeight);
  //              console.log("w ceiling", w)
                if (y+w > maxY || i+1 === row.length) { w = maxY-y; }
                layout.push([x,y,rowHeight,w]);
                y = (y+w);
            }
            subrect.setX(x+rowHeight);
        }
        //console.log(x, y, rowHeight, w)
    };

    // Pull values from input array until the aspect ratio of rectangles in row
    // under construction degrades.
    var buildRow = function(children) {
        var row = [];
        row.push(children.shift()); // descending input
        //row.push(children.pop()); // ascending input
        if (children.length === 0) {
            return row;
        }
    //    console.log("build row childred", children)       
        var newRow = row.slice();

        var w = subrect.getWidth();
        do {
            newRow.push(children[0]); // descending input
      //  console.log(newRow)
            //newRow.push(children[children.length-1]); // ascending input
            if (worst(row,w) > worst(newRow,w)){
                row = newRow.slice();
                children.shift(); // descending input
                //children.pop(); // ascending input
            }
            else {
                break;
            }
        } while (children.length > 0);
        return row;
    };

    // Non recursive version of Bruls, Huizing and van Wijk
    // squarify layout algorithim.
    // While values exist in input array, make a row with good aspect
    // ratios for its values then caclulate the row's geometry, repeat.
    var nrSquarify = function(children) {
        do {
            layoutrow(buildRow(children));
        } while (children.length > 0);
    };

    var row = [];
    var layout = [];
    var newVals = [];
    var i;

    // if either height or width of containing rect are <= 0 simply copy containing rect to layout rects
    if (rect[2] <= 0 || rect[3] <= 0) {
        for (i = 0; i < vals.length; i++) {
        //    console.log("slicing", rect.slice())
            layout.push(rect.slice());
        }
    } else { // else compute squarified layout
        // vals come in normalized. convert them here to make them relative to containing rect
        newVals = vals.map(function(item){return item*(rect[2]*rect[3]);}); 
  //      console.log(vals, newVals)
        //console.log(newVals)
        var subrect = new Subrectangle(rect.slice());
        nrSquarify(newVals);
    }
    this.layout = layout
    return layout;
};

TreemapUtils.sumArray = (function() {
    // Use one adding function rather than create a new one each
    // time sumArray is called.
    function add(a,b) {
        return a + b;
    }
    return function(arr) {
        return arr.reduce(add);
    };
}());

var Tree = function(){

};

Tree.prototype.getRatio = function(total, num_elements, ratios){
    if(num_elements==1){
        return [0.5];
    }

///    console.log(total, num_elements, ratios)
    var temp = [], total_ratio = 0;
    for (var n=0; n < ratios.length; n++){
        e = (1/num_elements);
        r = ratios[n]//total;
        ratio = (e + r)//2
        total_ratio += ratio 
        temp.push(ratio);
    }
   /// console.log(total, num_elements, ratios, temp)
    return temp;
};

Tree.prototype.interpColour = function(start, end, steps, count){
    return start + (((end - start) / steps) * count);
};

Tree.prototype.draw = function(response, current_colour){
    var ratios = [], callbacks = [];
    var total = 0;
    var paths = response[0];
    var tree_data = response[1];
    var colourdata = response[2];

    this.data = []
    for (var t in tree_data){
         var cell_data = tree_data[t];
//    console.log("celldata",cell_data)         
         var item = cell_data[0];
         var description = getPreview(cell_data[3], 30);  
         var path = paths + "," + item;
         var func = 'browse("' + escape(path) + '","#result")';
         var row = cell_data[3][0].split('-');  
         if (row[0] == "getDocument"){
             //console.log("getDocument!",row, row[1], row[2])
             $("html, body").animate({ scrollTop: 0 }, "fast");
             description = "";
             var docID = escape(row[1])// +'-'+ row[2]);
             console.log("browseDocument", docID, row)
             _samtla.settings.current_document = docID;
             func = 'browseDocument('+docID+')';
         }    
         var count = parseInt(cell_data[1]);
         total += 1;

         this.data.push([item, description, cell_data[3].length]);
         callbacks.push(func);
         ratios.push(count);
         //console.log("item", item, count, total)
    }
    var num_elements = (this.data != undefined) ? this.data.length : 0;
    this.x = 0;
    this.y = 0;
    this.doc_width = parseInt($('#result').css('width'));
    this.doc_height = Math.abs(parseInt($('body').css('height'))-50)//-parseInt($(window).height()));
    if (num_elements > 100){
        _samtla.setBrowserType();
        return;
    }
    var ratios = this.getRatio(total, num_elements, ratios);
    var layout = TreemapUtils.squarify([this.x, this.y, this.doc_width, this.doc_height], ratios);
//    console.log([this.x, this.y, this.doc_width, this.doc_height], total, num_elements, ratios)

    //var start_r = parseInt(rgb[0]);
    //var start_g = parseInt(rgb[1]);
    //var start_b = parseInt(rgb[2]);
    var data_size = this.data.length;
    this.html = ""//'<div id="grid" style="position: absolute; top:0px;left:0px;z-index: -1;height: '+(this.doc_height)+'px; width: '+this.doc_width+'px;">';
    for(var i = 0; i < data_size; i++){
        var img = ""//data[i].img,
            title = this.data[i][0],
            preview = this.data[i][1].toTitleCase(),
            callback = callbacks[i],
            total_items = this.data[i][2];
            cell = {};

      //      r = parseInt(this.interpColour(start_r, 255, 20, ratios[i])),
        //    g = parseInt(this.interpColour(start_g, 255, 20, ratios[i])),
          //  b = parseInt(this.interpColour(start_b, 255, 20, ratios[i]));   
            console.log("get colour",current_colour, title, window._samtla.settings['palette'][title])
            if (window._samtla.settings['palette'][title] != undefined){
                r = colourdata[title][0];
                g = colourdata[title][1];
                b = colourdata[title][2];
                cell.colour = "rgba(" + r + "," + g + "," + b + ",0.3)";
                
            } else {
 
            if(current_colour !=undefined){
                r = colourdata[title][0];
                g = colourdata[title][1];
                b = colourdata[title][2];
                cell.colour = "rgba(" + r + "," + g + "," + b + ",0.3)";

            } else {
                cell.colour = 'white';
            }
            }
            cell.x = layout[i][0];
            cell.y = layout[i][1];
            cell.width = layout[i][2];
            cell.height = layout[i][3];
       // console.log(cell.colour)
        if (data_size <= 1){
            cell.width = parseInt($('#content').width());
        }

        this.html += '<div class="alert alert-info" title="' + title + '" style="overflow: hidden;text-overflow: ellipsis; position: absolute; z-index: -1;left:'+cell.x+'px; top:'+cell.y+'px; width:'+(cell.width)+'px; height:'+cell.height+'px; color:#000; background-color: ' + cell.colour + ';" rel="'+i+'" onclick='+callback+' >';
        this.html += '<span class="cell-title" style="width:'+cell.width+'px; word-wrap: break-word; overflow-wrap: break-word;text-overflow: ellipsis; position:relative; font-size:1.5em;">' + img + '' + title.toTitleCase() + '</span>';

        
        this.html += '<div style="width:'+(cell.width*0.9)+'px;font-size:1em;word-wrap: break-word;overflow-wrap: break-word;"><p>'+preview+'</p></div>('+total_items+' items)</div>';

        this.card = '<span title="' + title + '" style="position: absolute; z-index: -1;left:'+cell.x+'px; top:'+cell.y+'px; width:'+(cell.width)+'px; height:'+(cell.height)+'px;"  rel="'+i+'" onclick='+callback+'>';
        this.card += '<div class="card-block">';
        this.card += '<h4 class="card-title">' + title.toTitleCase() + '</h4>';
        this.card += '<p class="card-text" style="text-overflow: ellipsis;">'+preview.replace(/\, +/g, '<br>')+'</p>';
        this.card += '</div>';
        this.card += '</span>';

    }
    //this.html += this.card;
    //this.html += '</div>';
    return this.html;
};
