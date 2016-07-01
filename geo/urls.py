from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    (r'^kml', 'geo.views.kml'),
    (r'^convex-hull/$','geo.views.convex_hull'),
    (r'^line/$','geo.views.line'),
    (r'^popupcontent/$','geo.views.popupcontent'),
    (r'^recordview/$','geo.views.recordview'),
)
