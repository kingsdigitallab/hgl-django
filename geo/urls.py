from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    (r'^kml', 'geo.views.kml')
)
