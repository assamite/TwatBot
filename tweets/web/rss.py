'''
.. py:module:: rss
    :platform: Unix

Interface for reading RSS feeds and extracting plain text articles from them.
'''
import re
import urllib
import feedparser
from bs4 import BeautifulSoup as BS

from ..utils import text

REUTERS_RSS_FEEDS = {
    'politics': 'http://feeds.reuters.com/Reuters/PoliticsNews',
    'science': 'http://feeds.reuters.com/reuters/scienceNews',
    'top news': 'http://feeds.reuters.com/reuters/topNews',
    'environment': 'http://feeds.reuters.com/reuters/environment',
    'arts & culture': 'http://feeds.reuters.com/news/artsculture'
}

#: Supported URL-formats.
SUPPORTED_FORMATS = [
    'reuters',                  
]

war_topic = ['war', 'terrorism', 'attack', 'dead', 'military']
arts_topic = ['arts', 'painting', 'music', 'acting', 'exhibition']
environment_topic = ['environment', 'climate', 'vegetation', 'animal', 'organism']
politics_topic = ['politics', 'legislation', 'government', 'party', 'president']
topics = {'war': war_topic, 'arts': arts_topic, 'environment': environment_topic, 'politics': politics_topic}

def get_feed(rss_url, max_items = 10):
    '''Get most recent entries from the given RSS feed.
    
    The returned entries are in the same format as created by `feedparser <http://pythonhosted.org/feedparser/>`_.
    
    :param rss_url: URL to the RSS feed
    :type rss_url: str
    :param max_items: Maximum amount of items returned from feed
    :type max_items: int
    :returns: list - feed's last entries
    '''
    feed = feedparser.parse(rss_url)
    return feed['entries'] if len(feed['entries']) < max_items else feed['entries'][:max_items]


def get_articles(rss_url, url_type='reuters', amount = 10, bow = True):
    '''Get most recent articles from the given RSS feed.
    
    Each article is returned as a dictionary with following contents:
    
    =====    =================================================
    Key      Value
    =====    =================================================
    title    Headline for the article
    url      URL for the article
    text     Plain text of the article.
    bow      Optional, bag-of-words extracted from the article
    =====    =================================================
    
    :param rss_url: URL to the RSS feed
    :type rss_url: str
    :param url_type: Format of the html-pages to parse for plain text article. See :py:SUPPORTED_FORMATS.
    :type url_type: str
    :param amount: Amount of articles to retrieve. For safety, should be in [1, 25].
    :type amount: int
    :param bow: Get also bag-of-words for each article. This is identical to calling :py:func:`utils.text.bow`.
    :type bow: bool
    :returns: list -- Parsed articles  
    '''
    if url_type not in SUPPORTED_FORMATS:
        raise ValueError('Given url_type: {} not in supported formats.'.format(url_type))
        
    entries = get_feed(rss_url, max_items = amount)
    ret = []
    for entry in entries:
        article = {}
        article['title'] = entry['title']
        article['url'] = entry['link']
        soup = _get_soup(entry['link'])
        article['text'] = _parse_article(soup, url_type = url_type)
        if bow:
            article['bow_counts'] = text.bow(article['text'], counts = True)
            article['bow'] = [w[0] for w in article['bow_counts']]
        ret.append(article)
    return ret
        
        
def _get_soup(url):
    html = urllib.urlopen(url).read()
    return BS(html)
     
        
def _parse_article(soup, url_type = None): 
    if url_type == 'reuters':
        return _parse_reuters(soup)      
    return ""
        
        
def _parse_reuters(soup):
    '''Parse Reuters html page for main article in plain text.
    
    Main article is assumed to be in DOM element with id = articleText.
    '''
    articleText = soup.find(id="articleText")
    p = articleText.findAll('p')[:-1] # last one is the reporters names
    text = reduce(lambda x,y: x+" "+(y.text).strip(), p, "").strip()
    text = re.sub("\s", " ", text)
    return text


def _get_similarity(model, topic, bow):
    fbow = []
    for w in bow:
        try:
            model.similarity('man', w)
        except:
            continue
        fbow.append(w)
    return model.n_similarity(topic, fbow)
    
    
def _get_similarities(model, topics, bow):
    fbow = []
    for w in bow:
        try:
            model.similarity('man', w)
        except:
            continue
        fbow.append(w)
    sims = {}
    for k, v in topics.items():
        sims[k] = model.n_similarity(v, fbow)
    return sims


def _test_topics(model, amount = 10, topics = topics):
    ret = {}
    for name, url in REUTERS_RSS_FEEDS.items():
        print "{0}:".format(name.upper())
        ret[name] = []
        articles = get_articles(url, amount = amount)
        for a in articles:
            sims = _get_similarities(model, topics, a['bow'])
            s = sorted(sims.items(), key = lambda x: x[1], reverse = True)
            a['topics'] = sims
            print "\t{0} ({1})".format(a['title'].upper(), a['url'])
            for t in s:
                print "\t\t{0:<20}{1}".format(t[0], t[1]) 
            ret[name].append(a)
        print 
    return ret
            



    