from django.contrib import admin
from tweets.models import ColorMap, EveryColorBotTweet, UnbracketedColorBigram
from tweets.models import ColorUnigram, BracketedColorBigram, PluralColorBigram
from tweets.models import Color, ColorUnigramSplit, Tweet

admin.site.register(Color)
admin.site.register(ColorMap)
admin.site.register(EveryColorBotTweet)
admin.site.register(UnbracketedColorBigram)
admin.site.register(ColorUnigram)
admin.site.register(ColorUnigramSplit)
admin.site.register(BracketedColorBigram)
admin.site.register(PluralColorBigram)
admin.site.register(Tweet)
