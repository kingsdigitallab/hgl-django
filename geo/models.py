# from django.db import models
import requests
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.geos import MultiPoint
from django.db.models import Manager as GeoManager


# ===================================================================================================
# Dependencies:
#   - py25-mysql    py25-mysql 1.2.2    Python interface to mysql
#   - py25-ldap     py25-ldap 2.3.5     Object-oriented api for python to
#   access LDAP directory servers

# ===================================================================================================

#
class Heritage(models.Model):
    name = models.CharField(blank=False, max_length=200, null=False,
                            unique=True)
    recorded_by = models.CharField(blank=True, max_length=200, null=True)
    hardware = models.CharField(blank=True, max_length=200, null=True)
    accuracy = models.CharField(blank=True, max_length=10, null=True)
    note = models.TextField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Provenance'


#
class Locus_Type(models.Model):
    name = models.CharField(blank=False, max_length=255, null=False,
                            unique=True)
    note = models.TextField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    class Meta:
        verbose_name = 'Location Type'
        verbose_name_plural = 'Location Types'

    def __unicode__(self):
        return self.name


#
class Locus(models.Model):
    # Changing display name of field to fit new regime from name to descriptor
    name = models.CharField(blank=False, max_length=200, null=False,
                            unique=True, verbose_name='Descriptor')
    attestation = models.CharField(max_length=500, null=True, blank=True,
                                   help_text="(for default name, descriptor)")
    geonames_id = models.IntegerField(null=True, blank=True, \
                                      help_text='Redundant field, '
                                                'see external URI below')
    pleiades_uri = models.URLField(blank=True, max_length=200, null=True, \
                                   help_text='Redundant field, see external '
                                             'URI below')
    locus_type = models.ForeignKey(Locus_Type, blank=True, null=True,
                                   on_delete=models.CASCADE)
    related_locus = models.ManyToManyField('self', symmetrical=False,
                                           through='Related_Locus')
    FEATURE_FIELD_TYPE = (
        (0, 'point'),
        (1, 'line'),
        (2, 'polygon'),
    )
    # add column 'featuretype' for table 'geo_locus'
    featuretype = models.IntegerField(choices=FEATURE_FIELD_TYPE,
                                      verbose_name='Geometry type', null=True,
                                      blank=True)
    featuretype_fk = models.ManyToManyField('FeatureTypes', null=True,
                                            blank=True)
    note = models.TextField(blank=True, null=True, verbose_name='Notes',
                            help_text='Use sparingly!')
    modified = models.DateTimeField(auto_now=True, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    # Adding GeoJson storage
    # JSON Field Postgres only so storing as unvalidated Text here
    geojsion = models.TextField(blank=True, null=True)
    geojson_provenance = models.TextField(blank=True, null=True)

    @staticmethod
    def autocomplete_search_fields():
        return ("name__icontains",)

        # retrieve all geonames alternate names and place in variant

    def getAltGeonames(self):
        l = Locus.objects.get(pk=self.id)
        if l.geonames_id:
            geoNamesUrl = 'http://api.geonames.org/getJSON?geonameId=' + str(
                l.geonames_id) + '&username=hergazlib'
            response = requests.get(geoNamesUrl)
            json = response.json()
            jsonAlt = json['alternateNames']
            for n in jsonAlt:
                vn = Locus_Variant()
                vn.name = n['name']
                vn.locus = l
                # Check that we don't already that name...
                if Locus_Variant.objects.filter(name=n['name']).count() == 0:
                    # Try to record language code if possible
                    try:
                        code = n['lang']
                        if code == 'link':
                            pass
                        else:
                            try:
                                vn.language = Language.objects.get(code=code)
                            except Exception:
                                pass
                    except Exception:
                        pass
                    vn.save()

    def getDescendants(self):
        related_loci = []
        for rel in Related_Locus.objects.filter(obj=self).filter(
                related_locus_type__name='forms part of'):
            related_loci.append(rel.subject)
        return related_loci

    def getConvexHull(self):
        # Find all points that descendants of this Locus
        descendants = self.getDescendants()
        i = 0
        while i < 5:
            i = i + 1
            for d in descendants:
                for ds in d.getDescendants():
                    if ds not in descendants:
                        descendants.append(ds)
        points = []
        for c in descendants:
            for p in c.locus_coordinate.all():
                points.append(p.point)

        coords = []
        mp = MultiPoint(points)
        geojson = {}
        if mp.convex_hull.coords.__len__() > 0:
            for css in mp.convex_hull.coords[0]:
                coords.append([css[0], css[1]])
        else:
            coords.append([18.018, 30.449])
            geojson["properties"] = {}
        geojson["properties"]["bad"] = "bad"
        # geojson = {}
        geojson["type"] = "Feature"
        geojson["geometry"] = {}
        geojson["geometry"]["type"] = "Polygon"
        geojson["geometry"]["coordinates"] = []
        geojson["geometry"]["coordinates"].append(coords)

        # Debug responder
        return geojson

        # return points

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        ordering = ['name']

    def __unicode__(self):
        return self.name

    ##return the value of featuretype value before save
    # def getType(self):
    #    return self.featuretype


class FeatureTypes(models.Model):
    description = models.CharField(max_length=50)
    category = models.ForeignKey('FeatureCategory', null=True, blank=True,
                                 on_delete=models.CASCADE)

    def __unicode__(self):
        return '%s' % self.description

    class Meta:
        ordering = ('description',)
        verbose_name_plural = "Feature types"


class FeatureCategory(models.Model):
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s' % self.description

    class Meta:
        ordering = ('description',)
        verbose_name_plural = "Feature categories"

    #


class Coordinate(models.Model):
    locus = models.ForeignKey(Locus, related_name='locus_coordinate',
                              on_delete=models.CASCADE)
    latitude = models.DecimalField(blank=False, decimal_places=7,
                                   max_digits=10, null=False)
    longitude = models.DecimalField(blank=False, decimal_places=7,
                                    max_digits=10, null=False)
    # add column 'height' for table 'geo_coordinate'
    height = models.DecimalField(blank=True, decimal_places=3, max_digits=11,
                                 null=True)
    heritage = models.ForeignKey(Heritage, on_delete=models.CASCADE)
    third_party_uri = models.CharField(max_length=500, null=True, blank=True)
    feature = models.CharField(blank=True, max_length=200, null=True)
    note = models.TextField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    point = models.PointField(null=True, blank=True)
    objects = GeoManager()

    def __unicode__(self):
        return str(self.latitude) + ', ' + str(self.longitude) + ', ' + str(
            self.height)

    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
            self.point = GEOSGeometry(
                'POINT (%s %s)' % (str(self.longitude), str(self.latitude)))
        super(Coordinate, self).save(*args, **kwargs)

    #


# add table 'geo_geojson' for database
# NJ Probably redundant ?? Will remoe from admin...
class Geojson(models.Model):
    locus = models.ForeignKey(Locus, related_name='locus_geojson',
                              on_delete=models.CASCADE)
    geojson = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.geojson


#
class Related_Locus_Type(models.Model):
    name = models.CharField(blank=False, max_length=255, null=False,
                            unique=True)
    reciprocal_name = models.CharField(blank=True, max_length=255, null=True,
                                       unique=False)
    note = models.TextField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    class Meta:
        verbose_name = 'Related Location Type'
        verbose_name_plural = 'Related Location Types'
        ordering = ['name', 'reciprocal_name', ]

    def __unicode__(self):
        return self.name


#
class Related_Locus(models.Model):
    subject = models.ForeignKey(Locus, related_name="child",
                                verbose_name='Child', on_delete=models.CASCADE)
    obj = models.ForeignKey(Locus, related_name="parent",
                            verbose_name='Parent', on_delete=models.CASCADE)
    related_locus_type = models.ForeignKey(Related_Locus_Type,
                                           verbose_name='Relationship',
                                           on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    # new time fields NJ
    date_from = models.DateTimeField(blank=True, null=True)
    date_to = models.DateTimeField(blank=True, null=True)
    period = models.ForeignKey('Period', blank=True, null=True,
                               on_delete=models.CASCADE)

    def reciprocal_name(self):
        return '%s' % self.related_locus_type.reciprocal_name

    class Meta:
        unique_together = ['subject', 'obj', 'related_locus_type']
        verbose_name = 'Related Location'
        verbose_name_plural = 'Related Locations'
        ordering = ["subject", "obj"]

    def __unicode__(self):
        return self.subject.name + ": " + self.related_locus_type.name + ": " + self.obj.name


class Period(models.Model):
    description = models.CharField(max_length=50)

    # unit = models.ForeignKey('Locus')

    class Meta:
        ordering = ['description', ]

    def __unicode__(self):
        return '%s' % (self.description)  # ,self.unit.name)


#
class Locus_Variant(models.Model):
    name = models.CharField(blank=False, max_length=200, null=False,
                            unique=False)
    locus = models.ForeignKey(Locus, related_name='variants',
                              on_delete=models.CASCADE)
    language = models.ForeignKey('Language', null=True, blank=True,
                                 on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True)
    attestation = models.CharField(max_length=500, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    provenance = models.ForeignKey('Heritage', null=True, blank=True,
                                   on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Variant Name'
        verbose_name_plural = 'Variant Names'
        ordering = ["name", ]

    def __unicode__(self):
        return self.name


class Language(models.Model):
    code = models.CharField(max_length=5)
    en_name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ('en_name',)

    def __unicode__(self):
        en_name = ''
        if self.en_name:
            en_name = self.en_name
        return '%s (%s)' % (self.code, en_name)


class VariantAttestation(models.Model):
    name_variant = models.ForeignKey('Locus_Variant', on_delete=models.CASCADE)
    author = models.ForeignKey('Author', null=True, blank=True,
                               on_delete=models.CASCADE)
    title = models.ForeignKey('Publication', null=True, blank=True,
                              on_delete=models.CASCADE)
    page_reference = models.CharField(max_length=30, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return '%s, attestation %s' % (self.name_variant, self.pk)


class Author(models.Model):
    person = models.BooleanField(default=True)
    family_or_institution_name = models.CharField(max_length=50, null=True,
                                                  blank=True)
    given_names = models.CharField(max_length=50, null=True, blank=True)
    date = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.family_or_institution_name


class Publication(models.Model):
    publication_type = models.ForeignKey('PublicationType', null=True,
                                         blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)

    def __unicode__(self):
        return '%s' % self.title


class PublicationType(models.Model):
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s' % self.description


#
class Inscription(models.Model):
    inscription_id = models.CharField(blank=False, max_length=15, null=False,
                                      unique=True)
    title = models.CharField(blank=False, max_length=256, null=False)
    locus = models.ManyToManyField(Locus, blank=True, null=True,
                                   through='Inscription_Locus')

    note = models.TextField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    def __unicode__(self):
        return self.inscription_id + ': ' + self.title


#
class Inscription_Locus_Type(models.Model):
    name = models.CharField(blank=False, max_length=255, null=False,
                            unique=True)

    note = models.TextField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    class Meta:
        verbose_name = 'Inscription Location Type'
        verbose_name_plural = 'Inscription Location Types'

    def __unicode__(self):
        return self.name


#
class Inscription_Locus(models.Model):
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE)
    locus = models.ForeignKey(Locus, on_delete=models.CASCADE)
    inscription_locus_type = models.ForeignKey(Inscription_Locus_Type,
                                               on_delete=models.CASCADE)
    context = models.TextField(blank=True, null=True)

    note = models.TextField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=False, null=False)

    class Meta:
        verbose_name = 'Inscription Location'
        verbose_name_plural = 'Inscriptions Locations'
        unique_together = ['inscription', 'locus', 'inscription_locus_type']


class ExternalURI(models.Model):
    uri = models.TextField()
    locus = models.ForeignKey(Locus, on_delete=models.CASCADE)
    authority = models.ForeignKey(
        'Authority', null=True, blank=True,
        help_text="Redundant - use Provenance below", on_delete=models.CASCADE
    )
    provenance = models.ForeignKey('Heritage', null=True, blank=True,
                                   on_delete=models.CASCADE)

    def __unicode__(self):
        return '%s, %s' % (self.locus.name, self.uri)


class Authority(models.Model):
    name = models.CharField(max_length=75)
    base_uri = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.name

    class Meta:
        verbose_name_plural = "Authorities"
