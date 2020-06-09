from geo.models import *
from geo.forms import *
from hgl.settings.local import GOOGLE_API

from django.contrib.gis.geos import Point, MultiPoint, LineString, MultiPolygon
from django.contrib.gis.geos import GEOSGeometry, GeometryCollection
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, HttpResponse, render,HttpResponseRedirect
from django.http import JsonResponse

from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login, logout

from dal import autocomplete


def getKey(item):
    return item[0]


def kml(request):
    polis_list= Locus.objects.filter(locus_type__name='Polis').filter(related_locus__name='Cyrenaica')
    return render_to_response('../templates/geo/kml.xml',{'polis_list':polis_list},content_type='text/xml')
    
def geojson(request):
    id = request.GET.get('id','')
    obj = Locus.objects.get(pk=id)
    geojson = obj.geojsion
    return JsonResponse(geojson, safe=False)


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
        geom = locus.getConvexHull()

        return JsonResponse( geom )
    else:
        return JsonResponse({'Records':'None'})

    #     rels = Related_Locus.objects\
    #         .filter(obj=locus)\
    #         .filter(related_locus_type__name='forms part of')
    #     points = []
    #     # Try to recover convex hull for poly within poly    
    #     # polys = []

    #     for r in rels:
    #         for c in r.subject.locus_coordinate.all():
    #             points.append(c.point)
    #             subrels = Related_Locus.objects\
    #                  .filter(obj=r.subject)\
    #                  .filter(related_locus_type__name='forms part of')
    #             for sr in subrels:
    #                 for cc in sr.subject.locus_coordinate.all():
    #                     points.append(cc.point)                    
    #                     subsubrels = Related_Locus.objects\
    #                         .filter(obj=sr.subject)\
    #                         .filter(related_locus_type__name='forms part of')                        
    #                     for ssr in subsubrels:
    #                         for ccc in ssr.subject.locus_coordinate.all():
    #                             points.append(ccc.point)                         
    #         #polys.append(convex_hull_children(r.subject.id))

    #     #Maybe going about this wrongly Neil

    #     mp = MultiPoint(points)

    #     #return HttpResponse(polys[0].__str__())

    #     #if polys.__len__() > 0:
    #     #    cx = MultiPolygon(polys)
    #     #    cnvx = cx.convex_hull

    #     if rels.__len__() < 3: #and polys.__len__() > 0 :
    #         #Not enough coords for a hull?
            
    #         coords = []
    #         for p in points:
    #             coords.append( [p.x, p.y ])
    #         geojson = {}
    #         geojson["type"] = "Feature"
    #         geojson["geometry"] = {}
    #         geojson["geometry"]["type"] = "MultiPoint"
    #         geojson["geometry"]["coordinates"] = coords            
    #         return JsonResponse( geojson )            
    #     # We need to convert this intoa dict object
    #     coords = []
    #     try:
    #         for css in mp.convex_hull.coords[0]:
    #             coords.append( [css[0],css[1]] )
    #         # If polys exist the add their coords to the array
    #         #if polys.__len__() < 0:
    #         #    cnvx = MultiPolygon([cnvx,mp]).convex_hull
    #         #    for i in cnvx.coords[0]:
    #         #        coords.append( [i[0],i[1]] )
    #         geojson = {}
    #         geojson["type"] = "Feature"
    #         geojson["geometry"] = {}
    #         geojson["geometry"]["type"] = "Polygon"
    #         geojson["geometry"]["coordinates"] = []
    #         geojson["geometry"]["coordinates"].append(coords)
    #     except Exception:
    #         return JsonResponse({'Records':'None'})
    # # Debug responder
    # return JsonResponse( geojson )



def convex_hull_children(id):
    try:
        locus = Locus.objects.get(pk=id)
    except Exception:
        locus = None
    if locus:
        rels = Related_Locus.objects\
            .filter(obj=locus)\
            .filter(related_locus_type__name='forms part of')
        points = []
        for r in rels:
            for c in r.subject.locus_coordinate.all():
                points.append(c.point)
        #for r in rels:
        mp = MultiPoint(points)
        if rels.__len__() < 3:
            #Not enough coords for a hull?  
            pass
        else:            
        # We need to convert this in to a dict object
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
                pass
    # Debug responder
        return mp.convex_hull



def line(request):
    # Return a JSON line response when line type feature
    parent_id = request.GET.get('parent','')
    locus = Locus.objects.get(pk=parent_id)
    debug = []
    points = []
    if locus:
        rels = Related_Locus.objects.filter(obj=locus)#.filter(related_locus_type=3)
        for r in rels:
            for c in r.subject.locus_coordinate.all():
                points.append(c.point)
                debug.append(r.subject.id)
                debug.append("-")
            subrels = Related_Locus.objects.filter(obj=r.subject)#.filter(related_locus_type=3)
            
            for sr in subrels:
                for sc in sr.subject.locus_coordinate.all():
                    points.append(sc.point)
                    debug.append(sr.subject.id)
                    debug.append("+")

                subsubrels = Related_Locus.objects.filter(obj=sr.subject)
                for ssr in subsubrels:
                    for ssc in ssr.subject.locus_coordinate.all():
                        points.append(ssc.point)
                        debug.append("++") 

        #return HttpResponse(points)
        pl = LineString(points)
        pl = pl.geojson
        
        coords = []
        for p in points:
            coords.append( [p.x, p.y] )

        coords_sort = sorted(coords, key=getKey)

        geojson = {}
        geojson["type"] = "Feature"
        geojson["geometry"] = {}
        geojson["geometry"]["type"] = "LineString"
        geojson["geometry"]["coordinates"] = coords_sort
        #geojson["geometry"]["coordinates"].append(coords)
    #return HttpResponse(points)
    return JsonResponse(geojson)

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
    context['google_api'] = GOOGLE_API
    return render_to_response('../templates/single-record.html',context,context_instance=RequestContext(request))


def recordview_simple(request,record_id):
    id = record_id
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
