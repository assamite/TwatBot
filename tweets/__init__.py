from django.db import connection

__REQUIRED_TABLES = [
    u'tweets_bracketedcolorbigram', 
    u'tweets_color', 
    u'tweets_colormap', 
    u'tweets_colorunigram', 
    u'tweets_colorunigramsplit', 
    u'tweets_everycolorbottweet', 
    u'tweets_pluralcolorbigram', 
    u'tweets_unbracketedcolorbigram'
]

__citn = connection.introspection.table_names()

# Only import if all the required tables are in the database
if all([(t in __citn) for t in  __REQUIRED_TABLES]):
    from color_semantics import ColorSemantics
    COLOR_SEMANTICS = ColorSemantics()