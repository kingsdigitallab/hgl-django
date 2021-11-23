from django.conf.urls import include, url
from .get_views import(
    get_children,
    get_parent,
    get_features,
    get_uri,
    get_variant
) 

urlpatterns = [
    url(r"locus-child/(\d+)/$", get_children),
    url(r"locus-parent/(\d+)/$", get_parent),
    url(r"features/(\d+)/$", get_features),
    url(r"variant/(\d+)/$", get_variant),
    url(r"uri/(\d+)/$", get_uri),
]
