{% load i18n %}

// Alias jquery to standard
$ = grp.jQuery;


// Alias jquery to standard
$ = grp.jQuery;

var maps = [];

$(document).ready(function(){
    // Find all the map textareas that hold the WKT repr of the geometry
    maps = $("[id*={{ geofield_js }}-")
        .filter( 
            function() { return this.id.match(/[0-9]/) }
         )
        .filter('textarea')
    //Insert a DIV before each one to contain the leaflet map
    for (i=0;i< maps.length;i++){
        //Create map for each point and remove the texarea
        $(maps[i]).before(
            '<div style="height:250px;width:500px;" id="' + $(maps[i]).attr('id') + '-map'  +'">' +
            'Map to go here' +
            '</div>'
        );
        var mapDiv = $(maps[i]).prev()
        // Create each map
        window['map' + i.toString() ] = new L.map( mapDiv.attr('id') ).setView([28.767659, 20.65429], 4);
        var currMap = window['map' + i.toString() ]
        
        // Add mapquest layer
        L.tileLayer('http://{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpg', {
            attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png">',
            maxZoom: 18,
            subdomains:['otile1','otile2','otile3','otile4']
        }).addTo(currMap);        

        // Add a draw control
	    window["drawnItems"+ i.toString()] = new L.FeatureGroup();
        var currDrawingLayer = window["drawnItems"+ i.toString()]
	    currMap.addLayer(window["drawnItems"+ i.toString()]);

        // Parse the point field wkt
        if ( $(maps[i]).html() != '' ){
            var marker = omnivore.wkt.parse( $(maps[i]).html() ).addTo(currDrawingLayer)
            currMap.setView( [ 
                marker.getBounds()._southWest.lat, 
                marker.getBounds()._southWest.lng ]
                , 13 )
        }        

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
	window["drawControl" + i.toString() ] = new L.Control.Draw(
		options
	);

    var currDrawControl = window["drawControl" + i.toString() ]
	currMap.addControl(currDrawControl);

    currMap.drawingLayer = currDrawingLayer;
    currMap.textArea = maps[i]
    currMap.latField = $('#id_locus_coordinate-' + i + '-latitude')
    currMap.lngField = $('#id_locus_coordinate-' + i + '-longitude')
    
    currMap.heightField = $('#id_locus_coordinate-' + i + '-height')

    currMap.on('draw:created', function (e) {
        this.drawingLayer.clearLayers();
        var type = e.layerType,
            layer = e.layer;
            if (type === 'marker') {
            // Do marker specific actions
            }
            // Do whatever else you need to. (save to db, add to map etc)
            this.drawingLayer.addLayer(layer);

            var wkt = 'SRID=4326;POINT(' + layer.getLatLng().lng.toString() + ' ' +  layer.getLatLng().lat.toString() + ')'
            console.log(wkt)
            $(this.textArea).val(wkt)
            $(this.latField).val( layer.getLatLng().lat.toFixed(6) )
            $(this.lngField).val( layer.getLatLng().lng.toFixed(6) )
            var height = $(this.heightField)

            var key = 'oe44IrqJEqFXMrGFA1xnstp7uGgMCzSl'

            var url = 'http://open.mapquestapi.com/elevation/v1/profile?key='+ key +'&shapeFormat=json&latLngCollection='+
            layer.getLatLng().lat.toFixed(6).toString() + ',' + layer.getLatLng().lng.toFixed(6).toString()

            $.ajax({
                dataType:"json",
                url:url,
                success: function(data){
                    data.elevationProfile[0].height
                    $(height).val( data.elevationProfile[0].height )
                    }
                }
            )

    });



    
    // For debugging
    $(maps[i]).show()
    
    }

    // Get rid of OpenLayers map
    
    $('.olMap').remove();
});
