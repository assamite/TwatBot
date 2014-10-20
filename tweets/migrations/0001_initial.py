# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Color'
        db.create_table(u'tweets_color', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('html', self.gf('django.db.models.fields.CharField')(unique=True, max_length=7)),
            ('hex', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8)),
            ('rgb_r', self.gf('django.db.models.fields.IntegerField')()),
            ('rgb_g', self.gf('django.db.models.fields.IntegerField')()),
            ('rgb_b', self.gf('django.db.models.fields.IntegerField')()),
            ('l', self.gf('django.db.models.fields.FloatField')()),
            ('a', self.gf('django.db.models.fields.FloatField')()),
            ('b', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'tweets', ['Color'])

        # Adding unique constraint on 'Color', fields ['rgb_r', 'rgb_g', 'rgb_b']
        db.create_unique(u'tweets_color', ['rgb_r', 'rgb_g', 'rgb_b'])

        # Adding model 'BracketedColorBigram'
        db.create_table(u'tweets_bracketedcolorbigram', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_bracket', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('end_bracket', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('f', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'tweets', ['BracketedColorBigram'])

        # Adding unique constraint on 'BracketedColorBigram', fields ['start_bracket', 'w1', 'w2', 'end_bracket']
        db.create_unique(u'tweets_bracketedcolorbigram', ['start_bracket', 'w1', 'w2', 'end_bracket'])

        # Adding model 'ColorMap'
        db.create_table(u'tweets_colormap', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stereotype', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('base_color', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tweets.Color'])),
        ))
        db.send_create_signal(u'tweets', ['ColorMap'])

        # Adding model 'ColorUnigram'
        db.create_table(u'tweets_colorunigram', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('solid_compound', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('f', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'tweets', ['ColorUnigram'])

        # Adding model 'ColorUnigramSplit'
        db.create_table(u'tweets_colorunigramsplit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('original', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tweets.ColorUnigram'])),
        ))
        db.send_create_signal(u'tweets', ['ColorUnigramSplit'])

        # Adding unique constraint on 'ColorUnigramSplit', fields ['w1', 'w2']
        db.create_unique(u'tweets_colorunigramsplit', ['w1', 'w2'])

        # Adding model 'EveryColorBotTweet'
        db.create_table(u'tweets_everycolorbottweet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tweets.Color'])),
            ('tweeted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'tweets', ['EveryColorBotTweet'])

        # Adding model 'PluralColorBigram'
        db.create_table(u'tweets_pluralcolorbigram', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('singular', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('f', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'tweets', ['PluralColorBigram'])

        # Adding unique constraint on 'PluralColorBigram', fields ['w1', 'w2', 'singular']
        db.create_unique(u'tweets_pluralcolorbigram', ['w1', 'w2', 'singular'])

        # Adding model 'UnbracketedColorBigram'
        db.create_table(u'tweets_unbracketedcolorbigram', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('w1', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('w2', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('f', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal(u'tweets', ['UnbracketedColorBigram'])

        # Adding unique constraint on 'UnbracketedColorBigram', fields ['w1', 'w2']
        db.create_unique(u'tweets_unbracketedcolorbigram', ['w1', 'w2'])

        # Adding model 'Tweet'
        db.create_table(u'tweets_tweet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tweeted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('muse', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('context', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('color_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('color_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal(u'tweets', ['Tweet'])


    def backwards(self, orm):
        # Removing unique constraint on 'UnbracketedColorBigram', fields ['w1', 'w2']
        db.delete_unique(u'tweets_unbracketedcolorbigram', ['w1', 'w2'])

        # Removing unique constraint on 'PluralColorBigram', fields ['w1', 'w2', 'singular']
        db.delete_unique(u'tweets_pluralcolorbigram', ['w1', 'w2', 'singular'])

        # Removing unique constraint on 'ColorUnigramSplit', fields ['w1', 'w2']
        db.delete_unique(u'tweets_colorunigramsplit', ['w1', 'w2'])

        # Removing unique constraint on 'BracketedColorBigram', fields ['start_bracket', 'w1', 'w2', 'end_bracket']
        db.delete_unique(u'tweets_bracketedcolorbigram', ['start_bracket', 'w1', 'w2', 'end_bracket'])

        # Removing unique constraint on 'Color', fields ['rgb_r', 'rgb_g', 'rgb_b']
        db.delete_unique(u'tweets_color', ['rgb_r', 'rgb_g', 'rgb_b'])

        # Deleting model 'Color'
        db.delete_table(u'tweets_color')

        # Deleting model 'BracketedColorBigram'
        db.delete_table(u'tweets_bracketedcolorbigram')

        # Deleting model 'ColorMap'
        db.delete_table(u'tweets_colormap')

        # Deleting model 'ColorUnigram'
        db.delete_table(u'tweets_colorunigram')

        # Deleting model 'ColorUnigramSplit'
        db.delete_table(u'tweets_colorunigramsplit')

        # Deleting model 'EveryColorBotTweet'
        db.delete_table(u'tweets_everycolorbottweet')

        # Deleting model 'PluralColorBigram'
        db.delete_table(u'tweets_pluralcolorbigram')

        # Deleting model 'UnbracketedColorBigram'
        db.delete_table(u'tweets_unbracketedcolorbigram')

        # Deleting model 'Tweet'
        db.delete_table(u'tweets_tweet')


    models = {
        u'tweets.bracketedcolorbigram': {
            'Meta': {'ordering': "['-f']", 'unique_together': "(('start_bracket', 'w1', 'w2', 'end_bracket'),)", 'object_name': 'BracketedColorBigram'},
            'end_bracket': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'f': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_bracket': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'tweets.color': {
            'Meta': {'unique_together': "(('rgb_r', 'rgb_g', 'rgb_b'),)", 'object_name': 'Color'},
            'a': ('django.db.models.fields.FloatField', [], {}),
            'b': ('django.db.models.fields.FloatField', [], {}),
            'hex': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'html': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '7'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'l': ('django.db.models.fields.FloatField', [], {}),
            'rgb_b': ('django.db.models.fields.IntegerField', [], {}),
            'rgb_g': ('django.db.models.fields.IntegerField', [], {}),
            'rgb_r': ('django.db.models.fields.IntegerField', [], {})
        },
        u'tweets.colormap': {
            'Meta': {'object_name': 'ColorMap'},
            'base_color': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tweets.Color']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stereotype': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'tweets.colorunigram': {
            'Meta': {'ordering': "['-f']", 'object_name': 'ColorUnigram'},
            'f': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'solid_compound': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'tweets.colorunigramsplit': {
            'Meta': {'ordering': "['w1', 'w2']", 'unique_together': "(('w1', 'w2'),)", 'object_name': 'ColorUnigramSplit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tweets.ColorUnigram']"}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'tweets.everycolorbottweet': {
            'Meta': {'object_name': 'EveryColorBotTweet'},
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tweets.Color']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tweeted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'tweets.pluralcolorbigram': {
            'Meta': {'ordering': "['-f']", 'unique_together': "(('w1', 'w2', 'singular'),)", 'object_name': 'PluralColorBigram'},
            'f': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'singular': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'tweets.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'color_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'color_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'context': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'muse': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tweeted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        u'tweets.unbracketedcolorbigram': {
            'Meta': {'ordering': "['-f']", 'unique_together': "(('w1', 'w2'),)", 'object_name': 'UnbracketedColorBigram'},
            'f': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'w1': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'w2': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['tweets']