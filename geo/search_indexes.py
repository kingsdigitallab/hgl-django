from haystack import indexes
from geo.models import Locus

class LocusIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #location_feature_type = indexes.MultiValueField(faceted=True)
    name =  indexes.CharField(model_attr='name')

    #def prepare_location_feature_type(self, object):
    #    return [ ft.description for ft in object.featuretype_fk.all() ]

    def get_model(self):
        return Locus

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


