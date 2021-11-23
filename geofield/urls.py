from django.conf.urls import include, url
from django.contrib import admin
from .views import geofield_js
urlpatterns = [
    # For creating custom js to append to admin screen as configured in app/admin.py
    url(r"^geocode.js", geofield_js),
    # ('/geocode_poly.js', 'geofield_poly_js'),
]
