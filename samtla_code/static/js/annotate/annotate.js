   (function( _samtla, undefined ) {
        _samtla.settings = {};
        _samtla.load_settings = function(objName){
            if(localStorage && localStorage[objName]){
                var row = localStorage[objName].split(','),
                attr = row[0],
                val = row[1];
                $(objName).css(attr, val);
                return [objName, attr, val];
            }   
//            document.getElementById('filename').addEventlistener('change', _samtla.upload);
        };

        _samtla.save_settings = function(objName, attr){
            if(localStorage){
                localStorage[objName] = attr + "," + $(objName).css(attr); 
            }
        };

        _samtla.upload = function(self){
                var file = self.files[0];
                console.log("file:", file)
                if (file){
                    var r = new FileReader();
                    r.onload = function(e) {
                        console.log(e)
                        document.getElementById('document').textContent = this.result;
                        //var form = document.getElementById('fileupload');
                        //form.submit();
                        $.getJSON('/annotate_upload', {
                            myfile: this.result,
                            filename: file.name,
                            async: true,          
                        }, function(data){
                            console.log("fileuploaded", data)
                        });
                    }
                }
                //var blob = file.slice(0, file.size);
                r.readAsText(file); 
            //}
        };

        _samtla.annotate = function(){
            text = document.getElementById('document').textContent;
            console.log("text", text)
            $.getJSON('/annotateNER', {
                text: text.replace('\n', ''),
                async: true,          
            }, (function(){
               return function(data) {
                   console.log("NERs", data)
                   document.getElementById('document').innerHTML = data.html;
                   var index = JSON.parse(data.idx); 
                   var html = "";
                   for (var type in index){
                       html += '<li class="dropdown">';
					   html += '<a href="#" class="dropdown-toggle">';
						
					   html += '<span class="hidden-xs"><i></i>' + type + '</span>';
				       html += '</a>';
             
     			       html += '<ul class="dropdown-menu">';
                       for (var ner in index[type]){
                           html += '<li class="drop-down-menu">' + ner + '</li>';
                           console.log(type, ner)
                       }
     			       html += '</ul>';
     			       html += '</li>';               
                   }
                   console.log("HTML", html);
                   document.getElementById('NER-menu').innerHTML = html;
                   document.getElementById('output').innerHTML = data.idx.toString();
               };
           }())
        );
        return false;
        };


    function replaceAll(str, find, replacewith) {
        return str.replace('/'+find+'/g', replacewith)//);
    };

    function sortranks(ob){
        ob.sort(function(a, b){return parseInt(a[0]) - parseInt(b[0]);})
        return ob;
    };
    
    }( window._samtla = window._samtla || {} ) );
