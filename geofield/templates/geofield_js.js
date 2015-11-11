{% load i18n %}

// Alias jquery to standard
$ = grp.jQuery;


// Alias jquery to standard
$ = grp.jQuery;

var maps = [];

$(document).ready(function(){
    maps = $("[id*={{ geofield_js }}-")
        .filter( 
            function() { return this.id.match(/[0-9]/) }
         )
        .filter('textarea')
    
    for (i=0;i< maps.length;i++){
        //Create map for each point and remove the texarea
        $(maps[i]).before(
            '<div style="height:250px;width:500px;" id="' + $(maps[i]).attr('id') + '-map'  +'">' +
            'Map to go here' +
            '</div>'
        );
        var mapDiv = $(maps[i]).prev()
        window['map' + i.toString() ] = new L.map( mapDiv.attr('id') ).setView([28.767659, 20.65429], 4);
        currMap = window['map' + i.toString() ]
        
	// Parse the point field wkt
        if ( $(maps[i]).html() != '' ){
            var marker = omnivore.wkt.parse( $(maps[i]).html() ).addTo(currMap)
            currMap.setView( [ 
                marker.getBounds()._southWest.lat, 
                marker.getBounds()._southWest.lng ]
                , 13 )
        }

        // Add mapquest layer
        L.tileLayer('http://{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpg', {
            attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png">',
            maxZoom: 18,
            subdomains:['otile1','otile2','otile3','otile4']
        }).addTo(currMap);        

        // Add a draw control
	window["drawnItems"+ i.toString()] = new L.FeatureGroup();
        currDrawingLayer = window["drawnItems"+ i.toString()]
	currMap.addLayer(currDrawingLayer);

	options = {
    		position: 'topright',
    		draw: {
        		polygon:  false ,
        		polyline:  false ,
        		circle :  false ,
        	rectangle:  false 
    		},
    		edit : {
        		featureGroup: currDrawingLayer
    		}
	}


	// Initialise the draw control and pass it the FeatureGroup of editable layers
	window["drawControl" + i.toString ] = new L.Control.Draw(
		options
	);

        currDrawControl = window["drawControl" + i.toString ]

	currMap.addControl(currDrawControl);
        
        $(maps[i]).hide()
    }
});
