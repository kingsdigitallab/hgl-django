from django.conf.urls import url
from .add_views import (
    add_parent,
    add_children,
    add_feature,
    add_variant,
    add_uri,
    add
)
urlpatterns = [

    url(r"parent/(\d+)/$", add_parent),
    url(r"children/(\d+)/$", add_children),
    url(r"feature/(\d+)/$", add_feature),
    url(r"variant/(\d+)/$", add_variant),
    url(r"uri/(\d+)/$", add_uri),
    url(r"^$", add),
]
