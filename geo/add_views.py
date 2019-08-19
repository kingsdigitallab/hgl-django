from geo.models import *
from geo.forms import *

from django.contrib.gis.geos import Point, MultiPoint
from django.contrib.gis.geos import GEOSGeometry
from django.template import RequestContext
from django.shortcuts import redirect, get_object_or_404, render_to_response, HttpResponse, render,HttpResponseRedirect
from django.http import JsonResponse

from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login, logout

def add(request):
    if request.method == 'POST': 
        form = NewRecordForm(request.POST)
        # New record
        l = Locus()
        if form.is_valid():
            l.name = form.cleaned_data['descriptor']
            l.save()
            if form.cleaned_data['feature_types']:
        	    for ft in form.cleaned_data['feature_types']:
        		    l.featuretype_fk.add(ft)
        		    l.save()
            if form.cleaned_data['notes']:
        	    l.notes = form.cleaned_data['notes']
            c = Coordinate()
            c.point = GEOSGeometry(form.cleaned_data['point'])
            c.latitude = c.point.y
            c.longitude = c.point.x
            c.locus = l
        	# default to first just to get it working
            c.heritage = Heritage.objects.all()[0]
            c.save()
            l.save()
            record = l
            return redirect('/irt_geo/recordview/?id='+ str(l.pk) )
        else:
            return render(request, 'add-new-record.html', {'form': form})

    else:
        form = NewRecordForm()
        return render(request, 'add-new-record.html', {'form': form})


def add_parent(request,id):
    if request.method == 'POST':
        form = LocationSelection(request.POST)
        if form.is_valid():
            l = Locus.objects.get(pk=id)
            for r in form.cleaned_data['locations']:
                rel = Related_Locus()
                rel.subject = l
                rel.obj = r
                rel.related_locus_type = Related_Locus_Type.objects.get(pk=1)
                rel.save()
            return redirect('/irt_geo/recordview/?id=' + str(id) )
        else:
            return redirect('/irt_geo/recordview/?id=' + str(id) )

def add_children(request,id):
    if request.method == 'POST':
        form = LocationSelection(request.POST)
        if form.is_valid():
            l = Locus.objects.get(pk=id)
            for r in form.cleaned_data['locations']:
                rel = Related_Locus()
                rel.obj = l
                rel.subject = r
                rel.related_locus_type = Related_Locus_Type.objects.get(pk=1)
                rel.save()
            return redirect('/irt_geo/recordview/?id=' + str(id) )
        else:
            return redirect('/irt_geo/recordview/?id=' + str(id) )

            
def add_feature(request,id):
    if request.method == 'POST':
        form = FeatureSelection(request.POST)    
        l = Locus.objects.get(pk=id)        
        if form.is_valid():
            for r in form.cleaned_data['features']:        
                l.featuretype_fk.add(r)
                l.save()
            return redirect('/irt_geo/recordview/?id=' + str(id) )
        else:
            return redirect('/irt_geo/recordview/?id=' + str(id) )
            
def add_variant(request,id):
    if request.method == 'POST':
        form = VariantAdd(request.POST)    
        l = Locus.objects.get(pk=id)        
        if form.is_valid():
            nv = Locus_Variant()
            nv.name = form.cleaned_data['variant_name']       
            nv.locus = l
            if form.cleaned_data['language']:
                nv.language = form.cleaned_data['language']
            if form.cleaned_data['attestation']:
                nv.attestation = form.cleaned_data['attestation']
            nv.save()
            return redirect('/irt_geo/recordview/?id=' + str(id) )
        else:
            return redirect('/irt_geo/recordview/?id=' + str(id) )
          

def add_uri(request,id):
    if request.method == 'POST':
        form = UrlAdd(request.POST)
        l = Locus.objects.get(pk=id)
        if form.is_valid():
            nv = ExternalURI()
            nv.uri = form.cleaned_data['uri']
            nv.locus = l
            nv.provenance = form.cleaned_data['provenance']
            nv.save()
            return redirect('/irt_geo/recordview/?id=' + str(id) )
        else:
            return redirect('/irt_geo/recordview/?id=' + str(id) )
