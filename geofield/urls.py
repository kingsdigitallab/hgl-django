from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('geofield.views',
    # For creating custom js to append to admin screen as configured in app/admin.py
    (r'^geocode.js', 'geofield_js'),
    #('/geocode_poly.js', 'geofield_poly_js'),	
)
