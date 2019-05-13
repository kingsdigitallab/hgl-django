from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    (r'^recordview/$','catalogue.views.recordview'),
    (r'^hypothesis-tag/(\d+)', 'catalogue.views.tag_search'),
    (r'^hypothesis-image/(\d+)', 'catalogue.views.image_search'),
    (r'^(\d+)/', 'catalogue.views.browse_item'),
    (r'^$', 'catalogue.views.browse'),
)
