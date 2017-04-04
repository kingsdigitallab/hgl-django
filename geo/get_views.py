from geo.models import *
from geo.forms import *

from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, HttpResponse, render,HttpResponseRedirect
from django.http import JsonResponse

from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login, logout

def get_children(request,id):
    form = LocationSelection()
    rel_type =  'children'
    return render(request, 'locations.html', {'form': form,'rel_type': rel_type,'id':id })

def get_parent(request,id):
    form = LocationSelection()
    rel_type =  'parent'
    return render(request, 'locations.html', {'form': form,'rel_type': rel_type,'id':id })
    
def get_features(request,id):
    form = FeatureSelection()
    rel_type =  'feature'
    return render(request, 'locations.html', {'form': form,'rel_type': rel_type,'id':id })    
    
def get_variant(request,id):
    form = VariantAdd()
    rel_type = 'variant'
    return render(request, 'locations.html', {'form': form,'rel_type': rel_type,'id':id })    

def get_uri(request,id):
    form = UrlAdd()
    rel_type = 'uri'
    return render(request, 'locations.html', {'form': form,'rel_type': rel_type,'id':id })
