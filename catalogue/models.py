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

    def __str__(self):
        return self.__unicode__()


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

    def __str__(self):
        return self.__unicode__()


class Repository(models.Model):
    desc = models.CharField(max_length=100)

    def __unicode__(self):
        return self.desc

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name_plural = "Repositories"


class Person(models.Model):
    surname = models.CharField(max_length=50)
    firstNames = models.CharField(max_length=60, null=True, blank=True)
    item = models.ManyToManyField(
        BasicArchiveModel, blank=True, related_name="person"
    )
    details = models.TextField(null=True, blank=True)
    DateFrom = models.DateField(null=True, blank=True)
    DateTo = models.DateField(null=True, blank=True)
    referenceType = models.ForeignKey("ReferenceType",
                                      on_delete=models.CASCADE, null=True, blank=True)

    def get_description(self):
        desc = self.surname
        if len(self.firstNames) > 0:
            desc += ", " + self.firstNames
        if (self.DateFrom and self.DateTo):
            desc += "(" + str(self.DateFrom) + "-" + str(self.DateTo) + ")"
        elif self.DateFrom:
            desc += "(" + str(self.DateFrom) + ")"
        return desc

    def __unicode__(self):
        return self.surname

    def __str__(self):
        return self.__unicode__()


class AlternativeName(models.Model):
    surname = models.CharField(max_length=60, null=True, blank=True)
    forename = models.CharField(max_length=60, null=True, blank=True)
    referenceType = models.ForeignKey("ReferenceType",
                                      on_delete=models.CASCADE, null=True)
    DateFrom = models.DateField(null=True, blank=True)
    DateTo = models.DateField(null=True, blank=True)
    defaultName = models.BooleanField(default=False)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)

    def get_description(self):
        desc = self.surname
        if len(self.forename) > 0:
            desc += ", " + self.forename
        if (self.DateFrom and self.DateTo):
            desc += "(" + str(self.DateFrom) + "-" + str(self.DateTo) + ")"
        elif self.DateFrom:
            desc += "(" + str(self.DateFrom) + ")"
        return desc

    def __str__(self):
        return self.surname + " (Alias of " + Person.get_description() + ")"


class ReferenceType(models.Model):
    Description = models.TextField(blank=True)

    def __str__(self):
        return self.Description;


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

    def __str__(self):
        return self.__unicode__()


class UnitIdType(models.Model):
    desc = models.CharField(max_length=50)

    def __unicode__(self):
        return self.desc

    def __str__(self):
        return self.__unicode__()


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

    def __str__(self):
        return self.__unicode__()


class NoteAudience(models.Model):
    desc = models.CharField(max_length=50)

    def __unicode__(self):
        return self.desc

    def __str__(self):
        return self.__unicode__()


class NoteType(models.Model):
    desc = models.CharField(max_length=50)

    def __unicode__(self):
        return self.desc

    def __str__(self):
        return self.__unicode__()


class Level(models.Model):
    desc = models.CharField(max_length=50)

    def __unicode__(self):
        return self.desc

    def __str__(self):
        return self.__unicode__()


class Language(models.Model):
    desc = models.CharField(max_length=100)

    def __unicode__(self):
        return self.desc

    def __str__(self):
        return self.__unicode__()


class Image(models.Model):
    item = models.ForeignKey("BasicArchiveModel", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/")
    desc = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.item.unittitle

    def __str__(self):
        return self.__unicode__()
