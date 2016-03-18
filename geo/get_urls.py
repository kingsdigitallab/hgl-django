from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    (r'locus-child/(\d+)/$','geo.get_views.get_children'),
    (r'locus-parent/(\d+)/$','geo.get_views.get_parent'),
    (r'features/(\d+)/$','geo.get_views.get_features'),    
    (r'variant/(\d+)/$','geo.get_views.get_variant'),        
)
