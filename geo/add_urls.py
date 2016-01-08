from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^$','geo.add_views.add'),
)
