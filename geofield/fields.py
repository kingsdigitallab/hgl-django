
from django.contrib.gis.db.models import PointField
from geopy import geocoders



class GeocodePointField(PointField):
    # collect some parameters for Geocoding
    def __init__(self, region=None,lookup_field=None, **kwargs):
        self.geocoder = geocoders.GeoNames()	
        super(GeocodePointField, self).__init__(**kwargs)
    """
    region:
    An additional value to pass to the geocoder to restrict the result set

    lookup_field:
    The related field in the model that holds the string to pass by default to the geocoder
    """

    # Define a geocoder for the point using GeoNames

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^geofield\.fields\.GeocodePointField"])
    
    