# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth import authenticate
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render_to_response



def geofield_js(request,field):
    context = {}
    context['geofield_js'] = field
    return render_to_response('geofield_js.js', context, context_instance=RequestContext(request) , content_type='application/javascript')		
	
def geofield_poly_js(request,field):
    context = {}
    context['geofield_js'] = field
    return render_to_response('geofield_poly_js.js', context, context_instance=RequestContext(request) , content_type='application/javascript')	


