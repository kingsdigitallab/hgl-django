from geo.models import *
from geo.forms import *

from django.template import RequestContext
from django.shortcuts import (
    get_object_or_404,
    render,
    HttpResponse,    
    HttpResponseRedirect,
)


import json as simplejson


def getKey(item):
    return item[0]


class templateClass:
    def __init__(self):
        self.featureDict = {
            "geometry": {
                "type": "MultiPoint",
                "coordinates": [],
                "properties": {"provenances": []},
            },
            "type": "Feature",
            "uri": "placeholder",
            "properties": {"types": []},
            "links": {"broad_matches": [], "close_matches": []},
            "names": [],
        }


class dumpEmptyClass:
    def __init__(self):
        self.featureDict = {"type": "FeatureCollection", "features": []}


def json_dump(request):
    dumpJson = dumpEmptyClass()
    for loc in Locus.objects.all():
        l = create_json_record(loc)
        dumpJson.featureDict["features"].append(l)
    return HttpResponse(
        simplejson.dumps(dumpJson.featureDict), content_type="application/json"
    )


def create_json_record(loc):
    ret = templateClass()
    for l in loc.locus_coordinate.all():
        ret.featureDict["geometry"]["coordinates"].append([l.point.x, l.point.y])
        ret.featureDict["geometry"]["properties"]["provenances"].append(l.heritage.name)
    if loc.locus_coordinate.all().__len__() == 0:
        del ret.featureDict["geometry"]
    if loc.locus_coordinate.all().__len__() == 1:
        ret.featureDict["geometry"]["type"] = "Point"
    ret.featureDict["title"] = loc.name
    ret.featureDict["id"] = loc.pk
    for t in loc.featuretype_fk.all():
        ret.featureDict["properties"]["types"].append(t.description)
    ret.featureDict["uri"] = "http://www.slsgazetteer.org/" + str(loc.id)
    for ln in loc.externaluri_set.all():
        if "geoname" in ln.uri:
            ret.featureDict["links"]["broad_matches"].append(ln.uri)
        else:
            ret.featureDict["links"]["close_matches"].append(ln.uri)
    for n in loc.variants.all():
        ret.featureDict["names"].append({"name": n.name})
    return ret.featureDict


def individual_json_dump(request, i):
    locus = Locus.objects.get(pk=i)
    ret = create_json_record(locus)
    # for l in locus.locus_coordinate.all():
    #    ret.featureDict["geometry"]["coordinates"].append([l.point.x,l.point.y])
    return HttpResponse(simplejson.dumps(ret), content_type="application/json")
