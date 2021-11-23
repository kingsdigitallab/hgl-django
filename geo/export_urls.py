from .export_views import json_dump, single_json_dump
from django.conf.urls import url
urlpatterns = [
    url(r"dumpall/$", json_dump),
    url(r"locus/(\d+)/$", single_json_dump),
]
