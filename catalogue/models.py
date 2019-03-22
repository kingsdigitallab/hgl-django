from django.db import models
import mptt

# Create your models here.


def get_parent(x):
    if not x.parent:
        return x
    return get_parent(x.parent)


class BasicArchiveModel(models.Model):
    level = models.ForeignKey("Level")
    unittitle = models.CharField(max_length=100)
    unitstart_date = models.IntegerField()
    unitend_date = models.IntegerField()
    repository = models.ForeignKey("Repository")
    scopecontent = models.TextField(null=True, blank=True)
    arrangement = models.TextField(null=True, blank=True)
    custodhist = models.TextField(null=True, blank=True)
    relatedmaterial = models.TextField(null=True, blank=True)
    bioghist = models.TextField(null=True, blank=True)
    language = models.ManyToManyField("Language", null=True, blank=True)
    # Fields above basic req. for Archive level desc.
    parent =  models.ForeignKey('self', null=True, blank=True,\
                                related_name="children")
    def __unicode__(self):
        return self.unittitle

    def get_top_parent(self):
        if get_parent(self) == self:
           return None
        else:
           return get_parent(self)

    def clean_scope(self):
        str = self.scopecontent.replace(" u'", " ").replace("None,", "")\
            .replace("[u","").replace("]","")
        return str

    def clean_arr(self):
        str = self.arrangement.replace(" u'", " ").replace("None,", "")\
            .replace("[u","").replace("]","")
        return str

    def clean_cust(self):
        str = self.custodhist.replace(" u'", " ").replace("None,", "")\
            .replace("[u","").replace("]","")
        return str

    def clean_bio(self):
        str = self.bioghist.replace(" u'", " ").replace("None,", "")\
            .replace("[u","").replace("]","")
        return str

    def clean_rel(self):
        str = self.relatedmaterial.replace(" u'", " ").replace("None,", "")\
            .replace("[u","").replace("]","")
        return str


#mptt.register(BasicArchiveModel)

class PhysDesc(models.Model):
    type = models.ForeignKey("PhysDescType")
    desc = models.TextField(null=True, blank=True)
    item = models.ForeignKey("BasicArchiveModel", null=True, blank=True,\
                             related_name='item_physdesc')
    def __unicode__(self):
        return self.type.desc

class PhysDescType(models.Model):
    desc = models.CharField(max_length=50)
    def __unicode__(self):
        return self.desc

class Repository(models.Model):
    desc = models.CharField(max_length=100)
    def __unicode__(self):
        return self.desc

class UnitId(models.Model):
    type = models.ForeignKey("UnitIdType")
    desc = models.TextField(null=True, blank=True)
    item = models.ForeignKey("BasicArchiveModel", null=True, blank=True)
    def __unicode__(self):
        return self.type.desc

class UnitIdType(models.Model):
    desc = models.CharField(max_length=50)

class Note(models.Model):
    audience = models.ForeignKey("NoteAudience")
    type = models.ForeignKey("NoteType")
    text = models.TextField(null=True, blank=True)
    item = models.ForeignKey("BasicArchiveModel", null=True, blank=True,\
                             related_name="item_note")
    def __unicode__(self):
        return self.audience.desc

class NoteAudience(models.Model):
    desc = models.CharField(max_length=50)
    def __unicode__(self):
        return self.desc

class NoteType(models.Model):
    desc = models.CharField(max_length=50)
    def __unicode__(self):
        return self.desc

class Level(models.Model):
    desc = models.CharField(max_length=50)
    def __unicode__(self):
        return self.desc

class Language(models.Model):
    desc = models.CharField(max_length=100)
    def __unicode__(self):
        return self.desc

