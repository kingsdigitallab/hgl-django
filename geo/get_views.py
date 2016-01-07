from geo.models import *
from geo.forms import *

from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, HttpResponse, render,HttpResponseRedirect
from django.http import JsonResponse

from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login, logout

def get_children(request,id):
    form = LocationSelection()
    return render(request, 'locations.html', {'form': form})

