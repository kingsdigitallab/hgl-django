 var map;
clusterLayer = new L.markerClusterGroup();
//var clusterLayer;
        //$(document).ready(function () {



        //})

        function loadMarkers(){
             map.spin(true);
            console.log(map);

            $.ajax(SCRIPT_URL+'map/?'+QUERY_STRING+'&page=1&mime_type=application/text',
                {
                    success: function (data) {
                        const geoMarkers = JSON.parse(data);
                        mapResult(geoMarkers, clusterLayer);
                        map.addLayer(clusterLayer);
                        map.spin(false);
                    }
                }
            );
        }

        function mapResult(geojson, clusterLayer) {
            g = new L.geoJson(geojson, {
                pointToLayer(f, ll) {
                    var mkr = new L.marker(ll);
                    mkr.on('click', function () {
                        $.ajax('/irt_geo/popupcontent/?id=' + f.properties.id, {
                            success: function (data) {
                                mkr.bindPopup(data).openPopup();
                            }
                        }); // end ajax
                    });
                    //clusterLayer.addLayer(mkr);
                    return mkr;
                }
            }).addTo(clusterLayer);

        }

$(document).ready(function(){
    // Create map
    map = new L.map('map');
    // and add tiles
    //var awmc = new L.TileLayer("http://{s}.tiles.mapbox.com/v3/isawnyu.map-knmctlkh/{z}/{x}/{y}.png",{subdomains:'abcd',
    // attribution:'<a href="http://awmc.unc.edu/wordpress/">AWMC</a>'}).addTo(map)


    var ofm = hglOpenFreeMapLayer().addTo(map);
    map.whenReady(loadMarkers);
    map.setView([30.449,18.018], 5);

});
