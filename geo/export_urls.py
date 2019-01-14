from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    (r'dumpall/$','geo.export_views.json_dump'),
    (r'locus/(\d+)/$','geo.export_views.single_json_dump'),
)
