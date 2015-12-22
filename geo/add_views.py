from geo.models import *
from geo.forms import *


from django.contrib.gis.geos import Point, MultiPoint
from django.contrib.gis.geos import GEOSGeometry
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, HttpResponse, render,HttpResponseRedirect
from django.http import JsonResponse

from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login, logout

def add(request):
    if request.POST: 
        pass
    else:
        form = NewRecordForm()
        return render(request, 'add-new-record.html', {'form': form})

