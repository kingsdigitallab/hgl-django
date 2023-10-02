from haystack import indexes
from catalogue.models import *

class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    preferred_name = indexes.CharField()
    alternative_names = indexes.MultiValueField(null=True)
    description = indexes.CharField()
    surname = indexes.FacetCharField(model_attr="surname")
    firstNames = indexes.CharField(model_attr="firstNames")
    details = indexes.CharField(model_attr="details")
    # date_from = indexes.FacetDateField(model_attr="DateFrom", null=True)
    # date_to = indexes.FacetDateField(model_attr="DateTo", null=True)
    references = indexes.MultiValueField(null=True)
    record_type = indexes.FacetCharField()
    sort_name = indexes.CharField(indexed=False, stored=True)

    def get_model(self):
        return Person

    def prepare_preferred_name(self, obj):
        preferred_name = obj.get_preferred_alternative_name()
        if preferred_name:
            return preferred_name.get_description()
        return obj.firstNames + " " + obj.surname

    def prepare_description(self, obj):
        preferred_name = obj.get_preferred_alternative_name()
        if preferred_name:
            return preferred_name.get_description()
        return obj.get_description()

    def prepare_references(self, obj):
        ret = []
        for ref in Reference.objects.filter(person=obj):
            ret.append(ref.__str__())
        return ret

    def prepare_record_type(self, obj):
        return "Person"

    def prepare_alternative_names(self, obj):
        ret = []
        for name in AlternativeName.objects.filter(person=obj):
            desc = name.get_description()
            if (desc is not None and len(desc) > 0):
                ret.append(desc)
        return ret
    def prepare_sort_name(self, obj):
        ret = obj.surname.lower() + " " + obj.firstNames.lower()
        return ret

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
    record_type = indexes.FacetCharField()

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

    def prepare_record_type(self, obj):
        return "BasicArchiveModel"

    def get_model(self):
        return BasicArchiveModel

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
