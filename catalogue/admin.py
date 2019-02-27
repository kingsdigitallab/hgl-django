from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from catalogue.models import * 



class NoteInline(admin.StackedInline):
    model = Note

class PhysDescInline(admin.StackedInline):
    model = PhysDesc

class UnitIdInline(admin.StackedInline):
    model = UnitId

class BasicAdmin(admin.ModelAdmin):
    raw_id_fields = ['parent',]
    fields = ['parent','level','unittitle','unitstart_date','unitend_date',
    'repository', 'scopecontent','arrangement','custodhist',\
    'relatedmaterial','language',]
    filter_horizontal = ["language",]
    inlines = [NoteInline,PhysDescInline,UnitIdInline]

class SimpleAdmin(admin.ModelAdmin):
    pass


admin.site.register(BasicArchiveModel, BasicAdmin)
admin.site.register(Note, SimpleAdmin)
admin.site.register(PhysDesc, SimpleAdmin)
