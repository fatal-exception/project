var getMouseXY = function(event, element){
    var x, y = 0;
    if (event.pageX || event.pageY) {
        x = event.pageX;
        y = event.pageY;
    } else {
        x = event.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
        y = event.clientY + document.body.scrollTop + document.documentElement.scrollTop;
    }
    //x += event.offsetX;//offsetLeft;
    //y += event.offsetY;//offsetTop;
    return {x: x, y: y};
};

if (!window.requestAnimationFrame) {
    window.requestAnimationFrame = (
	window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame ||
        window.oRequestAnimationFrame ||
        window.msRequestAnimationFrame ||
        function (callback) {return window.setTimeout(callback, 1000/60)});
};


var utils = {};
utils.mouse = {x: 0, y: 0, move: false, clicked: false, radius: 5};
var mousewheel = function (event){
    var wheel = event.wheelDelta/120;//n or -n
    var zoom = Math.pow(1 + Math.abs(wheel)/2 , wheel > 0 ? 1 : -1);
    mouse.zoom = zoom;
   // console.log(zoom)
};

var mousemove = function (event) {
    //console.log(event)
        event.preventDefault();
        var x, y;
        if (event.pageX || event.pageY) {
            x = event.pageX;
            y = event.pageY;
        } else {
            x = event.clientX + document.body.scrollLeft +
            document.documentElement.scrollLeft;
            y = event.clientY + document.body.scrollTop +
            document.documentElement.scrollTop;
        }
        x -= document.body.offsetLeft;
        y -= document.body.offsetTop;
        utils.mouse.x = x;
        utils.mouse.y = y;
        utils.mouse.move = true;
}

utils.captureMouse = function (element) {
    var mouse = {x: 0, y: 0, move: false, clicked: false, radius: 5};
    element.addEventListener('mousemove', mousemove, false);
    element.addEventListener('mousedown', 
	function (event) {
            event.preventDefault();
            mouse.clicked = true;
        }, false);
    element.addEventListener('mouseup', 
	function (event) {
            event.preventDefault();
            mouse.clicked = false;
        }, false);

    element.addEventListener('dblclick', 
	function (event) {
            event.preventDefault();
            mouse.dblclicked = true;
        }, false);

    element.addEventListener('onmousewheel', mousewheel, false);

    return mouse;
};

utils.captureKeyboard = function(element){
    keyboard = {left: false, right: false, up: false, down: false, zoomIn: false, zoomOut: false};
    window.onkeydown = function(e){
//        console.log(e.keyCode + "down");
        keyboard.keydown = true;
        keyboard.keyup = false;
        switch (e.keyCode){
        case 38:
            // up
            keyboard.up = true;
            break;
        case 40:
            //down
            keyboard.down = true;
            break;
        case 37:
            //left
            keyboard.left = true;
            break;
        case 39:
            //right
            keyboard.right = true;
            break;
        case 109:
            //- on keypad
            keyboard.zoomOut = true;
            break;
        case 189:
            //- near backspace
            keyboard.zoomOut = true;
            break;
        case 107:
            //+ on keypad
            keyboard.zoomIn = true;
            break;
        case 187:
            //+ near backspace
            keyboard.zoomIn = true;
            break;

        }
    }
    window.onkeyup = function(e){
        keyboard.keydown = false;
        keyboard.keyup = true;

        switch (e.keyCode){
        case 38:
            // up
            keyboard.up = false; 
            break;
        case 40:
            //down
            keyboard.down = false;
            break;
        case 37:
            //left
            keyboard.left = false;
            break;
        case 39:
            //right
            keyboard.right = false;
            break;
        case 109:
            //- on keypad
            keyboard.zoomOut = false;
            break;
        case 189:
            //- near backspace
            keyboard.zoomOut = false;
            break;
        case 107:
            //+ on keypad
            keyboard.zoomIn = false;
            break;
        case 187:
            //+ near backspace
            keyboard.zoomIn = false;
            break;

        }
    }
   return keyboard;
};

utils.captureTouch = function (element) {
    var touch = {x: null, y: null, isPressed: false};
    element.addEventListener('touchstart', 
        function (event) {
            touch.isPressed = true;
        }, false);
    element.addEventListener('touchend', 
        function (event) {
            touch.isPressed = false;
            touch.x = null;
            touch.y = null;
        }, false);
    element.addEventListener('touchmove', 
        function (event) {
            var x, y,
            touch_event = event.touches[0]; //first touch
            if (touch_event.pageX || touch_event.pageY) {
                x = touch_event.pageX;
                y = touch_event.pageY;
            } else {
                x = touch_event.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
                y = touch_event.clientY + document.body.scrollTop + document.documentElement.scrollTop;
            }
            x -= offsetLeft;
            y -= offsetTop;
            touch.x = x;
            touch.y = y;
        }, false);
    return touch;
};

utils.distanceFrom = function(objectA, objectB){
    var dx = objectB.x - objectA.x;
    var dy = objectB.y - objectA.y;
    dist = Math.sqrt(dx * dx + dy * dy);
    return {dx: dx, dy: dy, dist:dist};    
};

utils.checkCollision = function(position, button, scale){
    if(position.x > button.x / scale && position.x < button.x / scale + button.width / scale){
        if(position.y > button.y / scale && position.y < button.y / scale + button.height / scale){
	    return true;
        }  
    }
};

utils.detectCollision = function(objectA, objectB){
    dist = this.distanceFrom(objectA, objectB);
    if (dist < objectA.radius + objectB.radius) {
	return true;
    } else {
	return false;
    }
};

utils.isEmpty = function(ob){
   for(var i in ob){ return false;}
  return true;
}

utils.Sort = function(ob){
    ob.sort(function(a, b){return a[0] - b[0];})
    return ob;
};
utils.SortArray = function(ob){
    ob.sort(function(a, b){return a - b;})
    return ob;
};

utils.SortDesc = function(ob){
    ob.sort(function(a, b){return b - a;})
    return ob;
};

utils.getUserSelection = function(element){
    var start = element.selectionStart;
    var end = element.selectionEnd;
    return {start: start, end: end};
};

utils.calculateOffset = function(docID, text, mouse) {
    // Calculate the offer between where the user clicked and the actual idx caused by addition of line numbers. 
    var pattern = /\d+\. /g;
    var start_offset = text.slice(0, parseInt(mouse.start)).match(pattern);
    var end_offset = text.slice(0, parseInt(mouse.end)).match(pattern);
//    console.log("Mouse", mouse.start, mouse.end)

    if (start_offset){
        var offset = start_offset.join('').length
	var start = mouse.start - offset;	 
    } else {
        var start = mouse.start;
    }
    if(end_offset){
        var offset = start_offset.join('').length
	var end = mouse.end - offset;
    } else {
        var end = mouse.end;
    }
    return {start: start, end: end};
};

utils.lineBreaker = function(text, marker, replace_startwith, replace_endwith){
    // divides up the text and inserts line numbers for TextArea and HTML.
//    console.log("LINEBREAKER")
    var lines = "";
    var n = 1;
    var textarray = text.split(marker.line_break);
    for (var i = 0; i < textarray.length; i++) {
        if (textarray[i].length == 0){continue} 
    	lines += replace_startwith + (n) + replace_endwith + textarray[i];
        n += 1;
    }
    return lines//text.replace('*', '<br>')//linebreak).trim();
};

utils.handleHighlightTags = function(html, marker){
    //console.log('utils.handlehighlights', html) 
    // Replace the place holding tags with html markup.
    html = html.replace(new RegExp(marker.begin_largest, "g"), "<span class='highlight'>");
    html = html.replace(new RegExp(marker.end_largest, "g"), "</span>");


    html = html.replace(new RegExp(marker.begin_highlight, "g"), "<span class='highlight'>");
    html = html.replace(new RegExp(marker.end_highlight, "g"), "</span>");
  //  console.log("highlighted result", html, marker.begin_longest, marker.end_longest)
    html = utils.lineBreaker(html, marker, "<br><br><span class='num'>", ". </span>");
//    html = utils.lineBreaker(html, marker, "", ". ", "");
    //html = html.replace('*', '<br>');
    
    return html.trim().replace(/\*/g, '</br></br>');
};

	//Select and submit to query bar after removing line numbers etc.
utils.selectText = function(){
    var query = document.getElementById('query');
    var match = new RegExp('[0-9]+\.', "igm"); 
    if (window.getSelection){
	query.value = window.getSelection().toString().replace(match, '');
    } else if (document.getSelection){
        query.value = document.getSelection();
    } else if (document.selection){
	query.value = document.selection.createRange().text;
    }
};

utils.Timer = function(dt, counter, rate){
    if(counter > 0){
        counter -= rate; 
        return counter;
    } else {  
        return 0;
    }  
};

utils.resetTimer = function(counter, totaltime){
    counter = totaltime;
};

utils.localStorage = function() {
  try {
    return 'localStorage' in window && window['localStorage'] !== null;
  } catch (e) {
    return false;
  }
};

utils.sortByKey = function(array, key, type){
    return array.sort(function(a, b) {
        var x = a[key]; 
        var y = b[key];
        if(type=='descending'){ 
            return ((x < y) ? 1 : ((x > y) ? -1 : 0));
        } else {
            return ((x < y) ? -1 : ((x > y) ? 1 : 0));
        }
    });
};

Number.prototype.roundTo = function(to) {
    return Math.round(this / to) * to;
}

utils.resizeFont = function(box){
$(box).each(function ( i, box ) {
    var width = $( box ).width(),
        html = '<span style="white-space:nowrap"></span>',
        line = $( box ).wrapInner( html ).children()[ 0 ],
        n = 100;

    $( box ).css( 'font-size', n );

    while ( $( line ).width() > width ) {
        $( box ).css( 'font-size', --n );
    }

    $( box ).text( $( line ).text() );

});

};

utils.intersects = function (rectA, rectB, zoom) {
//  console.log("intersects", rectA, rectB); 
  return !((rectA.x * zoom) + (rectA.width * zoom) < (rectB.x * zoom)  ||
           (rectB.x * zoom) + (rectB.width * zoom) < (rectA.x * zoom)  ||
           (rectA.y * zoom) + (rectA.height * zoom) < (rectB.y * zoom) ||
           (rectB.y * zoom) + (rectB.height * zoom) < (rectA.y * zoom));
};


String.prototype.toTitleCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};
function uniq(a) {
    var seen = {};
    return a.filter(function(item) {
        return seen.hasOwnProperty(item) ? false : (seen[item] = true);
    });
}
function intersection_destructive(a, b)
{
  var result = [];
  while( a.length > 0 && b.length > 0 )
  {  
     if      (a[0] < b[0] ){ a.shift(); }
     else if (a[0] > b[0] ){ b.shift(); }
     else /* they're equal */
     {
       result.push(a.shift());
       b.shift();
     }
  }

  return result;
}
