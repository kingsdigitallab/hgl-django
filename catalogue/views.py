from catalogue.models import *

from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, HttpResponse, render,HttpResponseRedirect

    
def recordview(request):
    id = request.GET.get('id','')
    item = BasicArchiveModel.objects.get(pk=id)    
    context = {}
    context['record'] = item
    return render_to_response('../templates/single-cat-record.html',context,context_instance=RequestContext(request))


def browse(request):
    ### Gets all top level containers (no parent)
    context = {}
    context['cats'] = BasicArchiveModel.objects.filter(parent__isnull=True)
    return render_to_response('../templates/browse.html',context,context_instance=RequestContext(request))

def browse_item(request, id):
    context = {}
    context['cat'] = BasicArchiveModel.objects.get(pk=id)
    return render_to_response('../templates/browse_item.html',context,context_instance=RequestContext(request))