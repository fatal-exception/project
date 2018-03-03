var googlemap = null;

function getGoogleMap(NER, latlong){

    var coords = latlong.split(':');
    var mapOptions = {
            zoom: 5,
            mapTypeControl: false,
            mapTypeControlOptions: {
                style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
            },
            zoomControl: true,
            zoomControlOptions: {
                style: google.maps.ZoomControlStyle.SMALL
            },
            disableDefaultUI: true
        };
    var map = window._samtla.settings['map']//new google.maps.Map(document.getElementById('google_map'), mapOptions)
    console.log("GOOGLE MAP", google,NER, latlong, coords, map)

   // console.log(NER, window._samtla.data['KML'])
//    coords = latlong.split(':')
    for (var loc in window._samtla.data['KML']){

        var title_bar = loc.charAt(0).toUpperCase() + loc.slice(1, loc.length);
        var coords = window._samtla.data['KML'][loc].split(':'); 
        console.log(loc, coords)
        if (coords.length < 1){
            var lat = parseFloat(coords[1]), 
                long = parseFloat(coords[0]);
            var myLatlng = new google.maps.LatLng(long, lat);   
 
            var contentString = ""//title_bar
            console.log(coords, lat, long, contentString) 
            if (loc != location){ 
                marker_img = 'red_dot.png';
            } else {
                marker_img = 'green_dot.png';    
                map.setCenter(myLatlng); 
            }
            var marker = new google.maps.Marker({position: {lat: lat, lng: long}});
            marker.setMap(map);
            console.log(map)
        createMarker({map: map, coord: myLatlng, img: iconBase + marker_img, title: title_bar, contentString: contentString});
        }
    }

    return map    
};

function hideGoogleMap(){
    console.log("hide google map - TBA")
};

function createMarker(obj){
    var marker = new google.maps.Marker({
        position: obj.coord,
        map: obj.map,
        title: obj.title,
        icon: obj.img
    });
    var contentString = '<div id="content">'+
        '<p>' + obj.title + '</p>' + 
        '</div>';
    var infowindow = new google.maps.InfoWindow({
        content: obj.contentString
    });
    marker.addListener('click', function() {
        infowindow.open(obj.map, marker);
    });
};
