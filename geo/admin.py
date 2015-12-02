from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.forms.models import BaseInlineFormSet
from geo.models import * #Heritage, Locus_Type, Locus, Coordinate, Related_Locus_Type, Related_Locus, Locus_Variant\
    #,Inscription, Inscription_Locus_Type, Inscription_Locus, Geojson *

## compare method to be used to validate the input
## get featuretype and validate coordinate count accordingly
#def compare(featuretype, row):
#    if featuretype == 0:
#        if row > 1:
#            raise ValidationError('point has one data entry!')
#    if featuretype == 1:
#        if row != 2:
#            raise ValidationError('line has two data entries!')
#    if featuretype == 2:
#        if row < 3:
#            raise ValidationError('polygon has more than three data entries!')

## try validate in this class but failed
#class CoordinateInlineFormSet(BaseInlineFormSet):
## get current coordinate count
#    def getCount(self):
#        return len(self.forms)
## get returned 'featuretype' value from class 'Locus' and compare it with coordinate count
## not getting selected value of 'featuretype' but default value since it's instantising the object
## couldn't find the fix 
#    def clean(self):
#       compare(Locus().getType(),self.getCount())


class BasicAdmin(admin.ModelAdmin):
    pass

class AttestationInline(admin.StackedInline):
    model = VariantAttestation


class HeritageAdmin(admin.ModelAdmin):
    model = Heritage
    
    date_hierarchy = 'modified'
    
    list_display = ['name', 'recorded_by', 'hardware', 'accuracy', 'modified', 'created']
    list_display_links = ['name']
    list_filter = ['modified', 'created']

    ordering = ['modified', 'name']

    search_fields = ['name', 'recorded_by', 'hardware', 'accuracy']

#
class Locus_TypeAdmin(admin.ModelAdmin):
    model = Locus_Type
    
    date_hierarchy = 'modified'
    
    list_display = ['name', 'modified', 'created']
    list_display_links = ['name']
    list_filter = ['modified', 'created']

    ordering = ['modified', 'name']

#
class CoordinateInline(admin.TabularInline):
    model = Coordinate
    fieldsets = [
        ('Coordinates', {'fields': ['latitude', 'longitude','height','point']}),
        (None, {'fields': ['heritage', 'feature',]}),
    ]
    #formset = CoordinateInlineFormSet
    extra = 1

#
class Related_LocusInline(admin.TabularInline):
    model = Related_Locus
    raw_id_fields = ('obj',)
    autocomplete_lookup_fields = {
        'fk': ['obj'],
    }
    fieldsets = [
        (None, {'fields': ['obj','related_locus_type','period','note','date_from','date_to',]}),
    ]    
    ordering = ['obj']
    fk_name = 'subject'
    extra = 1

#
class Related_LocusInverseInline(admin.TabularInline):
    model = Related_Locus
    fields = ['subject', 'related_locus_type',]
    fk_name = 'obj'
    extra = 0
    verbose_name = 'Inverse Related Location'
    verbose_name_plural = 'Inverse Related Locations'

#
class Locus_VariantInline(admin.TabularInline):
    model = Locus_Variant
    fields = ['name','language']
    extra = 1

#
#class GeojsonInline(admin.TabularInline):
#    model = Geojson
#    fields = ['geojson']
#    extra = 1

#
class LocusAdmin(admin.ModelAdmin):
    model = Locus
    exclude = ('locus_type',)
    filter_horizontal = ['featuretype_fk',]
    list_display = ['id', 'name', 'pleiades_uri', 'locus_type', 'modified', 'created']
    list_display_links = ['name']
    list_filter = ['locus_type', 'modified', 'created']

    ordering = ['name', 'id', 'modified']
    search_fields = ['name']
    
    inlines = [CoordinateInline,Related_LocusInline, Locus_VariantInline, Related_LocusInverseInline]

    class Media:
        geofield = 'coordinate'
        js = ('/static/vendor/leaflet/dist/leaflet.js',\
              '/static/js/leaflet-omnivore-master/leaflet-omnivore.min.js',\
              '/static/vendor/leaflet-draw/dist/leaflet.draw.js',\
              '/geofield/%s/geofield.js' % geofield )
        css = {
            'all':('/static/vendor/leaflet/dist/leaflet.css',\
                '/static/vendor/leaflet-draw/dist/leaflet.draw.css',)
        }

#
class CoordinateAdmin(admin.ModelAdmin):
    model = Coordinate

    date_hierarchy = 'modified'

    list_display = ['latitude', 'longitude', 'height', 'heritage', 'feature', 'locus', 'modified', 'created']
    list_display_links = ['latitude', 'longitude']
    list_filter = ['heritage', 'modified', 'created']

    ordering = ['modified']

    search_fields = ['heritage', 'feature']
    
#
class Related_Locus_TypeAdmin(admin.ModelAdmin):
    model = Related_Locus_Type
    
    date_hierarchy = 'modified'
    
    list_display = ['name', 'modified', 'created']
    list_display_links = ['name']
    list_filter = ('modified', 'created',)

    ordering = ['modified', 'name']
    
#
class Locus_VariantAdmin(admin.ModelAdmin):
    model = Locus_Variant
    inlines = [AttestationInline,]
    date_hierarchy = 'modified'
    
    list_display = ['name', 'modified', 'created']
    list_display_links = ['name']
    list_filter = ['modified', 'created']

    ordering = ['modified', 'name']

#
class Inscription_LocusInline(admin.TabularInline):
    model = Inscription_Locus

    fieldsets = [
        ('Type', {'fields': ['inscription_locus_type']}),
        ('Location', {'fields': ['locus']}),
    ]

    extra = 1
    
#
class InscriptionAdmin(admin.ModelAdmin):
    model = Inscription
    
    list_display = ['inscription_id', 'title', 'modified', 'created']
    list_display_links = ['inscription_id', 'title']
    list_filter = ['modified', 'created']

    ordering = ['modified', 'inscription_id']
    
    inlines = [Inscription_LocusInline]
    
#
class Inscription_Locus_TypeAdmin(admin.ModelAdmin):
    model = Inscription_Locus_Type

    list_display = ['name', 'modified', 'created']
    list_display_links = ['name']
    list_filter = ['modified', 'created']

    ordering = ['modified', 'name']

#
class Inscription_LocusAdmin(admin.ModelAdmin):
    model = Inscription_Locus

    date_hierarchy = 'modified'

    list_display = ['context', 'modified', 'created']
    list_display_links = ['context']
    list_filter = []

    ordering = []


#
admin.site.register(Heritage, HeritageAdmin)
admin.site.register(Locus_Type, Locus_TypeAdmin)
admin.site.register(Locus, LocusAdmin)
admin.site.register(Coordinate, CoordinateAdmin)
admin.site.register(Related_Locus_Type, Related_Locus_TypeAdmin)
admin.site.register(Locus_Variant, Locus_VariantAdmin)
admin.site.register(Inscription, InscriptionAdmin)
admin.site.register(Inscription_Locus_Type, Inscription_Locus_TypeAdmin)
admin.site.register(Inscription_Locus, Inscription_LocusAdmin)


admin.site.register(VariantAttestation,BasicAdmin)
admin.site.register(Author,BasicAdmin)
admin.site.register(Publication,BasicAdmin)
admin.site.register(PublicationType,BasicAdmin)
admin.site.register(FeatureTypes,BasicAdmin)
admin.site.register(Period,BasicAdmin)
admin.site.register(Language,BasicAdmin)
admin.site.register(Related_Locus,BasicAdmin)
