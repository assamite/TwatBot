#Encoding: utf-8
'''
.. py:module:: emotion
    :platform: Unix
    
Shallow computational model for `Lövheim cube of emotion 
<http://upload.wikimedia.org/wikipedia/commons/c/c1/L%C3%B6vheim_cube_of_emotion.jpg>`_. 

The model maps neurotransmitter levels (serotonin, noradrenaline and dopamine) 
into cube with each dimension from -1 to 1. The dimensions are mapped in the 
following order:

    * 0: serotonin
    * 1: noradrenaline
    * 2: dopamine
    
Each emotion is placed on a surface of a unit sphere with has the same center as 
the cube. User of the module can then query for emotions closest to the certain
point or vector using py:func:`get_closest`.
'''
import itertools
import numpy as np 
import sys
from random import choice
import emotions

AXIS = ((0, 'serotonin'), (1, 'noradrenaline'), (2, 'dopamine'))

EMOTIONS = emotions.EMOTIONS

"""
BASE_EMOTION_MAP = {
    (0, 0, 0): ('shame', 'humiliation'),
    (0, 1, 0): ('distress', 'anguish'),
    (0, 1, 1): ('anger', 'rage'),
    (0, 0, 1): ('fear', 'terror'),
    (1, 0, 0): ('contempt', 'disgust'),
    (1, 1, 0): ('surprise',),
    (1, 0, 1): ('enjoyment', 'joy'),
    (1, 1, 1): ('interest', 'excitement')
}
"""

BASE_EMOTION_MAP = {
    (-1,-1,-1): ('shame', 'humiliation'),
    (-1, 1,-1): ('distress', 'anguish'),
    (-1, 1, 1): ('anger', 'rage'),
    (-1,-1, 1): ('fear', 'terror'),
    ( 1,-1,-1): ('contempt', 'disgust'),
    ( 1, 1,-1): ('surprise',),
    ( 1,-1, 1): ('enjoyment', 'joy'),
    ( 1, 1, 1): ('interest', 'excitement')
}


VECTORS = {
    (-1,-1,-1): np.array((-1,-1,-1)),
    (-1, 1,-1): np.array((-1, 1,-1)),
    (-1, 1, 1): np.array((-1, 1, 1)),
    (-1,-1, 1): np.array((-1,-1, 1)),
    ( 1,-1,-1): np.array(( 1,-1,-1)),
    ( 1, 1,-1): np.array(( 1, 1,-1)),
    ( 1,-1, 1): np.array(( 1,-1, 1)),
    ( 1, 1, 1): np.array(( 1, 1, 1)),          
}

"""
def map_stimulation(stimulation, model):
    '''Map stimulation to the Lövheim cube based on the base emotions and their
    dimensions.'''
    sims = {}
    for k,v in BASE_EMOTION_MAP.items():
        s = []
        for emotion in v:
            s.append(model.similarity(stimulation, emotion))
        sims[k] = max(s)
    keys = BASE_EMOTION_MAP.keys()
    diffs = {(1, 0, 0): 0.5, (0, 1, 0): 0.5, (0, 0, 1): 0.5}
    for t1, t2 in itertools.combinations(keys, 2):
        a, m = _dim_diff(t1, t2)
        if a == 1:
            d, dim = _get_dim(m) 
            if t1[d] == 0:
                lo = t1
                hi = t2
            else:
                lo = t2
                hi = t1            
            slo = sims[lo]
            shi = sims[hi]
            adj = slo + shi
            sadh = 0.5 + (shi / 2.0)
            if slo > shi:
                sadh = 0.5 - (slo / 2.0)
            if abs(sadh - 0.5) > abs(diffs[dim] - 0.5):
                diffs[dim] = sadh
    mapping = [0, 0, 0]
    for t1, v in diffs.items():
        d, dim = _get_dim(t1)
        mapping[d] = v
    return tuple(mapping)
"""


def map_stimulation(stimulation, model):
    '''Map stimulation into the unit sphere inside the Lövheim cube.
    '''
    sims = {}
    for k,v in BASE_EMOTION_MAP.items():
        s = []
        for emotion in v:
            s.append(model.similarity(stimulation, emotion))
        sims[k] = max(s)
              
    keys = BASE_EMOTION_MAP.keys()
    v = np.array((0, 0, 0))
    for t1, t2 in itertools.combinations(keys, 2):
        v1 = VECTORS[t1]
        v2 = VECTORS[t2]
        s1 = sims[t1]**3
        s2 = sims[t2]**3
        sa = s1 + s2
        sa1 = s1 / sa
        sa2 = s2 / sa
        v = v + (v1*s1 + v2*s2) 
    return _normalize(v)


def get_closest(point, vector = True):
    '''Get emotion closest to the point.
    
    If there are multiple emotions as close the point, picks one in random. If 
    vector is True, first normalizes the vector represented by point on the 
    surface of the unit sphere, and then get's the closest emotion. 
    
    :param point: Point in 3D space
    :type point: np.array
    :param vector: Is point considered as a vector originating from the Origo.
    :type vector: bool
    :returns: tuple -- (emotion, point)
    '''
    mind = sys.maxint
    closest = []
    if vector:
        point = _normalize(point)
    for em, p in EMOTIONS:
        curd = _ed(p, point)
        if curd <= mind:
            if curd == mind:
                closest.append(em)
            else:
                closest = [em]
            mind = curd
    em = choice(closest)
    p = emotions.get_point(em)
    return em, p
    
    
def _normalize(v):
    return v / _ed((0,0,0), v)    
    
              
def _get_dim(t1):
    if t1[0] == 1:
        return 0, (1, 0, 0)
    if t1[1] == 1:
        return 1, (0, 1, 0)
    return 2, (0, 0, 1)
    

def _dim_diff(t1, t2):
    ts = zip(t1, t2)
    m = map(lambda x: abs(x[0] - x[1]), ts)
    a = reduce(lambda x,y: x+ abs(y[0] - y[1]), ts, 0)
    return a, m


def _ed(p1, p2):
    ps = zip(p1, p2)
    return np.sqrt(reduce(lambda x,y: x+abs(y[0] - y[1])**2, ps, 0))
  

def map_emotions(emotions, model):
    '''Map multiple emotions on the surface of the unit sphere inside the 
    Lövheim cube of emotion.
    '''
    emos = []
    points = []
    X = []
    Y = []
    Z = [] 
    for emo in emotions:
        try: 
            p = map_stimulation(emo, model)
        except:
            continue
        emos.append(emo)
        X.append(p[0])
        Y.append(p[1])
        Z.append(p[2])
        points.append(p)  
    
    return emos, X, Y, Z    

    
def plot_emotions(emotions, X, Y, Z, plot_labels = True):
    emos = emotions
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt 
    from mpl_toolkits.mplot3d import Axes3D
    from mpl_toolkits.mplot3d import proj3d
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')    
    ax.scatter(X, Y, Z)
    ax.set_xlabel('Serotonin')
    ax.set_ylabel('Noradrenaline')
    ax.set_zlabel('Dopamine')
    
    if plot_labels:
        labels = []
        for i in range(len(X)):
            x2, y2, _ = proj3d.proj_transform(X[i],Y[i],Z[i], ax.get_proj())
            label = plt.annotate(
                emos[i], 
                xy = (x2, y2), xytext = (-5, 5),
                textcoords = 'offset points', ha = 'right', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.1', fc = 'yellow', alpha = 0.5),
                arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))
            labels.append(label)
        
        def update_position(e):
            for i in range(len(X)):
                x2, y2, _ = proj3d.proj_transform(X[i],Y[i],Z[i], ax.get_proj())
                labels[i].xy = (x2, y2)
                labels[i].update_positions(fig.canvas.renderer)
            fig.canvas.draw()
        fig.canvas.mpl_connect('button_release_event', update_position)
    plt.tight_layout()
    plt.show()
    
    
def write2file(filepath, E, X, Y, Z):
    '''Write mappings to file.'''
    enc = set()
    with open(filepath, 'w') as f:
        s = "(\n"
        for i in xrange(len(E)):
            if E[i] not in enc:
                s+= "('{}', ({}, {}, {})),\n".format(E[i],X[i],Y[i],Z[i])
                enc.add(E[i])
        s+=")"
        f.write(s)
    
        
if __name__ == "__main__":
    from web import therex
    import gensim
    negs = therex.categories("negative:emotion")['Members']
    negs = map(lambda x: x[0], negs)
    negs = negs[:10]
    poss = therex.categories("positive:emotion")['Members']
    poss = map(lambda x: x[0], poss)
    poss = poss[:10]
    emos = negs + poss
    #emos = set(emos)
    model = gensim.models.Word2Vec.load("/Users/pihatonttu/nltk_data/gensim/googlenews_gensim_v2w.model")
    E, X, Y, Z = map_emotions(emos, model)
    plot_emotions(E, X, Y, Z)
    
    
    
    
    



