from django.contrib import admin
from tweets.models import ColorMap, EveryColorBotTweet, UnbracketedColorBigram
from tweets.models import ColorUnigram, BracketedColorBigram, PluralColorBigram
from tweets.models import Color, ColorUnigramSplit, Tweet

class TweetAdmin(admin.ModelAdmin):
    list_display = ('tweeted', 'message','color_name', 'color_code', 'value')
    list_editable = ('message','color_name', 'color_code', 'value')
    
class EveryColorBotTweetAdmin(admin.ModelAdmin):
    list_display = ('added', 'url', 'color', 'tweeted')
    list_editable = ('tweeted',)

admin.site.register(Color)
admin.site.register(ColorMap)
admin.site.register(EveryColorBotTweet, EveryColorBotTweetAdmin)
admin.site.register(UnbracketedColorBigram)
admin.site.register(ColorUnigram)
admin.site.register(ColorUnigramSplit)
admin.site.register(BracketedColorBigram)
admin.site.register(PluralColorBigram)
admin.site.register(Tweet, TweetAdmin)
