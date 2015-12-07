var map;

$(document).ready(function(){
    // Create map
    map = new L.map('map', {
        center:[30.449,18.018],
        zoom: 5
    });
    // and add tiles
    var awmc = new L.TileLayer("http://{s}.tiles.mapbox.com/v3/isawnyu.map-knmctlkh/{z}/{x}/{y}.png",{subdomains:'abcd'}).addTo(map)
});