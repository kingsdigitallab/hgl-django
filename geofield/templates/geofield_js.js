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

        $(maps[i]).after(
            '<div style="height:100px;width:500px;" id="' + $(maps[i]).attr('id') + '-geosearch'  +'">' +
            '<form class="geosearch-form" id="' + $(maps[i]).attr('id') + '-geosearch-search-form' + '">' +
            '<label style="padding-left:20px;margin-bottom:20px;" for="' + $(maps[i]).attr('id') + '-geosearch-search' + ' " ' + '>Search text:   </label>' +
            '<input name="search-text" style="padding-left:20px;margin-bottom:20px;" id="' + $(maps[i]).attr('id') + '-geosearch-search' + '" type="text"></input>' +
            '<input id="' + $(maps[i]).attr('id') + 'geosearch-submit' + '" type="submit" value="Search"></input></br>' +
            '<label style="padding-left:20px;" for="' + $(maps[i]).attr('id') + '-geosearch-list' + ' " ' + '>Results:   </label>' +
            '<select style="padding-left:20px;" id="' + $(maps[i]).attr('id') + '-geosearch-list' + '" type="select">' + 
                '<option>...</option>' +
            '</select>' +
            '</form>' +
            '</div>'
        )

	// Get rid of Openlayers div
        //$( $(maps[i]).attr('id') + '_map' ).remove()


        // Set up search form:
        searchUrl = 'http://api.geonames.org/searchJSON?formatted=false&country=LY&maxRows=10&lang=en&username=hergazlib'
        // debug search param


        
       $( 'form#' + $(maps[i]).attr('id') + '-geosearch-search-form' ).on('submit', function (e){
            e.preventDefault();
            var form =  this;
            var searchText = $("input[name='search-text']",form).val()
            var searchResultsHolder = $("select",form)
            var searchMap = window[ 'map' + $('form.geosearch-form').index(this) ]

            console.log('map' + $('form.geosearch-form').index(this) )

            $.ajax({
                dataType:"json",
                url:searchUrl + '&q=' + encodeURIComponent( searchText ),
                success: function(data){
                    var options = "";
                    for (g in data.geonames){
                        options += '<option data-lng="'+ data.geonames[g].lng +'" data-lat="'+ data.geonames[g].lat +'">'+ data.geonames[g].name +'</option>'
                    }
                    $(searchResultsHolder).append(options);
                    // set event and map result
                    $(searchResultsHolder).change(function(){
                        var y = ( $(this).find('option:selected').attr('data-lng') );
                        var x = ( $(this).find('option:selected').attr('data-lat') );
                        searchMap.drawingLayer.clearLayers()
                        var layer = new L.marker([x,y])
                        searchMap.drawingLayer.addLayer(layer)
                        $(searchMap.textArea).val('SRID=4326;POINT(' + y + ' ' + x + ')' )
                        $(searchMap.latField).val(x)
                        $(searchMap.lngField).val(y)
                        getHeight(y,x,searchMap.heightField)

                    })
                }
            })
        });





        var mapDiv = $(maps[i]).prev()
        // Create each map in its respective div
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
                , 6 )
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
        		featureGroup: currDrawingLayer,
                remove: false,
                edit: false

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
            $(this.textArea).val(wkt)
            $(this.latField).val( layer.getLatLng().lat.toFixed(6) )
            $(this.lngField).val( layer.getLatLng().lng.toFixed(6) )
            var height = $(this.heightField)


            // Mapquest api key for height query
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
            })

        });
    
        $(currMap._container).prev().hide()
    
    } // end for loop

    // Get rid of OpenLayers map

    $('.olMap').remove();

});  // end doc ready


function getHeight(y,x,field){

            var key = 'oe44IrqJEqFXMrGFA1xnstp7uGgMCzSl'
            var url = 'http://open.mapquestapi.com/elevation/v1/profile?key='+ key +'&shapeFormat=json&latLngCollection='+
                x + ',' + y
            $.ajax({
                dataType:"json",
                url:url,
                success: function(data){
                    $(field).val(data.elevationProfile[0].height)   
                }
            })

}
