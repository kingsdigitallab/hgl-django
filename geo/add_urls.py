from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'parent/(\d+)/$','geo.add_views.add_parent'),	
    (r'children/(\d+)/$','geo.add_views.add_children'),
    (r'^$','geo.add_views.add'),
)
