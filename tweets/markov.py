'''
.. py:module:: markov
    :platofrm: Unix
    
First order Markov chains for textual generation.
'''
import re
import operator
import random
import nltk
from nltk.tokenize import WhitespaceTokenizer

class MarkovSentences():
    """First order Markov chain model and sentence generation with given corpus.
    """
    
    sanitizer = re.compile(r'[\t\n\r\"_]', re.UNICODE) 
    remove_spaces = re.compile(' +', re.UNICODE)
    max_length = 140
    sentence_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    end_chars = '.!?'
    
    def __init__(self, text = None, filepath = None, order = 1):
        """Build Markov chain model for given text or file.
        
        If text is specified, then file is not read.
        
        **Args:**
            | text (str or unicode): Corpus as text.
            | filepath: Path to corpus file.
        """
        if text is None and filepath is None:
            raise ValueError("You must specify either text of file path.")
        if text is not None and type(text) is not (str or unicode):
            raise ValueError("Text must be either in str or unicode format.")
        if text is not None:
            self.corpus = text
        else:
            with open(filepath, 'r') as f:
                self.corpus = f.read()
                   
        self.order = order
        self._sanitize_corpus()
        self.punkted_corpus = self.sentence_detector.tokenize(self.corpus)
        self._build_model()
        
       
        
    def _sanitize_corpus(self):
        """Sanitize corpus by removing line changes, etc.
        """
        self.corpus = self.sanitizer.sub(' ', self.corpus)
        self.corpus = self.remove_spaces.sub(' ', self.corpus)
       
            
    def _build_model(self):
        model = {}
        starts = []
        ends = []
        tokenizer = WhitespaceTokenizer()
        for sentence in self.punkted_corpus:
            print sentence
            tokens = tokenizer.tokenize(sentence)
            self._add_to_model(tokens, model, starts, ends)
          
        self.probabilities = self._calc_probabilities(model) 
              
        self.model = model
        self.starts = starts
        self.ends = ends
      
        
    def _add_to_model(self, tokens, model, starts, ends):
        if self.order == 1:
            starts.append(tokens[0])
            ends.append(tokens[-1])
            if len(tokens) > 1:
                for i, token in enumerate(tokens[1:]):
                    last = tokens[i]
                    if last not in model:
                        model[last] = {}
                    
                    if token in model[last]:
                        model[last][token] += 1
                    else:
                        model[last][token] = 1
                    
                    
    def _calc_probabilities(self, model):
        probabilities = {}
        for s in model:
            probabilities[s] = []
            cur_sum = float(sum([v for k, v in model[s].items()]))
            for k, v in model[s].items():
                probabilities[s].append([k, float(v)/cur_sum])
            sv = sorted(probabilities[s], key = operator.itemgetter(1), reverse = True)
            cp = 0.0
            for i, item in enumerate(sv):
                cp += item[1]
                sv[i][1] = cp
                
        return probabilities
    
    
    def generate_sentence(self):
        sentence = ""
        start = random.choice(self.starts)
        sentence += start
        cur = start
        while cur not in self.ends:
            rng = random.random()
            for item in self.probabilities[cur]:
                if rng < item[1]:
                    sentence += " "
                    sentence += item[0].split()[0]
                    cur = item[0]
                    break
   
        return sentence
            
            
        
                
                
                
        
        
            
            
            
        
 
            
