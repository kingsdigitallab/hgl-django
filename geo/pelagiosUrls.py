from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    (r'^downloads/json/dump.js','geo.pelagiosViews.json_dump'),
    (r'^downloads/json/(\d+).js','geo.pelagiosViews.individual_json_dump'),
)
