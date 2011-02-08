import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.util import ngrams
from nltk.probability import FreqDist
import sys
import os
#from nltk.book import *

#text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])

WRD_NGRAMS = False
WRD_NGRAM_SIZE = 3
N_WRD_NGRAMS = 10

CHAR_NGRAMS = False
CHAR_NGRAM_SIZE = 3
N_CHAR_NGRAMS = 10

FUNCTION_WORDS = False

# TODO: How can this be dynamic?
CORPUS_ROOT = "/Users/epb/Documents/uni/kandidat/speciale/data/fed_papers/set2"
# TODO: How can this be dynamic?
FEATURE_FILE = "/Users/epb/Documents/uni/kandidat/speciale/code/out.txt"
#CH_NGRAM_FREQS = "/Users/epb/Documents/uni/kandidat/speciale/code/out.txt"
CATEGORY_FILE = "/Users/epb/Documents/uni/kandidat/speciale/code/cat.txt"
# TODO: Dynamic
FUNC_FOLDER = "/Users/epb/Documents/uni/kandidat/speciale/data/func_words_eng_zlch06"


def load_wrds(dir, cmt="//"):
    '''
    Load a list of a words from some text files found in a given dir.
    Each line is considered a word if it is not a comment.
    @param dir: Where the files are found
    @param cmt: Comment-line indicator
    '''
    wrds = []
    for e in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, e)):
            f = open(os.path.join(dir,e))
            for l in f:
                if not l.startswith(cmt):
                    wrds.append(l.rstrip())
            f.close()
    return wrds

# Get options from command line
a = 0
while a < len(sys.argv):
    arg = sys.argv[a]
    i = 1
    
    # Character n-grams, with n-gram size and no. of n-grams
    if arg == "-c":
        CHAR_NGRAMS = True
        if a+1 < len(sys.argv) and not sys.argv[a+1].startswith("-"):
            CHAR_NGRAM_SIZE = int(sys.argv[a+1])
            i = i + 1
        if a+2 < len(sys.argv) and not sys.argv[a+2].startswith("-"):
            N_CHAR_NGRAMS = int(sys.argv[a+2])
            i = i + 1
        
    # Function words
    elif arg == "-f":
        FUNCTION_WORDS = True
        
    # Word n-grams
    elif arg == "-w":
        WRD_NGRAMS = True
        if a+1 < len(sys.argv) and not sys.argv[a+1].startswith("-"):
            WRD_NGRAM_SIZE = int(sys.argv[a+1])
            i = i + 1
            if a+2 < len(sys.argv) and not sys.argv[a+2].startswith("-"):
                N_WRD_NGRAMS = int(sys.argv[a+2])
                i = i + 1
            
    # Corpus
    elif arg == "-r":
        if a+1 < len(sys.argv) and not sys.argv[a+1].startswith("-"):
            CORPUS_ROOT = sys.argv[a+1]
            i = i + 1
            
    a = a + i
            
MAX = 5
i = 0

# Load corpus
corpus = PlaintextCorpusReader(CORPUS_ROOT, '.*')
n_texts = len(corpus.fileids())

# Matrix containing features; a list for each text
feature_matrix = [[] for i in range(n_texts)]
#print feature_matrix

# List of classes, one for each text in corpus
text_classes = []

# TODO: Needed?
possible_categories = {"hamilton": 1, "madison": 2, "jay": 3}


## CHAR N-GRAM VARIABLES 

if CHAR_NGRAMS:
    all_char_ngrams = [] # All n-grams found in entire corpus
    text_char_ngrams_freqs = [] # The frequency of char n-grams found in each text   

## WORD N-GRAM VARIABLES

if WRD_NGRAMS:
    all_wd_ngrams = []
    text_wrd_ngram_freqs = []

## FUNCTION WORD VARIABLES

if FUNCTION_WORDS:
    func_wrds = load_wrds(FUNC_FOLDER)
    #print len(func_wrds)
    text_funcwrd_freqs = []


######## ANALYZE TEXTS ########

for text in corpus.fileids():
    
    # TODO: can I reuse any word or character lists?
    wrd_tokens = corpus.words(text)
    lower_wrds = [w.lower() for w in wrd_tokens if w.isalnum()]
    
    # Find category in filename
    found_category = ""
    for features in possible_categories.keys():
        if text.count(features):
            found_category = possible_categories[features]
            break # only one category per file
    text_classes.append(found_category)
    
    #print ""
    #print text, len(corpus.words(text))
    
    
    #### FUNCTION WORDS ####
    
    if FUNCTION_WORDS:
        my_func_wrds = [w for w in lower_wrds if func_wrds.count(w) > 0]
        text_funcwrd_freqs.append(FreqDist(my_func_wrds))
    
    
    ######## CHAR N-GRAMS #############
    
    if CHAR_NGRAMS:
        text_str = corpus.raw(text).replace('\r','').replace('\n', ' ')
        char_ngrams = ngrams(text_str, CHAR_NGRAM_SIZE)
        text_char_ngrams_freqs.append(FreqDist(char_ngrams))
        all_char_ngrams.extend(char_ngrams)
    
    
    ######## WORD N-GRAMS #############
    
    if WRD_NGRAMS:
        wrd_ng = ngrams(lower_wrds, WRD_NGRAM_SIZE)
        text_wrd_ngram_freqs.append(FreqDist(wrd_ng))
        all_wd_ngrams.extend(wrd_ng)
    

##### SAVE FREQS OF FUNCTION WORDS AS FEATURES

if FUNCTION_WORDS:
    
    for t in range(n_texts):
        freqs = text_funcwrd_freqs[t]
        
        for f in func_wrds:
            freq = freqs.freq(f)
            feature_matrix[t].append(freq)
    

    
##### SAVE CHAR N-GRAMS AS FEATURES

if CHAR_NGRAMS:
        
    # Frequency of all possible n-grams across corpus    
    all_char_ngrams_freqs = FreqDist(all_char_ngrams)
    tot_ngrams = min([N_CHAR_NGRAMS, all_char_ngrams_freqs.B()])
    
    # Select char n-gram features
    for t in range(n_texts):
        freqs = text_char_ngrams_freqs[t]
        
        # Step through X most frequent n-grams across corpus, the feature is the
        # relative frequency for each n-gram in each text
        for r in range(tot_ngrams):
            ngram = all_char_ngrams_freqs.keys()[r]
            freq = freqs.freq(ngram)
            feature_matrix[t].append(freq)


##### SAVE WORD N-GRAMS AS FEATURES

if WRD_NGRAMS:
    
    all_wrd_ngrams_freqs = FreqDist(all_wd_ngrams)
    tot_ngrams = min([N_WRD_NGRAMS, all_wrd_ngrams_freqs.B()])
    
    # Select word n-gram features
    for t in range(n_texts):
        freqs = text_wrd_ngram_freqs[t]
        
        # Step through X most frequent n-grams across corpus, the feature is the
        # relative frequency for each n-gram in each text
        for r in range(tot_ngrams):
            ngram = all_wrd_ngrams_freqs.keys()[r]
            freq = freqs.freq(ngram)
            feature_matrix[t].append(freq)




#### PUT FEATURES IN A FILE ####

ff = open(FEATURE_FILE,'w')
for feat in feature_matrix:
    strlist = [str(i) for i in feat]
    ff.write(" ".join(strlist) + "\n")
ff.flush()
print FEATURE_FILE

#### PUT CLASSES IN A FILE ####

cf = open(CATEGORY_FILE,'w')
for c in text_classes:
    cf.write(str(c) + "\n")
cf.flush()
print CATEGORY_FILE
