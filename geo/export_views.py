
# Create your views here.
from django.core.mail import send_mail
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response,render
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


from geo.models import *

import datetime
import urllib2
import codecs
import simplejson



from django.contrib.gis.geos import GEOSGeometry


 
class locusEmptyClass:
    def __init__(self):
        self.featureDict = {"type":"Feature",\
            "properties":{}\
        }
    
class dumpEmptyClass:
    def __init__(self):
        self.featureDict = {"type":"FeatureCollection",\
            "features":[]\
        }    

def json_dump(request):
    dumpJson = dumpEmptyClass()
    for l in Locus.objects.all():
        f = create_geojson_locus(l)
        dumpJson.featureDict["features"].append( f )
    return HttpResponse(simplejson.dumps(dumpJson.featureDict,sort_keys=True, indent=4 * ' '),content_type='application/json')   

def single_json_dump(request,id):
    locus =  Locus.objects.get(pk=id)
    f = create_geojson_locus(locus)
    return HttpResponse(simplejson.dumps(f,sort_keys=True, indent=4 * ' '),content_type='application/json')       
    
def create_geojson_locus(locus):
    jsonObj = {}
    jsonObj['type'] = 'Feature'
    jsonObj['geometry'] = {}
    jsonObj['geometry']['type'] = 'MultiPoint'
    jsonObj['geometry']['coordinates'] = []
    for c in locus.locus_coordinate.all():
        jsonObj['geometry']['coordinates'].append( [ c.point.x , c.point.y] )
    jsonObj['properties'] = {}
    jsonObj['properties']['default_name'] = locus.name
    jsonObj['feature_types'] = []
    for f in locus.featuretype_fk.all():
        jsonObj['feature_types'].append(f.description)
    jsonObj['properties']['id'] = locus.id       
    jsonObj['properties']['child_locations'] = []
    for r in Locus.objects.filter(related_locus=locus):
        jsonObj['properties']['child_locations'].append( { 'name':r.name, 'id':r.id } )
    jsonObj['properties']['name_variants'] = []    
    for n in locus.variants.all():
        jsonObj['properties']['name_variants'].append({'variant': n.name, 'attestation': n.attestation , 'language': n.language })
    jsonObj['properties']['parent_locations'] = []
    for p in locus.related_locus.all():
        jsonObj['properties']['parent_locations'].append( { 'name':p.name, 'id':p.id } )
    return jsonObj
    