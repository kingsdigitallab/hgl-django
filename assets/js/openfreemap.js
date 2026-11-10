// OpenFreeMap base layer for Leaflet (vector tiles rendered via MapLibre GL).
// Requires (in order): Leaflet >= 1.x, maplibre-gl.js, leaflet-maplibre-gl.js.
// https://openfreemap.org/quick_start/
window.hglOpenFreeMapLayer = function () {
    var layer = L.maplibreGL({
        style: 'https://tiles.openfreemap.org/styles/liberty',
        attribution: '<a href="https://openfreemap.org" target="_blank" rel="noopener">OpenFreeMap</a> ' +
            '&copy; <a href="https://www.openmaptiles.org/" target="_blank" rel="noopener">OpenMapTiles</a> ' +
            'Data from <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'
    });
    // Unlike a raster L.TileLayer, this layer gives the map no zoom limits, so
    // map.getMaxZoom() is Infinity and Leaflet.markercluster throws
    // "Map has no maxZoom specified". Keep the old OSM tile layer's limit (18).
    layer.on('add', function () {
        if (this._map && this._map.options.maxZoom === undefined) {
            this._map.setMaxZoom(18);
        }
    });
    return layer;
};
