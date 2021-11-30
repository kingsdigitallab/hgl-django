from django.conf.urls import url

from .pelagiosViews import json_dump, individual_json_dump

urlpatterns = [
    url(r"^downloads/json/dump.json", json_dump),
    url(r"^downloads/json/(\d+).json", individual_json_dump),
]
