import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.util import ngrams
from nltk.probability import FreqDist
import sys
import os
import time
#from nltk.book import *

#text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])

wrd_ngrams = False
wrd_ngram_size = 3
n_wrd_ngrams = 10

char_ngrams = False
char_ngram_size = 3
n_char_ngrams = 10

function_words = False
FUNC_FOLDER = "/Users/epb/Documents/uni/kandidat/speciale/data/func_words_eng_zlch06"

# output files
FEATURE_FILE = "/Users/epb/Documents/uni/kandidat/speciale/code/out.txt"
CATEGORY_FILE = "/Users/epb/Documents/uni/kandidat/speciale/code/cat.txt"
#FEATURE_FILE = "/home/epb/Documents/code/out.txt"
#CATEGORY_FILE = "/home/epb/Documents/code/cat.txt"
#STATUS_FILE = "/Users/epb/Documents/uni/kandidat/speciale/code/out_state.txt"

# folder with corpus
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/fed_papers/all_single_quat_multi"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/PersonaeCorpus_onlineVersion/set3"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/a2_4_10"
corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/set30_10_2"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/test/test1_64"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/dark_web_forum_portal/almedad/a1_3_40_10"


#st_file = open(STATUS_FILE,"w")
#st_file.write(str(time.strftime("%X %x")) + "\n")

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
        char_ngrams = True
        if a+1 < len(sys.argv) and not sys.argv[a+1].startswith("-"):
            char_ngram_size = int(sys.argv[a+1])
            i = i + 1
            if a+2 < len(sys.argv) and not sys.argv[a+2].startswith("-"):
                n_char_ngrams = int(sys.argv[a+2])
                i = i + 1
        print "Using the", n_char_ngrams, "most frequent char n-grams of size", char_ngram_size
        #st_file.write("Using the " + str(n_char_ngrams) + " most frequent char n-grams of size " + str(char_ngram_size) + "\n")
        
    # Function words
    elif arg == "-f":
        function_words = True
        print "Using function words"
        #st_file.write("Using function words\n")
        
    # Word n-grams
    elif arg == "-w":
        wrd_ngrams = True
        if a+1 < len(sys.argv) and not sys.argv[a+1].startswith("-"):
            wrd_ngram_size = int(sys.argv[a+1])
            i = i + 1
            if a+2 < len(sys.argv) and not sys.argv[a+2].startswith("-"):
                n_wrd_ngrams = int(sys.argv[a+2])
                i = i + 1
        print "Using the", n_wrd_ngrams, "most frequent word n-grams of size", wrd_ngram_size 
        #st_file.write("Using the " + str(n_wrd_ngrams) +  " most frequent word n-grams of size " + str(wrd_ngram_size) + "\n")
        
    # Corpus
    elif arg == "-r":
        if a+1 < len(sys.argv) and not sys.argv[a+1].startswith("-"):
            corpus_root = sys.argv[a+1]
            i = i + 1
                        
    a = a + i
    
print "Corpus is", corpus_root
#st_file.write("Corpus is " + corpus_root + "\n")

start = time.time()
            
MAX = 5
i = 0

# Load corpus
corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding='UTF-8')
n_texts = len(corpus.fileids())

# Matrix containing features; a list for each text
feature_matrix = [[] for i in range(n_texts)]
#print feature_matrix

# List of classes, one for each text in corpus
text_classes = []


## CHAR N-GRAM VARIABLES 

if char_ngrams:
    all_char_ngrams = [] # All n-grams found in entire corpus
    text_char_ngrams_freqs = [] # The frequency of char n-grams found in each text   

## WORD N-GRAM VARIABLES

if wrd_ngrams:
    all_wd_ngrams = []
    text_wrd_ngram_freqs = []

## FUNCTION WORD VARIABLES

if function_words:
    func_wrds = load_wrds(FUNC_FOLDER)
    #print len(func_wrds)
    text_funcwrd_freqs = []


######## ANALYZE TEXTS ########

for text in corpus.fileids():
    
    if not text.endswith(".txt"):
        continue
    print text
    #st_file.write(text + "\n")
    
    wrd_tokens = corpus.words(text)
    
    empty = len(corpus.raw(text)) == 0 

    if not empty:
        #print len(wrd_tokens)
        lower_wrds = [w.lower() for w in wrd_tokens if w.isalnum()]
    
    
    # Find category in filename
    #cat_start = text.rfind("_") + 1
    #found_category = (text.rpartition("_")[2]).partition(".")[0]
    found_category = text.partition(".")[0]
    #print found_category
    #for k in possible_categories.keys():
    #    if text.count(k) > 0:
    #        found_category = possible_categories[k]
    #        break # only one category per file
    
    text_classes.append(found_category)
    
    #print ""
    #print text, len(corpus.words(text))
    
    
    #### FUNCTION WORDS ####
    
    if function_words:
        if not empty:
            my_func_wrds = [w for w in lower_wrds if func_wrds.count(w) > 0]
            text_funcwrd_freqs.append(FreqDist(my_func_wrds))
        else:
            text_funcwrd_freqs.append(FreqDist())
    
    
    ######## CHAR N-GRAMS #############
    
    if char_ngrams:
        if not empty:
            text_str = corpus.raw(text).replace('\r','').replace('\n', ' ')
            char_ngrams = ngrams(text_str, char_ngram_size)
            text_char_ngrams_freqs.append(FreqDist(char_ngrams))
            all_char_ngrams.extend(char_ngrams)
            #print FreqDist(char_ngrams).items()[10:]
        else:
            text_char_ngrams_freqs.append(FreqDist())
    
    
    ######## WORD N-GRAMS #############
    
    if wrd_ngrams:
        if not empty:
            wrd_ng = ngrams(lower_wrds, wrd_ngram_size)
            #if FreqDist(wrd_ng).keys().count(('bj', 'papa', 'bj')) > 0:
            #    print text
            text_wrd_ngram_freqs.append(FreqDist(wrd_ng))
            all_wd_ngrams.extend(wrd_ng)
            #print FreqDist(wrd_ng).items()[10:]
        else:
            text_wrd_ngram_freqs.append(FreqDist())
    

##### SAVE FREQS OF FUNCTION WORDS AS FEATURES

if function_words:
    
    print "Attaching function words to list of features"
    
    for t in range(n_texts):
        freqs = text_funcwrd_freqs[t]
        
        for f in func_wrds:
            freq = freqs.freq(f)
            feature_matrix[t].append(freq)
    

    
##### SAVE CHAR N-GRAMS AS FEATURES

if char_ngrams:
        
    print "Attaching char n-grams to list of features"
    #st_file.write("Attaching char n-grams to list of features\n")
    
    # Frequency of all possible n-grams across corpus    
    all_char_ngrams_freqs = FreqDist(all_char_ngrams)
    #print all_char_ngrams_freqs.items()[:10]
    #print all_char_ngrams_freqs.keys()[:10]
    #print len(all_char_ngrams_freqs)
    # we can't look for more n-grams than we have
    tot_ngrams = min([n_char_ngrams, all_char_ngrams_freqs.B()])
    #print tot_ngrams
    
    # Select char n-gram features
    for t in range(n_texts):
        print 'Text', t
        #st_file.write("Text: " + str(t) + "\n")
        freqs = text_char_ngrams_freqs[t]
        #print freqs
        
        # Step through X most frequent n-grams across corpus, the feature is the
        # relative frequency for each n-gram in each text
        for r in range(tot_ngrams):
            #print r
            ngram = all_char_ngrams_freqs.keys()[r]
            #print ngram
            #print ngram
            freq = freqs.freq(ngram)
            #print ngram, freq
            feature_matrix[t].append(freq)


##### SAVE WORD N-GRAMS AS FEATURES

if wrd_ngrams:
    
    print "Attaching word n-grams to list of features"
    #st_file.write("Attaching word n-grams to list of features\n")
    
    all_wrd_ngrams_freqs = FreqDist(all_wd_ngrams)
    #print len(all_wrd_ngrams_freqs)
    #print all_wrd_ngrams_freqs
    #print all_wrd_ngrams_freqs.items()[:10]
    
    # we can't look for more n-grams than we have
    tot_ngrams = min([n_wrd_ngrams, all_wrd_ngrams_freqs.B()])
    #print tot_ngrams
    #print all_wrd_ngrams_freqs.keys()[:tot_ngrams]
    
    # Select word n-gram features
    for t in range(n_texts):
        print 'Text', t
        #st_file.write("Text: " + str(t) + "\n")
        freqs = text_wrd_ngram_freqs[t]
        
        # Step through X most frequent n-grams across corpus, the feature is the
        # relative frequency for each n-gram in each text
        for r in range(tot_ngrams):
            #print r
            ngram = all_wrd_ngrams_freqs.keys()[r]
            #print ngram
            freq = freqs.freq(ngram)
            #if ngram == ('bj', 'papa', 'bj'):
            #    print freq
            feature_matrix[t].append(freq)




#### PUT FEATURES IN A FILE ####

print "Outputting features to", FEATURE_FILE
#st_file.write("Outputting features to " + FEATURE_FILE + "\n")
ff = open(FEATURE_FILE,'w')
for feat in feature_matrix:
    strlist = [str(i) for i in feat]
    ff.write(" ".join(strlist) + "\n")
ff.flush()


#### PUT CLASSES IN A FILE ####

# TODO: Output real classes + subclasses to real_cat

print "Outputting classes to", CATEGORY_FILE
#st_file.write("Outputting classes to " + CATEGORY_FILE + "\n")
distinct_classes = list(set(text_classes))
#print distinct_classes
#int_classes = range(1,len(text_classes))
cf = open(CATEGORY_FILE,'w')
for c in text_classes:
    i = distinct_classes.index(c) + 1
    #cf.write(str(c) + "\n")
    cf.write(str(i) + "\n")
cf.flush()

# Stop timer and display results
end = time.time()
n_texts = len(corpus.fileids())
n_features = len(feature_matrix[0])
print "Total time elapsed analysing {0} texts: {1} sec. No. of features: {2}".format(n_texts,end-start,n_features)
#st_file.write("Total time elapsed analysing {0} texts: {1} sec. No. of features: {2}".format(n_texts,end-start,n_features) + "\n")

#st_file.write(str(time.strftime("%X %x")) + "\n")
#st_file.flush()