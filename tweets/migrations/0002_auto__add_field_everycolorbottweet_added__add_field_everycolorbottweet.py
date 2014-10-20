# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'EveryColorBotTweet.added'
        db.add_column(u'tweets_everycolorbottweet', 'added',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'EveryColorBotTweet.tweet_id'
        db.add_column(u'tweets_everycolorbottweet', 'tweet_id',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'EveryColorBotTweet.added'
        db.delete_column(u'tweets_everycolorbottweet', 'added')

        # Deleting field 'EveryColorBotTweet.tweet_id'
        db.delete_column(u'tweets_everycolorbottweet', 'tweet_id')


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
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tweets.Color']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tweet_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
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