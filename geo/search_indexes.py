from haystack import indexes
from geo.models import *

class LocusIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    Feature = indexes.MultiValueField(faceted=True)
    name = indexes.CharField(model_attr='name')
    sort_name = indexes.CharField(indexed=False, stored=True)
    variant_names =  indexes.MultiValueField()   
    Period = indexes.MultiValueField(faceted=True)

    def prepare_Feature(self, object):
        return [ ft.description for ft in object.featuretype_fk.all() ]
    
    #def prepare_location_feature_type(self, obj):
    #    ret = []
    #    for f in obj.featuretype_fk.all():
    #        ret.append(f.description)
    #    return ret
    
    def prepare_variant_names(self,obj):
        ret = []
        for v in obj.variants.all():
            ret.append(v.name)
        return ret

    def prepare_Period(self, obj):
        ret = []
        try:
            rls = Related_Locus.objects.filter(obj=obj)
            for r in rls:
                if r.period.description not in ret:
                    ret.append(r.period.description)
            return ret
        except Exception:
            return []

    def prepare_sort_name(self,obj):
        ret = obj.name.lower()
        ret = ret.replace(':',' ')
        ret = ret.replace(',',' ')
        return ret

    def get_model(self):
        return Locus

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


