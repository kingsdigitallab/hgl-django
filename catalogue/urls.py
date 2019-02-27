from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    (r'^recordview/$','catalogue.views.recordview'),
)
