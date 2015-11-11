# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Related_Locus_Type.reciprocal_name'
        db.add_column('geo_related_locus_type', 'reciprocal_name',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Locus_Type.reciprocal_name'
        db.delete_column('geo_locus_type', 'reciprocal_name')


    def backwards(self, orm):
        # Deleting field 'Related_Locus_Type.reciprocal_name'
        db.delete_column('geo_related_locus_type', 'reciprocal_name')

        # Adding field 'Locus_Type.reciprocal_name'
        db.add_column('geo_locus_type', 'reciprocal_name',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    models = {
        'geo.coordinate': {
            'Meta': {'object_name': 'Coordinate'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feature': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '7'}),
            'heritage': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Heritage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '7'}),
            'locus': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locus_coordinate'", 'to': "orm['geo.Locus']"}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '7'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'geo.geojson': {
            'Meta': {'object_name': 'Geojson'},
            'geojson': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locus': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'locus_geojson'", 'to': "orm['geo.Locus']"})
        },
        'geo.heritage': {
            'Meta': {'object_name': 'Heritage'},
            'accuracy': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hardware': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'recorded_by': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'geo.inscription': {
            'Meta': {'object_name': 'Inscription'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inscription_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'locus': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['geo.Locus']", 'null': 'True', 'through': "orm['geo.Inscription_Locus']", 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'geo.inscription_locus': {
            'Meta': {'unique_together': "(['inscription', 'locus', 'inscription_locus_type'],)", 'object_name': 'Inscription_Locus'},
            'context': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Inscription']"}),
            'inscription_locus_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Inscription_Locus_Type']"}),
            'locus': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Locus']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'geo.inscription_locus_type': {
            'Meta': {'object_name': 'Inscription_Locus_Type'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'geo.locus': {
            'Meta': {'ordering': "['name']", 'object_name': 'Locus'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'featuretype': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locus_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Locus_Type']", 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'pleiades_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'related_locus': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['geo.Locus']", 'through': "orm['geo.Related_Locus']", 'symmetrical': 'False'})
        },
        'geo.locus_type': {
            'Meta': {'object_name': 'Locus_Type'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'geo.locus_variant': {
            'Meta': {'object_name': 'Locus_Variant'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locus': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variants'", 'to': "orm['geo.Locus']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'geo.related_locus': {
            'Meta': {'unique_together': "(['subject', 'obj', 'related_locus_type'],)", 'object_name': 'Related_Locus'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'obj': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'object'", 'to': "orm['geo.Locus']"}),
            'related_locus_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geo.Related_Locus_Type']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subject'", 'to': "orm['geo.Locus']"})
        },
        'geo.related_locus_type': {
            'Meta': {'object_name': 'Related_Locus_Type'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'reciprocal_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['geo']