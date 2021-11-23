from catalogue.models import *
from requests_oauthlib import OAuth2Session
import json

from django.template import RequestContext
from django.shortcuts import (
    get_object_or_404,
    render,
    HttpResponse,
    render,
    HttpResponseRedirect,
)


def recordview(request):
    id = request.GET.get("id", "")
    item = BasicArchiveModel.objects.get(pk=id)
    context = {}
    context["record"] = item
    return render(
        request,
        "../templates/single-cat-record.html",
        context
    )


def browse(request):
    ### Gets all top level containers (no parent)
    context = {}
    context["cats"] = BasicArchiveModel.objects.filter(parent__isnull=True)
    return render(
        request,
        "../templates/browse.html", context
    )


def browse_item(request, id):
    context = {}
    context["cat"] = BasicArchiveModel.objects.get(pk=id)
    return render(
        request,
        "../templates/browse_item.html",
        context
    )


def tag_search(request, id):
    context = {}
    searchurl = "https://hypothes.is/api/search?tag=HGL:" + str(id)
    token = {
        "access_token": "6879-AHM93XsH2RBSu71vTSt6odLIFRPt35oFbmXYqpSn-5E",
        "token_type": "Bearer",
    }
    hyp = OAuth2Session(token=token)
    ret = hyp.get(searchurl).json()
    return HttpResponse(json.dumps(ret), content_type="application/json")


def image_search(request, id):
    context = {}
    searchurl = "https://hypothes.is/api/search?tag=HGLimage:" + str(id)
    token = {
        "access_token": "6879-AHM93XsH2RBSu71vTSt6odLIFRPt35oFbmXYqpSn-5E",
        "token_type": "Bearer",
    }
    hyp = OAuth2Session(token=token)
    ret = hyp.get(searchurl).json()
    return HttpResponse(json.dumps(ret), content_type="application/json")
