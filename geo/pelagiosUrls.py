from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    (r'^downloads/json/dump.json','geo.pelagiosViews.json_dump'),
    (r'^downloads/json/(\d+).json','geo.pelagiosViews.individual_json_dump'),
)
