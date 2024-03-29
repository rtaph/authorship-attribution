from nltk.corpus import PlaintextCorpusReader
from nltk.probability import FreqDist
import sys
import time
import fextract_helper

wrd_ngrams = False
wrd_ngram_size = 3
n_wrd_ngrams = 10

char_ngrams = False
char_ngram_size = 3
n_char_ngrams = 10

function_words = False
FUNC_FOLDER = "/Users/epb/Documents/uni/kandidat/speciale/data/func_words_eng_zlch06"


CG_REPR = False
KN_SMOOTH = False
GT_SMOOTH = False

# output files
FEATURE_FILE = "/Users/epb/Documents/uni/kandidat/speciale/code/out.txt"
CATEGORY_FILE = "/Users/epb/Documents/uni/kandidat/speciale/code/cat.txt"
#FEATURE_FILE = "/home/epb/Documents/code/out.txt"
#CATEGORY_FILE = "/home/epb/Documents/code/cat.txt"

# folder with corpus
corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/fed/f2"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/personae/p2"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blogs/b1"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/b1"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/test/test1_64"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/ansar1/an2"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/almedad/al2"

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
print 'Prob. of n-grams depend on history:', CG_REPR
print 'Good-Turing:', GT_SMOOTH
print 'Kneser-Ney:', KN_SMOOTH

start = time.time()

# Load corpus
corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding='UTF-8')
n_texts = len(corpus.fileids())

# Matrix containing features; a list for each text
feature_matrix = [[] for i in range(n_texts)]
#print feature_matrix

# List of classes, one for each text in corpus
text_classes = fextract_helper.find_classes(corpus.fileids())

if char_ngrams:
    s1 = time.time()
    a, t = fextract_helper.char_ngram_stats(corpus.fileids(), corpus, \
                                            char_ngram_size, CG_REPR or KN_SMOOTH)
    e1 = time.time()
    print 'Char: Finding took', e1-s1, 'seconds'
    
    s1 = time.time()
    tot_cngs = min([n_char_ngrams, a.B()])
    mostfreq_ngs = a.keys()[:tot_cngs]
    #print len(mostfreq_ngs)
    e1 = time.time()
    print 'Char: Calc took', e1-s1, 'seconds'
    
    s1 = time.time()
    feat_charngram = fextract_helper.create_ngram_feats(mostfreq_ngs, char_ngram_size, \
                                                        t, CG_REPR or KN_SMOOTH, \
                                                        KN_SMOOTH, GT_SMOOTH)
    e1 = time.time()
    print 'Char: Creating took', e1-s1, 'seconds'
    
    
if wrd_ngrams:
    s1 = time.time()
    a, t = fextract_helper.wrd_ngram_stats(corpus.fileids(), corpus, \
                                           wrd_ngram_size, CG_REPR or KN_SMOOTH)
    e1 = time.time()
    print 'Word: Finding took', e1-s1, 'seconds'
    
    s1 = time.time()
    tot_wngs = min([n_wrd_ngrams, a.B()])
    mostfreq_wngs = a.keys()[:tot_wngs]
    #print wrd_ngram_size
    #print len(mostfreq_wngs)
    #print mostfreq_wngs[:10]
    #exit()
    e1 = time.time()
    print 'Word: Calc took', e1-s1, 'seconds'
    
    s1 = time.time()
    feat_wrdgram = fextract_helper.create_ngram_feats(mostfreq_wngs, wrd_ngram_size, \
                                                      t, CG_REPR or KN_SMOOTH, \
                                                      KN_SMOOTH, GT_SMOOTH)
    e1 = time.time()
    print 'Word: Creating took', e1-s1, 'seconds'
    
if function_words:
    func_wds, text_func_wrds = fextract_helper.extract_fws(corpus.fileids(), corpus, FUNC_FOLDER)
    feat_funcwrds = fextract_helper.create_fw_features(func_wds, text_func_wrds)
for f in range(len(feature_matrix)):
    if char_ngrams:
        feature_matrix[f].extend(feat_charngram[f])
    if wrd_ngrams:
        feature_matrix[f].extend(feat_wrdgram[f])
    if function_words:
        feature_matrix[f].extend(feat_funcwrds[f])

fextract_helper.save_features(FEATURE_FILE, feature_matrix, CATEGORY_FILE, text_classes)

# Stop timer and display results
end = time.time()
n_texts = len(corpus.fileids())
n_features = len(feature_matrix[0])
print "Total time elapsed analysing {0} texts: {1} sec. No. of features: {2}".format(n_texts,end-start,n_features)