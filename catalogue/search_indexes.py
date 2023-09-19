from haystack import indexes
from catalogue.models import *

class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    surname = indexes.CharField(model_attr="surname")
    firstNames = indexes.CharField(model_attr="firstNames")
    details = indexes.CharField(model_attr="details")
    DateFrom = indexes.DateField(model_attr="DateFrom")
    DateTo = indexes.DateField(model_attr="DateTo")
    referenceType = indexes.FacetCharField(model_attr="referenceType")

    def get_model(self):
        return Person

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class CatalogueIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr="unittitle")
    level = indexes.CharField()
    sort_name = indexes.CharField(indexed=False, stored=True)
    language = indexes.MultiValueField()
    period_start = indexes.IntegerField()
    period_end = indexes.IntegerField()

    def prepare_period_start(self, obj):
        return obj.unitstart_date

    def prepare_period_end(self, obj):
        return obj.unitend_date

    def prepare_title(self, obj):
        return obj.unittitle

    def prepare_level(self, obj):
        return obj.level.desc

    def prepare_language(self, obj):
        ret = []
        for l in obj.language.all():
            ret.append(l.desc)
        return ret

    def prepare_sort_name(self, obj):
        ret = obj.unittitle.lower()
        ret = ret.replace(":", " ")
        ret = ret.replace(",", " ")
        return ret

    def get_model(self):
        return BasicArchiveModel

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
