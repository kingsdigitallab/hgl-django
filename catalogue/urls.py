from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    (r'^recordview/$','catalogue.views.recordview'),
    (r'^(\d+)/', 'catalogue.views.browse_item'),
    (r'^$', 'catalogue.views.browse'),
)