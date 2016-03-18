from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'parent/(\d+)/$','geo.add_views.add_parent'),	
    (r'children/(\d+)/$','geo.add_views.add_children'),
    (r'feature/(\d+)/$','geo.add_views.add_feature'),
    (r'variant/(\d+)/$','geo.add_views.add_variant'),    
    (r'^$','geo.add_views.add'),
)
