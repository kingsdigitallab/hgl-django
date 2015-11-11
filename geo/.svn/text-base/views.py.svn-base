from geo.models import *
from django.shortcuts import get_object_or_404, render_to_response

def kml(request):
    polis_list= Locus.objects.filter(locus_type__name='Polis').filter(related_locus__name='Cyrenaica')
    return render_to_response('../templates/geo/kml.xml',{'polis_list':polis_list},mimetype='text/xml')
