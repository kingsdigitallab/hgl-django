from geo.models import *
from django.contrib.gis.geos import Point, MultiPoint
from django.contrib.gis.geos import GEOSGeometry
from django.shortcuts import get_object_or_404, render_to_response, HttpResponse
from django.http import JsonResponse


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
        # We need to convert this intoa dict object
        coords = []
        for css in mp.convex_hull.coords[0]:
            coords.append( [css[0],css[1]] )
        geojson = {}
        geojson["type"] = "Feature"
        geojson["geometry"] = {}
        geojson["geometry"]["type"] = "Polygon"
        geojson["geometry"]["coordinates"] = []
        geojson["geometry"]["coordinates"].append(coords)
    # Debuug responder
    return JsonResponse( geojson )
