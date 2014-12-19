'''
.. py:module:: interjections
    :platform: Unix
    
Generate common English interjections for given stimulation. The available 
interjections have been created mostly according to this 
`site <http://www.vidarholen.net/contents/interjections/>`_.

Intended usage follows roughly this scheme:: 

    >>>import gensim, interjections
    >>>model = gensim.models.Word2Vec().load("/path/to/my/trained/model")
    >>>interjections.get('annoyed', model)
    'sheeeshh'
    >>>interjections.get('happiness', model)
    'whheee'


'''
from random import randint, choice

#: Threshold for filtering interjections if model is given. Only interjections 
#: that score higher than threshold for similarity can be accepted.
INTERJECTION_THRESHOLD = 0.40

# Available interjections in the form of (word, amounts, meaning, emotions, intensity, agreement).
# words: basic forms of the interjection
# amounts: tuples of integers with same length as words. Amount of possible repetitions for each character (for each basic form).
# meaning: out written meaning as a sentence
# emotions: typical complex emotions and attributes for the interjection
# intensity: usual intensity associated with the interjection, 0 = mild, 1 = normal, 2 = tense
# agreement: simple categorisation of the complex emotions, 0 = disagree, 1 = mixed, 2 = agree
interjections = [
    (('aah',), ((1,3,2),), "Help!", ('fright', 'shock'), 2, 0),
    (('aha', 'a-ha'), ((1,1,2), (1,1,1,2)), "I understand.", ('triumph', 'understanding'), 1, 2),
    (('ah', 'aah'), ((1,4), (1,2,3)), "OK, I see.", ('realization', 'understanding'), 1, 2),
    (('argh',), ((3,2,3,3),), "Damn!", ('annoyance', 'anger', 'frustration'), 2, 0),
    (('aw',), ((1,4),), "How sweet!", ('sentimental','approval', 'attachment'), 2, 2),
    (('aw', 'ohh'), ((1,2), (1,1,3)), "That's too bad.", ('pity', 'sorry'), 1, 2),
    (('bah',), ((1,1,3),), "Whatever.", ('dismissive', 'annoyance'), 1, 0),
    (('boo','booh'), ((1,1,3),(1,1,3,1)), "That's bad.", ('disapproval', 'contempt'), 1, 0),
    (('duh',), ((1,1,3),), "That's dumb.", ('annoyance',), 0, 0),
    (('eek',), ((1,4,2),), "Help!", ('surprise','scare'), 2, 1),
    (('eep',), ((1,3,1),), "Oh no!", ('surprise',), 1, 1, '!'),
    (('eh','huh'), ((1,3),(1,1,2)), "What?", ('misunderstanding',), 1, 1, '?'),
    (('eh','huh','eyh'), ((1,1),(1,1,1),(1,2,1)), "Is that right?", ('confirmation', 'understanding'), 0, 1),
    (('eww',), ((2,1,4),), "Disgusting.", ('disgust','dislike'), 2, 0),
    (('gah',), ((1,1,1),), "This is hopeless", ('exasperation', 'despair'), 1, 0),
    (('gee',), ((1,1,3),), "Really?", ('surprise','enthusiasm'), 2, 2),
    (('grr',), ((1,1,3),), "I'm angry.", ('anger', 'fury', 'rage'), 2, 0),
    (('hmm',), ((1,1,3),), "I wonder.", ('thoughtful', 'hesitation', 'wistful'), 2, 2),
    (('humph','hmph'), ((1,1,2,2,3),(1,3,2,3)), "I don't like this", ('annoyance', 'dislike', 'disbelief'), 0, 0),
    (('hah',), ((1,1,2),), "Funny.", ('hilarity','mirth'), 0, 2),
    (('haha','hahaha'), ((1,1,2,3),(1,1,2,1,1,3)), "Funny.", ('elation',), 1, 2),
    (('ich','yuck','yak'), ((1,1,2),(1,1,2,3),(1,1,2)), "Disgusting.", ('disgust','dislike'), 1, 0),
    (('meh',), ((1,1,3),), "I don't know", ('indifference','boredom'), 1, 1),
    (('mhm',), ((1,2,2),), "Yes.", ('agreement', 'approbation', 'approval'), 0, 2),
    (('mm',), ((1,4),), "Lovely.", ('pleasure', 'attachment'), 1, 2),
    (('muahaha','mwahaha','bwahaha'), ((1,1,1,2,1,2,3),(1,1,1,2,1,2,3),(1,1,1,2,1,2,3)), "I'm so evil.", ('evil','wicked','mischievous','ironic'), 1, 2),
    (('nah',), ((1,1,2),), "No.", ('disagreement',), 1, 0),
    (('oh',), ((1,3),), "I see.", ('realization',), 1, 0),
    (('ooh-la-la',), ((1,2,2,1,1,1,1,1,1),), "Fancy!", ('pleasure',), 2, 1),
    (('oops',), ((1,3,1,2),), "I didn't mean that.", ('surprise',), 1, 1),
    (('ow','ouch','yeow'), ((1,3),(2,1,2,3), (1,1,1,2)), "That hurts", ('pain',), 2, 0),
    (('pff','pfft'), ((1,1,3),(1,1,3,2)), "That's nothing.", ('downplay','annoyance'), 1, 0),
    (('phew',), ((1,1,2,3),), "That was close!", ('relief',), 1, 1),
    (('psst',), ((1,1,3,2),), "Whispering.", ('secretive','intimate'), 1, 1),
    (('sheesh',), ((1,1,1,2,2,2),), "I can't believe this!", ('exasperation','annoyance'), 1, 0),
    (('tsk-tsk',), ((1,1,1,1,1,1,1),), "Disappointing.", ('disappointment','contempt'), 1, 0),
    (('uhh', 'uhm', 'err'), ((1,1,3),(1,2,2),(1,1,3)), "Wait, I'm thinking.", ('wistful','thoughtful', 'reflective'), 1, 1),
    (('wee','whee'), ((1,1,3),(1,2,1,3)), "This is fun!", ('joy','excitement'), 1, 2),
    (('whoa',), ((1,2,1,1),), "Nice.", ('surprise','amazement'), 1, 2),
    (('wow',), ((2,3,3),), "Amazing!", ('impressed','astonished','awe'), 2, 2),
    (('yay',), ((1,1,3),), "Yes!", ('approval','happiness'), 1, 2),
    (('yeah',), ((1,3,2,3),), "Yes!", ('approval','agreement'), 1, 2),
]

def available():
    '''All available interjections.
    
    Get all available interjections as a list. Each item in the list corresponds 
    to one base interjection type. Each interjection type is a 6-part tuple with
    elements in following order:
    
    * words: tuple, basic forms of the interjection
    * amounts: tuple of tuples, amount of possible repetitions for  characters in each basic form. See :py:func:`adjust`.
    * meaning: written out meaning as a sentence
    * emotions: typical complex emotions and attributes for the interjection
    * intensity: usual intensity associated with the interjection, 0 = mild, 1 = normal, 2 = tense
    * agreement: simple categorisation of the complex emotions, 0 = disagree, 1 = mixed, 2 = agree
    
    :returns: list -- all available interjections  
    '''
    return interjections
    

def __weight(stimulation, model = None):
    '''Weight all available interjections based on the given stimulation and model.
    
    Given stimulation can be any textual content, but for best results should be
    an emotion, mood or reaction type.
    
    If given, the model is used to calculate similarities between stimulation
    and attributes associated to the interjections. It should have a ``similarity``-
    method, which takes as an argument two strings.
    
    If model is given, the returned list is sorted by the calculated similarities.
    Empty list is returned when no interjections can be associated with the
    given stimulation.
    
    :param stimulation: Stimulation which causes interjection
    :type stimulation: str or unicode
    :param model: The model to calculate similarities
    :type model: Word2Vec or similar
    :returns: list -- All interjections.  
    '''
    mood_interjections = []
    if model: 
        for i in interjections:
            cur_score = 0
            ems = []
            for em in i[3]:
                try:
                    sim = model.similarity(stimulation, em)
                except:
                    continue  
                ems.append(em)
                if sim > cur_score:
                    cur_score = sim
            cur_score = model.n_similarity([stimulation], ems)
            mood_interjections.append((cur_score, i))
        return sorted(mood_interjections, key = lambda x: x[0], reverse = True)
    else:
        for i in interjections:
            for em in i[3]:
                if em == stimulation:
                    mood_interjections.append((0, i[:3]))
    return mood_interjections


def get(stimulation, model = None):
    '''Get suitable interjection for given stimulation.
    
    Given stimulation can be any textual content, but for best results should be
    an emotion, mood or reaction type. 
    
    If given, the model is used to weight interjections for best performance.
    It should have a ``similarity``-method, which takes as an argument two 
    strings and returns their similarity (the higher the better). Example of a
    suitable model is, e.g. `gensim's Word2Vec <http://radimrehurek.com/gensim/models/word2vec.html>`_.
    
    .. note::
        
        If model is given, the stimulation string has to be recognized by the 
        model. If no model is given, then stimulation should be one of the words
        appearing in the available interjections 'emotions' part.
    
    :param stimulation: Stimulation which causes interjection
    :type stimulation: str or unicode
    :param model: The model to calculate similarities
    :type model: Word2Vec or similar
    :returns: tuple -- (str, str) Suitable interjection for given stimulation and its base form.
    '''
    inters = __weight(stimulation, model = model)
    if model is not None:
        inters = filter(lambda x: (x[0] > INTERJECTION_THRESHOLD and inters[0][0] - x[0] < 0.3), inters)
    if len(inters) == 0:
        return None
    inter = choice(inters)
    r = randint(0, len(inter[1][0])-1)
    return adjust(inter[1][0][r], inter[1][1][r]), inter[1][0][r]
                
    
def adjust(interjection, max_amounts):
    '''Adjust interjection to have natural variation as is common in social media.
    
    Interjection can be any short string, e.g 'ah' or 'um'. Each character
    is repeated in *[1,max_amounts[i]]* range, where *i* is the character's 
    index in the string.
    
    :param interjection: Short exclamation, e.g. 'ah' or 'um'.
    :type interjection: str or unicode
    :param max_amounts: Positive integers, same length as the stereotype string
    :type max_amounts: list
    :returns: str or unicode -- adjusted interjection string.
    '''
    counts = [(c, randint(1,max_amounts[i]))  for i,c in enumerate(interjection)]
    return reduce(lambda x,y: x+"".join([y[0] for r in xrange(y[1])]), counts, "")
  

