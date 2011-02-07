import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.util import ngrams
from nltk.probability import FreqDist
import sys
import os
#from nltk.book import *

#text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])

WRD_NGRAMS = False

CHAR_NGRAMS = False
NGRAM_SIZE = 3
NO_OF_NGRAMS_USED = 10

FUNCTION_WORDS = False

# TODO: How can this be dynamic?
CORPUS_ROOT = "/Users/epb/Documents/uni/kandidat/speciale/data/fed_papers/set2"
# TODO: How can this be dynamic?
FEATURE_FILE = "/Users/epb/Documents/uni/kandidat/speciale/code/python/out.txt"
#CH_NGRAM_FREQS = "/Users/epb/Documents/uni/kandidat/speciale/code/python/out.txt"
CATEGORY_FILE = "/Users/epb/Documents/uni/kandidat/speciale/code/python/cat.txt"
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
            NGRAM_SIZE = int(sys.argv[a+1])
            i = i + 1
        if a+2 < len(sys.argv) and not sys.argv[a+2].startswith("-"):
            NO_OF_NGRAMS_USED = int(sys.argv[a+2])
            i = i + 1
        
    # Function words
    elif arg == "-f":
        FUNCTION_WORDS = True
            
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

all_char_ngrams = [] # All n-grams found in entire corpus
text_char_ngrams_freqs = [] # The frequency of char n-grams found in each text
#n_char_ngrams = []

## WORD N-GRAM VARIABLES

all_wd_ngrams = []
wrd_fd_list = []

## FUNCTION WORD VARIABLES

if FUNCTION_WORDS:
    func_wrds = load_wrds(FUNC_FOLDER)



for text in corpus.fileids():
    
    # TODO: can I reuse any word or character lists?
    
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
        wrd_tokens = corpus.words(text)
        wrd_tokens = [w.lower() for w in wrd_tokens if w.isalnum()]
        
    
    
    ######## CHARS #############
    
    if CHAR_NGRAMS:
        text_str = corpus.raw(text).replace('\r','').replace('\n', ' ')
        char_ngrams = ngrams(text_str, NGRAM_SIZE)
        
        
        
        char_ngrams_freqs = FreqDist(char_ngrams)
        #n_char_ngrams.append(char_ngrams_freqs.N())
        
        text_char_ngrams_freqs.append(char_ngrams_freqs)
        
        all_char_ngrams.extend(char_ngrams)
    
    
    ######## WORDS #############
    
    if WRD_NGRAMS:
        #break
        #print ""
        wrd_tokens = corpus.words(text)
        wrd_tokens = [w.lower() for w in wrd_tokens if w.isalnum()]
        #print wrd_tokens[:10]
        wrd_ng = ngrams(wrd_tokens, NGRAM_SIZE)
        #print NGRAM_SIZE, "-grams (words):", len(wrd_ng)
        #print "Example:", wrd_ng[:20]
        wrd_fd = FreqDist(wrd_ng)
        #print wrd_fd.items()[:10] # ordered by decreasing frequency
        
        wrd_fd_list.append(wrd_fd)
        
        all_wd_ngrams.extend(wrd_ng)
        
        #wrd_fd.plot(cumulative=True)     
        
        #i = i + 1
        #if i >= MAX:
        #    break
        
        #break
    

    
######### CHARS ##########

if CHAR_NGRAMS:
        
    # Frequency of all possible n-grams across corpus    
    all_char_ngrams_freqs = FreqDist(all_char_ngrams)
    

    # Select char n-gram features
    #for a in range(len(text_char_ngrams_freqs)):
    for t in range(n_texts):
        freqs = text_char_ngrams_freqs[t]
        #print freqs
        #n_ngrams = float(n_char_ngrams[t])
        n_ngrams = freqs.N() # no. of n-grams in text
        
        # Step through X most frequent n-grams across corpus and calculate a
        # relative frequency for each n-gram in each text 
        for r in range(NO_OF_NGRAMS_USED):
            ngram = all_char_ngrams_freqs.keys()[r]
            freq = freqs.freq(ngram)
            feature_matrix[t].append(freq)
            #print ngram, freq
            #l = l + str(freqs[all_char_ngrams_freqs.keys()[r]] / n_ngrams) + " "
            #feature_matrix[t].append(freqs[ngram] / n_ngrams)


######### WORDS ##########

if WRD_NGRAMS:
    
    all_wd_fd = FreqDist(all_wd_ngrams)
    #print all_wd_fd.items()[:20]
    #all_wd_fd.plot(200, cumulative=True)
    #print all_wd_fd.keys()[0]
    #print all_wd_fd.keys()[1]
    
    # Print some frequencies
    #for a in wrd_fd_list:
        #print a.keys().count(all_wd_fd.keys()[0])
        #print a.count(all_wd_fd.keys()[0])




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







#### UNUSED ####

#print all_char_ngrams_freqs.items()[:20]
#print all_char_ngrams_freqs.keys()[0]
#print all_char_ngrams_freqs.keys()[1]

# Print some frequencies
#print "["
#for a in range(len(text_char_ngrams_freqs)):
#    freqs = text_char_ngrams_freqs[a]
#    print freqs[all_char_ngrams_freqs.keys()[0]] / float(n_char_ngrams[a]), ",",  freqs[all_char_ngrams_freqs.keys()[1]] / float(n_char_ngrams[a]), freqs[all_char_ngrams_freqs.keys()[2]] / float(n_char_ngrams[a]), ",",  freqs[all_char_ngrams_freqs.keys()[3]] / float(n_char_ngrams[a]), ";"
#print "]"

# Print found categories
#print "["
#for features in text_classes:
#    print  features, ";"
#print "]"
