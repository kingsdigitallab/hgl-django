var map;

$(document).ready(function(){
    // Create map
    map = new L.map('map', {
        center:[30.449,18.018],
        zoom: 5
    });
    // and add tiles
    //var awmc = new L.TileLayer("http://{s}.tiles.mapbox.com/v3/isawnyu.map-knmctlkh/{z}/{x}/{y}.png",{subdomains:'abcd',
    // attribution:'<a href="http://awmc.unc.edu/wordpress/">AWMC</a>'}).addTo(map)


    var ggl = new L.Google('HYBRID');

    var osm = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);


    var switcher = new L.Control.Layers({'AWMC':awmc, 'Google':ggl, 'Open Street Map':osm },{}).addTo(map) 

});
