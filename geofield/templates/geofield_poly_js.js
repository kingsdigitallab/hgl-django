{% load i18n %}

$(document).ready(function(){
	formHTML = 
	'<div id="geo-wrapper" style="float:left;display:block;width:10%,margin-left:20px;">'+
	'<p>Basic geocoding tools</p>'+
		'<span id="geo-fields">'+
		'<input id="geocode-string" style="display:block;margin-top:10px;" type="text"></input>'+
		'<label></label>'+
		'<input type="button"  style="display:block;margin-top:10px;" value="Sumbit search text" onclick="getPoints()"></input>'+
    	'<select id="geocode_select" style="display:block;margin-top:10px;"></select>'
		'<span>'+
	'</div>'

	$('#id_{{ geofield_js }}_admin_map').before(formHTML);
	
    $('#geocode_select').change(function(){
		centreMap(	$(this).val()	)
	})

    // Resize map:
    $('#id_{{ geofield_js }}_map').width('400px');
	
	if(typeof geodjango_geom !== 'undefined'){
		if (geodjango_geom.map.layers[1].features[0]) {
			var f = geodjango_geom.map.layers[1].features[0];
			geodjango_geom.map.zoomToExtent(f.geometry.bounds);
		}; 
	};
});

function getPoints(){
    //Clear the list
	$('#geocode_select').html('');
    var val = $('#geocode-string').val();

		//base_url = '/nominatim.openstreetmap.org/search?';
        base_url = '/geonames/';
        //base_url = 'http://api.geonames.org/searchJSON?';
		query_url = '?q='+val+'&country=CY';
		params = '&maxRows=10&callback=listPoints&username=cyprusgazetteer'
		
		url = base_url + query_url + params;
		
		$.ajax({
			url: url,
			dataType: "jsonp",
			async:true,
			jsonpCallback: "listPoints",
			jsonp: 'callback'
		});
}

function listPoints(locations){
	locationList = locations.geonames;
	$('#geocode_select').append('<option value="">...</option>');
	for (l in locationList){
		var str = locationList[l].name + ' (' + locationList[l].fclName + ', ' + locationList[l].adminName1 +')';
		var opt = l;
		$('#geocode_select').append('<option value='+l+'>'+str+'</option>');
	}
}

function centreMap(l){
	// First reproject the point
	rp = wgs84toWebmerc(parseFloat(locationList[l].lng),parseFloat(locationList[l].lat));
	// User returned value to recenter tha map
	var pnt = new OpenLayers.LonLat(
		rp.x,
		rp.y
	);
	geodjango_{{ geofield_js }}.map.setCenter(pnt,13);

	geodjango_{{ geofield_js }}.map.setCenter(pnt,12);
        geodjango_{{ geofield_js }}.map.zoomTo(14);

            $('input#id_uri').val(locationList[l].geonameId).
			after('<label>'+locationList[l].name +'</label>')
            $('input#id_lat').val(locationList[l].lat);
            $('input#id_lng').val(locationList[l].lng);

}

function wgs84toWebmerc(lon,lat){
	var world = new Proj4js.Proj('EPSG:4326');
	var webmerc = new Proj4js.Proj('EPSG:900913');
	var p = new Proj4js.Point(lon,lat);
	Proj4js.transform(world,webmerc,p);
	return p;
}