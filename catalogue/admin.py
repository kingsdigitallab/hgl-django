from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from catalogue.models import * 


class PersonAdmin(admin.ModelAdmin):
    filter_horizontal = ['item',]

class BibRefAdmin(admin.ModelAdmin):
    filter_horizontal = ['item',]

class PersonInline(admin.StackedInline):
    model = Person.item.through

class ImageInline(admin.StackedInline):
    model = Image

class NoteInline(admin.StackedInline):
    model = Note

class PhysDescInline(admin.StackedInline):
    model = PhysDesc

class UnitIdInline(admin.StackedInline):
    model = UnitId

class GazLinkInline(admin.StackedInline):
    raw_id_fields = ['locus']
    model = cat_to_gaz_link

class BasicAdmin(admin.ModelAdmin):
    raw_id_fields = ['parent',]
    fields = ['parent','level','unittitle','unitstart_date','unitend_date',
    'repository', 'scopecontent','arrangement','custodhist',\
    'relatedmaterial','language', 'bioghist']
    filter_horizontal = ["language",]
    search_fields = ['unittitle',]
    inlines = [NoteInline,PhysDescInline,UnitIdInline,GazLinkInline,PersonInline,ImageInline]

class SimpleAdmin(admin.ModelAdmin):
    pass


admin.site.register(BasicArchiveModel, BasicAdmin)
admin.site.register(Note, SimpleAdmin)
admin.site.register(PhysDesc, SimpleAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(BibliographicReference, BibRefAdmin)
admin.site.register(Image, SimpleAdmin)
admin.site.register(UnitIdType, SimpleAdmin)
