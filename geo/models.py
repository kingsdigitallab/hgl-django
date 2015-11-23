from django.contrib.contenttypes.models import ContentType
#from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry

#===================================================================================================
# Dependencies:
#   - py25-mysql    py25-mysql 1.2.2    Python interface to mysql
#   - py25-ldap     py25-ldap 2.3.5     Object-oriented api for python to access LDAP directory servers
#===================================================================================================

#
class Heritage(models.Model):
    name = models.CharField(blank = False, max_length = 200, null = False, unique = True)
    recorded_by = models.CharField(blank = True, max_length = 200, null = True)
    hardware = models.CharField(blank = True, max_length = 200, null = True)
    accuracy = models.CharField(blank = True, max_length = 10, null = True)
    note = models.TextField(blank = True, null = True)
    modified = models.DateTimeField(auto_now = True, blank = False, null = False)
    created = models.DateTimeField(auto_now_add = True, blank = False, null = False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Provenance'
    
#
class Locus_Type(models.Model):
    name = models.CharField(blank = False, max_length = 255, null = False, unique = True)
    note = models.TextField(blank = True, null = True)
    modified = models.DateTimeField(auto_now = True, blank = False, null = False)
    created = models.DateTimeField(auto_now_add = True, blank = False, null = False)
    
    class Meta:
        verbose_name = 'Location Type'
        verbose_name_plural = 'Location Types'
    
    def __unicode__(self):
        return self.name

#
class Locus(models.Model):
    # Changing display name of field to fit new regime from name to descriptor
    name = models.CharField(blank = False, max_length = 200, null = False, unique = True,verbose_name='Descriptor')
    geonames_id = models.IntegerField(null=True,blank=True)
    pleiades_uri = models.URLField(blank = True, max_length = 200, null = True) #, verify_exists = True)
    locus_type = models.ForeignKey(Locus_Type, blank = True, null = True)
    related_locus = models.ManyToManyField('self', symmetrical = False, through = 'Related_Locus')
    FEATURE_FIELD_TYPE = (
        (0, 'point'),
        (1, 'line'),
        (2, 'polygon'),
    )
    #add column 'featuretype' for table 'geo_locus'
    featuretype = models.IntegerField(choices=FEATURE_FIELD_TYPE,verbose_name='Geometry type')
    featuretype_fk = models.ManyToManyField('FeatureTypes',null=True,blank=True)
    note = models.TextField(blank = True, null = True,verbose_name='Notes',help_text='Use sparingly!')
    modified = models.DateTimeField(auto_now = True, blank = False, null = False)
    created = models.DateTimeField(auto_now_add = True, blank = False, null = False)

    @staticmethod
    def autocomplete_search_fields():
            return ("name__icontains",) 

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        ordering = ['name']

    def __unicode__(self):
        return self.name
    
    ##return the value of featuretype value before save
    #def getType(self):
    #    return self.featuretype
class FeatureTypes(models.Model):
    description =  models.CharField(max_length=50)
    def __unicode__(self):
        return u'%s' % self.description

    class Meta:
        ordering = ('description',)

#
class Coordinate(models.Model):
    locus = models.ForeignKey(Locus, related_name='locus_coordinate')
    latitude = models.DecimalField(blank = False, decimal_places = 7, max_digits = 10, null = False)
    longitude = models.DecimalField(blank = False, decimal_places = 7, max_digits = 10, null = False)
    #add column 'height' for table 'geo_coordinate'
    height = models.DecimalField(blank = True, decimal_places = 7, max_digits = 10, null = True)
    heritage = models.ForeignKey(Heritage)
    third_party_uri = models.CharField(max_length=500,null=True,blank=True)
    feature = models.CharField(blank = True, max_length = 200, null = True)
    note = models.TextField(blank = True, null = True)
    modified = models.DateTimeField(auto_now = True, blank = False, null = False)
    created = models.DateTimeField(auto_now_add = True, blank = False, null = False)
    point = models.PointField(null=True,blank=True)
    objects = models.GeoManager()
   

    def __unicode__(self):
        return str(self.latitude) + ', ' + str(self.longitude) + ', ' + str(self.height)

    def save(self,*args,**kwargs):
        if self.latitude and self.longitude:
            self.point = GEOSGeometry( u'POINT (%s %s)' % ( str(self.longitude) , str(self.latitude) ) ) 
        super(Coordinate,self).save(*args,**kwargs)   




#
#add table 'geo_geojson' for database
# NJ Probably redundant ?? Will remoe from admin...
class Geojson(models.Model):
    locus = models.ForeignKey(Locus, related_name='locus_geojson')
    geojson = models.TextField(blank = True, null = True)

    def __unicode__(self):
        return self.geojson
#
class Related_Locus_Type(models.Model):
    name = models.CharField(blank = False, max_length = 255, null = False, unique = True)
    reciprocal_name = models.CharField(blank = True, max_length = 255, null = True, unique = False)
    note = models.TextField(blank = True, null = True)
    modified = models.DateTimeField(auto_now = True, blank = False, null = False)
    created = models.DateTimeField(auto_now_add = True, blank = False, null = False)

    class Meta:
        verbose_name = 'Related Location Type'
        verbose_name_plural = 'Related Location Types'
    
    def __unicode__(self):
        return self.name

#
class Related_Locus(models.Model):
    subject = models.ForeignKey(Locus, related_name="child",verbose_name='Child')
    obj = models.ForeignKey(Locus, related_name="parent", verbose_name='Parent')
    related_locus_type = models.ForeignKey(Related_Locus_Type,verbose_name='Relationship')
    note = models.TextField(blank = True, null = True)
    modified = models.DateTimeField(auto_now = True, blank = False, null = False)
    created = models.DateTimeField(auto_now_add = True, blank = False, null = False)
    # new time fields NJ
    date_from =  models.DateTimeField(blank=True, null=True)
    date_to =  models.DateTimeField(blank=True, null=True)

    def reciprocal_name(self):
        return u'%s' % self.related_locus_type.reciprocal_name
    
    class Meta:
        unique_together = ['subject', 'obj', 'related_locus_type']
        verbose_name = 'Related Location'
        verbose_name_plural = 'Related Locations'
        
    def __unicode__(self):
        return self.subject.name + ": " + self.related_locus_type.name + ": " + self.obj.name

#
class Locus_Variant(models.Model):
    name = models.CharField(blank = False, max_length = 200, null = False, unique = True)
    locus = models.ForeignKey(Locus,related_name = 'variants')
    
    note = models.TextField(blank = True, null = True)
    modified = models.DateTimeField(auto_now = True, blank = False, null = False)
    created = models.DateTimeField(auto_now_add = True, blank = False, null = False)
    
    class Meta:
        verbose_name = 'Variant Name'
        verbose_name_plural = 'Variant Names'
        
    def __unicode__(self):
        return self.name

class VariantAttestation(models.Model):
    name_variant =  models.ForeignKey('Locus_Variant')
    author = models.ForeignKey('Author',null=True,blank=True)
    title = models.ForeignKey('Publication',null=True,blank=True)
    page_reference = models.CharField(max_length=30,null=True,blank=True)
    notes = models.TextField(null=True,blank=True)
    link = models.CharField(max_length=500,null=True,blank=True)

    def __unicode__(self):
        return u'%s, attestation %s' % (self.name_variant,self.pk)


class Author(models.Model):
    person = models.BooleanField(default=True)
    family_or_institution_name = models.CharField(max_length=50,null=True,blank=True)
    given_names = models.CharField(max_length=50,null=True,blank=True)
    date = models.IntegerField(null=True,blank=True)

    def __unicode__(self):
        return u'%s' % self.family_or_institution_name


class Publication(models.Model):
    publication_type =  models.ForeignKey('PublicationType',null=True,blank=True)
    title = models.CharField(max_length=150)

    def __unicode__(self):
        return u'%s' % self.title


class PublicationType(models.Model):
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return u'%s' % self.description

#
class Inscription(models.Model):
    inscription_id = models.CharField(blank = False, max_length = 15, null = False, unique = True)
    title = models.CharField(blank = False, max_length = 256, null = False)
    locus = models.ManyToManyField(Locus, blank = True, null = True, through = 'Inscription_Locus')
    
    note = models.TextField(blank = True, null = True)
    modified = models.DateTimeField(auto_now = True, blank = False, null = False)
    created = models.DateTimeField(auto_now_add = True, blank = False, null = False)


    def __unicode__(self):
        return self.inscription_id + ': ' + self.title

#
class Inscription_Locus_Type(models.Model):
    name = models.CharField(blank = False, max_length = 255, null = False, unique = True)

    note = models.TextField(blank = True, null = True)
    modified = models.DateTimeField(auto_now = True, blank = False, null = False)
    created = models.DateTimeField(auto_now_add = True, blank = False, null = False)

    class Meta:
        verbose_name = 'Inscription Location Type'
        verbose_name_plural = 'Inscription Location Types'

    def __unicode__(self):
        return self.name
        
#
class Inscription_Locus(models.Model):
    inscription = models.ForeignKey(Inscription)
    locus = models.ForeignKey(Locus)
    inscription_locus_type = models.ForeignKey(Inscription_Locus_Type)
    context = models.TextField(blank = True, null = True)

    note = models.TextField(blank = True, null = True)
    modified = models.DateTimeField(auto_now = True, blank = False, null = False)
    created = models.DateTimeField(auto_now_add = True, blank = False, null = False)
    
    class Meta:
        verbose_name = 'Inscription Location'
        verbose_name_plural = 'Inscriptions Locations'
        unique_together = ['inscription', 'locus', 'inscription_locus_type']


   
