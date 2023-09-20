from django.conf.urls import include, url
from .views import (
    recordview,
    tag_search,
    image_search,
    browse_item,
    browse
)

urlpatterns = [

    url(r"^recordview/$", recordview),
    url(r"^hypothesis-tag/(\d+)", tag_search),
    url(r"^hypothesis-image/(\d+)", image_search),

    url(r"^(\d+)/", browse_item),
    url(r"^$", browse),

]