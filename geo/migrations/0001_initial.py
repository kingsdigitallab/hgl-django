# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Heritage'
        db.create_table('geo_heritage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('recorded_by', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('hardware', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('accuracy', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('geo', ['Heritage'])

        # Adding model 'Locus_Type'
        db.create_table('geo_locus_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('geo', ['Locus_Type'])

        # Adding model 'Locus'
        db.create_table('geo_locus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('pleiades_uri', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('locus_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Locus_Type'], null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('geo', ['Locus'])

        # Adding model 'Coordinate'
        db.create_table('geo_coordinate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('locus', self.gf('django.db.models.fields.related.ForeignKey')(related_name='locus_coordinate', to=orm['geo.Locus'])),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=7)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=7)),
            ('heritage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Heritage'])),
            ('feature', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('geo', ['Coordinate'])

        # Adding model 'Geojson'
        db.create_table('geo_geojson', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('locus', self.gf('django.db.models.fields.related.ForeignKey')(related_name='locus_geojson', to=orm['geo.Locus'])),
            ('geojson', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('geo', ['Geojson'])

        # Adding model 'Related_Locus_Type'
        db.create_table('geo_related_locus_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('geo', ['Related_Locus_Type'])

        # Adding model 'Related_Locus'
        db.create_table('geo_related_locus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subject', to=orm['geo.Locus'])),
            ('obj', self.gf('django.db.models.fields.related.ForeignKey')(related_name='object', to=orm['geo.Locus'])),
            ('related_locus_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Related_Locus_Type'])),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('geo', ['Related_Locus'])

        # Adding unique constraint on 'Related_Locus', fields ['subject', 'obj', 'related_locus_type']
        db.create_unique('geo_related_locus', ['subject_id', 'obj_id', 'related_locus_type_id'])

        # Adding model 'Locus_Variant'
        db.create_table('geo_locus_variant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('locus', self.gf('django.db.models.fields.related.ForeignKey')(related_name='variants', to=orm['geo.Locus'])),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('geo', ['Locus_Variant'])

        # Adding model 'Inscription'
        db.create_table('geo_inscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inscription_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('geo', ['Inscription'])

        # Adding model 'Inscription_Locus_Type'
        db.create_table('geo_inscription_locus_type', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('geo', ['Inscription_Locus_Type'])

        # Adding model 'Inscription_Locus'
        db.create_table('geo_inscription_locus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Inscription'])),
            ('locus', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Locus'])),
            ('inscription_locus_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['geo.Inscription_Locus_Type'])),
            ('context', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('note', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('geo', ['Inscription_Locus'])

        # Adding unique constraint on 'Inscription_Locus', fields ['inscription', 'locus', 'inscription_locus_type']
        db.create_unique('geo_inscription_locus', ['inscription_id', 'locus_id', 'inscription_locus_type_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Inscription_Locus', fields ['inscription', 'locus', 'inscription_locus_type']
        db.delete_unique('geo_inscription_locus', ['inscription_id', 'locus_id', 'inscription_locus_type_id'])

        # Removing unique constraint on 'Related_Locus', fields ['subject', 'obj', 'related_locus_type']
        db.delete_unique('geo_related_locus', ['subject_id', 'obj_id', 'related_locus_type_id'])

        # Deleting model 'Heritage'
        db.delete_table('geo_heritage')

        # Deleting model 'Locus_Type'
        db.delete_table('geo_locus_type')

        # Deleting model 'Locus'
        db.delete_table('geo_locus')

        # Deleting model 'Coordinate'
        db.delete_table('geo_coordinate')

        # Deleting model 'Geojson'
        db.delete_table('geo_geojson')

        # Deleting model 'Related_Locus_Type'
        db.delete_table('geo_related_locus_type')

        # Deleting model 'Related_Locus'
        db.delete_table('geo_related_locus')

        # Deleting model 'Locus_Variant'
        db.delete_table('geo_locus_variant')

        # Deleting model 'Inscription'
        db.delete_table('geo_inscription')

        # Deleting model 'Inscription_Locus_Type'
        db.delete_table('geo_inscription_locus_type')

        # Deleting model 'Inscription_Locus'
        db.delete_table('geo_inscription_locus')


    models = {
        'geo.coordinate': {
            'Meta': {'object_name': 'Coordinate'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feature': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
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
            'note': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['geo']