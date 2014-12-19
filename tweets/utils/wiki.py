'''
.. py:module:: 'wiki'
    :platform: Unix
    
Utilities for parsing and working with wikipedia dumps.
'''
import gensim

def train_word2vec(bow_file, outfile):
    '''Train word2vec model with bag-of-words file.'''
    
    corpus = gensim.corpora.MmCorpus(bow_file)
    model = gensim.models.Word2Vec(size = 200, workers = 4)
    model.build_vocab(corpus)
    corpus = gensim.corpora.MmCorpus(bow_file)
    model.train(corpus)
    

