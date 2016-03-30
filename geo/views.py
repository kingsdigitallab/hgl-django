from geo.models import *
from geo.forms import *

from django.contrib.gis.geos import Point, MultiPoint
from django.contrib.gis.geos import GEOSGeometry
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, HttpResponse, render,HttpResponseRedirect
from django.http import JsonResponse

from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login, logout

from dal import autocomplete


def kml(request):
    polis_list= Locus.objects.filter(locus_type__name='Polis').filter(related_locus__name='Cyrenaica')
    return render_to_response('../templates/geo/kml.xml',{'polis_list':polis_list},content_type='text/xml')
    
def convex_hull(request):
    parent_id = request.GET.get('parent','')
    if parent_id != '':
        try:
            locus = Locus.objects.get(pk=parent_id)
        except Exception:
            locus = None
    else:
        locus = None
    if locus:
        rels = Related_Locus.objects\
            .filter(obj=locus)\
            .filter(related_locus_type__name='forms part of')
        points = []    
        for r in rels:
            for c in r.subject.locus_coordinate.all():
                points.append(c.point)
        mp = MultiPoint(points)
        if rels.__len__() < 3:
            #Not enough coords for a hull?
            coords = []
            for p in points:
                coords.append( [p.x, p.y ])
            geojson = {}
            geojson["type"] = "Feature"
            geojson["geometry"] = {}
            geojson["geometry"]["type"] = "MultiPoint"
            geojson["geometry"]["coordinates"] = coords            
            return JsonResponse( geojson )            
        # We need to convert this intoa dict object
        coords = []
        try:
            for css in mp.convex_hull.coords[0]:
                coords.append( [css[0],css[1]] )
            geojson = {}
            geojson["type"] = "Feature"
            geojson["geometry"] = {}
            geojson["geometry"]["type"] = "Polygon"
            geojson["geometry"]["coordinates"] = []
            geojson["geometry"]["coordinates"].append(coords)
        except Exception:
            return JsonResponse({'Records':'None'})
    # Debug responder
    return JsonResponse( geojson )

def popupcontent(request):
    id = request.GET.get('id','')
    locus = Locus.objects.get(pk=id)
    #if Related_Locus.objects.filter(obj=locus).filter(related_locus_type__name='forms part of').count() > 0:
    #    return HttpResponse('<div>' + locus.name + ' I have children! </div><div><a href="/irt_geo/convex-hull/?parent='+ locus.id.__str__() +'">Geojson hull</a></div>')
    return HttpResponse('<div><a href="/irt_geo/recordview/?id='+ str(id) + '">' + locus.name + '</a></div>')
    
def recordview(request):
    id = request.GET.get('id','')
    locus = Locus.objects.get(pk=id)    
    context = {}
    context['record'] = locus
    return render_to_response('../templates/single-record.html',context,context_instance=RequestContext(request))

def login_user(request):
    username = password = ''
    if request.POST: 
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    username = password = ''
    return HttpResponseRedirect('/')



class autocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Locus.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


def json_dump(request):
    dumpJson = dumpEmptyClass()
    for ae in Monument.objects.all():
        f = create_geojson_monument(ae)
        dumpJson.featureDict["features"].append( f )
    for ae in HistoricalUnit.objects.all():
        f = create_geojson_hu(ae)
        dumpJson.featureDict["features"].append( f )
    return HttpResponse(simplejson.dumps(dumpJson.featureDict),mimetype='application/json')
