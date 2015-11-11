from django.conf.urls.defaults import *

urlpatterns = patterns('',
#    (r'^$', 'geo.views.index'),
    (r'^kml', 'geo.views.kml')
)
