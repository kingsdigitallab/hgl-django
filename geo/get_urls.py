from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    (r'locus-child/(\d+)/$','geo.get_views.get_children'),
)
