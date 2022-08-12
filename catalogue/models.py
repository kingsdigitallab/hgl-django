from django.db import models


# Create your models here.


def get_parent(x):
    if not x.parent:
        return x
    return get_parent(x.parent)


class BasicArchiveModel(models.Model):
    level = models.ForeignKey("Level", on_delete=models.CASCADE)
    unittitle = models.CharField(max_length=100)
    unitstart_date = models.IntegerField()
    unitend_date = models.IntegerField()
    repository = models.ForeignKey("Repository", on_delete=models.CASCADE)
    scopecontent = models.TextField(null=True, blank=True)
    arrangement = models.TextField(null=True, blank=True)
    custodhist = models.TextField(null=True, blank=True)
    relatedmaterial = models.TextField(null=True, blank=True)
    bioghist = models.TextField(null=True, blank=True)
    language = models.ManyToManyField("Language", blank=True)
    # gaz_link = models.ManyToManyField("Locus", null=True, blank=True)
    # Fields above basic req. for Archive level desc.
    parent = models.ForeignKey("self", null=True, blank=True,
                               related_name="children",
                               on_delete=models.CASCADE)

    def __unicode__(self):
        return self.unittitle

    def __str__(self):
        return self.__unicode__()

    def get_top_parent(self):
        if get_parent(self) == self:
            return None
        else:
            return get_parent(self)

    def clean_scope(self):
        str = (
            self.scopecontent.replace(" u'", " ")
                .replace("None,", "")
                .replace("[u", "")
                .replace("]", "")
        )
        return str

    def clean_arr(self):
        str = (
            self.arrangement.replace(" u'", " ")
                .replace("None,", "")
                .replace("[u", "")
                .replace("]", "")
        )
        return str

    def clean_cust(self):
        str = (
            self.custodhist.replace(" u'", " ")
                .replace("None,", "")
                .replace("[u", "")
                .replace("]", "")
        )
        return str

    def clean_bio(self):
        str = (
            self.bioghist.replace(" u'", " ")
                .replace("None,", "")
                .replace("[u", "")
                .replace("]", "")
        )
        return str

    def clean_rel(self):
        str = (
            self.relatedmaterial.replace(" u'", " ")
                .replace("None,", "")
                .replace("[u", "")
                .replace("]", "")
        )
        return str


# mptt.register(BasicArchiveModel)


class cat_to_gaz_link(models.Model):
    item = models.ForeignKey("BasicArchiveModel", on_delete=models.CASCADE)
    locus = models.ForeignKey("geo.Locus", on_delete=models.CASCADE)
    detail = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "%s to %s" % (self.item.unittitle, self.locus.id.__str__())


class PhysDesc(models.Model):
    type = models.ForeignKey("PhysDescType", on_delete=models.CASCADE)
    desc = models.TextField(null=True, blank=True)
    item = models.ForeignKey(
        "BasicArchiveModel", null=True, blank=True,
        related_name="item_physdesc", on_delete=models.CASCADE
    )

    def __unicode__(self):
        return self.type.desc


    def __str__(self):
        return self.__unicode__()



class PhysDescType(models.Model):
    desc = models.CharField(max_length=50)

    def __unicode__(self):
        return self.desc


class Repository(models.Model):
    desc = models.CharField(max_length=100)

    def __unicode__(self):
        return self.desc

    class Meta:
        verbose_name_plural = "Repositories"


class Person(models.Model):
    surname = models.CharField(max_length=50)
    firstNames = models.CharField(max_length=60, null=True, blank=True)
    item = models.ManyToManyField(
        BasicArchiveModel, blank=True, related_name="person"
    )
    details = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.surname


class BibliographicReference(models.Model):
    item = models.ManyToManyField(
        BasicArchiveModel, blank=True, related_name="biblio_ref"
    )
    url = models.CharField(max_length=100, null=True, blank=True)
    details = models.TextField(null=True, blank=True)


class UnitId(models.Model):
    type = models.ForeignKey("UnitIdType", on_delete=models.CASCADE)
    desc = models.TextField(null=True, blank=True)
    item = models.ForeignKey("BasicArchiveModel", null=True, blank=True,
                             on_delete=models.CASCADE)

    def __unicode__(self):
        return self.type.desc


class UnitIdType(models.Model):
    desc = models.CharField(max_length=50)

    def __unicode__(self):
        return self.desc


class Note(models.Model):
    audience = models.ForeignKey("NoteAudience", on_delete=models.CASCADE)
    type = models.ForeignKey("NoteType", on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    item = models.ForeignKey(
        "BasicArchiveModel", null=True, blank=True, related_name="item_note",
        on_delete=models.CASCADE
    )

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


class Image(models.Model):
    item = models.ForeignKey("BasicArchiveModel", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
    desc = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.item.unittitle
