from nltk.util import ngrams
from nltk.probability import FreqDist
from nltk.corpus import PlaintextCorpusReader
import os
import time
import math

def find_classes(texts):
    '''
    For a set of texts, find the class of the text, given in
    the name of the text.
    @return: A list of classes, one per text
    '''
    text_classes = []
    for text in texts:
        found_category = text.partition(".")[0]
        text_classes.append(found_category)
    return text_classes

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

def char_ngram_stats(texts, corpus, n_char_ngrams, char_ngram_size):
    '''
    Original version of extracting n-grams: Returns a list
    of all n-grams across all texts and a matrix with a list of
    n-grams per text
    ''' 
    
    all_char_ngrams = [] # All n-grams found in entire corpus
    text_char_ngrams = [] # The frequency of char n-grams found in each text
    
    for text in texts:
        
        if not text.endswith(".txt"):
            continue
        
        empty = len(corpus.raw(text)) == 0 
    
        if not empty:
            text_str = corpus.raw(text).replace('\r','').replace('\n', ' ')
            char_ng = ngrams(text_str, char_ngram_size)
            text_char_ngrams.append(char_ng)
            all_char_ngrams.extend(char_ng)
        else:
            text_char_ngrams.append([])
            
    return all_char_ngrams, text_char_ngrams

def get_text_cngs(texts, corpus_root, ngram_size):
    '''
    For each text, get a list of all char n-grams occurring the text
    '''
    
    ngs = []
    corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding='UTF-8')
    for text in texts:
        
        if not text.endswith(".txt"):
            continue
    
        if not len(corpus.raw(text)) == 0:
            text_str = corpus.raw(text).replace('\r','').replace('\n', ' ')
            char_ng = ngrams(text_str, ngram_size)
            ngs.append(char_ng)
        else:
            ngs.append([])
            
    return ngs

def get_cngs(texts, corpus_root, ngram_size):
    '''
    Get a list of all char n-grams occurring in some texts
    '''
    
    ngs = []
    
    corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding='UTF-8')
    for text in texts:
        
        if not text.endswith(".txt"):
            continue
    
        if not len(corpus.raw(text)) == 0:
            text_str = corpus.raw(text).replace('\r','').replace('\n', ' ')
            char_ng = ngrams(text_str, ngram_size)
            ngs.extend(char_ng)
            
    return ngs

def slr(x, y):
    '''
    Simple Linear Regression, y = a + bx
    @return: a, b
    '''
    assert len(x) == len(y)
    a = b = 0
    avgx = float(sum(x)) / len(x)
    avgy = float(sum(y)) / len(y)
    n = d = 0
    for i in range(len(x)):
        n = n + ((x[i]-avgx)*(y[i]-avgy))
        d = d + math.pow(x[i]-avgx,2)
    b = n/d
    a = avgy - (b*avgx)
    return a, b

def gt_nr_est(freqs):
    '''
    Smooth the Nr parameter for Good-Turing smoothing
    @return: a, b, X for a linear regression of log(Nr) = a + b*log(r)
    and X is the first r-value to start using smoothed nr's
    '''
    #CONFID_FACTOR = 1.96 # Adapted from http://www.grsampson.net/D_SGT.c
    CONFID_FACTOR = 1.65
    rl = sorted(list(set(freqs.values())))
    if len(rl) < 4:
        # There are too few (r,Nr)-pairs to smooth Nr
        return None, None, None
    logzr = []
    nrl = []
    for i in range(len(rl)):
        nr = freqs.Nr(rl[i])
        nrl.append(nr)
        if i > 0 and i < len(rl)-1:
            zr = (2*nr)/float(rl[i+1]-rl[i-1])
            logzr.append(math.log10(zr))
    logr = [math.log10(x) for x in rl[1:len(rl)-1]]
    a, b = slr(logr, logzr)
    
    # Find point (r) where to start using smoothed Nr's. This is
    # the place where the Nr's are no longer significantly different
    # from the smoothed Nr's
    X = len(rl)
    for i in range(len(rl)-1):
        
        r = rl[i]
        nr = float(nrl[i])
        nr1 = float(nrl[i+1])
        if nr == 0:
            X = r
            break 
        snr = math.pow(10, a + (b*math.log10(r)))
        stdv = math.sqrt((r+1)*(r+1)*(nr1/(nr*nr))*(1+(nr1/nr)))
        #print r, nr, nr1, snr, stdv
        
        # If the difference between Nr and smoothed Nr has dropped
        # below CONFID_FACTOR * standard deviation, the Nr is no longer
        # significantly different and we will use smoothed Nr from here
        if math.fabs(nr-snr) <= CONFID_FACTOR * stdv:
            X = r
            #print 'X',X
            break
    
    return a, b, X
    
    

def gt_smoothing(freqs, a, b, X):
    '''
    Good-Turing smoothing: Find r* for all r>=1
    a and b are from the linear regression log(Nr) = a + b*log(r)
    @return: Dictionary with key=r, value=r*
    '''
    
    rl = sorted(list(set(freqs.values()))) # list of r
    rsl = {} # dict of r,r*
    
    for r in rl:
        
        nr = freqs.Nr(r)
        nr1 = freqs.Nr(r+1)
        
        if a is not None and b is not None and b <= -1: 
            if nr == 0 or r >= X: # Good-Turing estimate for high r
                nr = math.pow(10, a + (b*math.log10(r)))
            if r+1 >= X:
                nr1 = math.pow(10, a + (b*math.log10(r+1)))
    
        rstar = (r+1) * (nr1/float(nr))
        #print r, nr, nr1, rstar
        if rstar > 0:
            rsl[r] = rstar
        else:
            rsl[r] = r # Occurs when too few seen objects
    
#    r = freqs[ngram]
#    nr = freqs.Nr(r)
#        
#    if nr == 0 or r >= X: # Good-Turing estimate for high r
#        nr = math.pow(10, a + (b*math.log10(r)))
#    if r+1 >= X:
#        nr1 = math.pow(10, a + (b*math.log10(r+1)))
#    else:
#        nr1 = freqs.Nr(r+1)
#    
#    rstar = (r+1) * (nr1/float(nr))
    #freq = rstar/N
    #print r, ngram, freq, freqs.freq(ngram)
    
    return rsl
    
def create_ngram_feats(ngrams, text_ngrams):
    '''
    Create n-gram features for each text, using the list of n-grams
    to consider given in ngrams argument. Can be used for both
    chars and words
    '''
    GT_SMOOTHING = True
    GT_RENORM = True
    GT_P0 = True
    
    n_texts = len(text_ngrams)
    print os.getpid(), ": Creating n-grams features for", n_texts, "texts"
    feature_matrix = [[] for i in range(n_texts)]
    
    #start = time.time()
    # Select char n-gram features
    for t in range(n_texts):
        freqs = FreqDist(text_ngrams[t])
        print 'Text', t
        
        if GT_SMOOTHING:
            # Find parameters for smoothed Nr
            a, b, X = gt_nr_est(freqs)
            N = freqs.N()
            p0_all = 1.0
            if N > 0: 
                p0_all = freqs.Nr(1) / float(N) # Probability for all unseen objects
            #print 'p0_all', p0_all
            # Dict of r,r*
            #print 'X', X
            rsl = gt_smoothing(freqs, a, b, X)
            #print rsl
            # Nstar is the total number of objects, using estimated r
            Nstar = 0
            for p in rsl.items():
                Nr = freqs.Nr(p[0])
                Nstar = Nstar + (Nr * p[1])
            #if Nstar == 0:
            #    print 'X', X
            #    print freqs.items()
            # Calculate p0
            unseen = 0
            for ngram in ngrams:
                if freqs[ngram] == 0:
                    unseen = unseen + 1
            if unseen > 0:
                p0 = p0_all / float(unseen)
                #print 'p0', p0
            #else:
            #    p0 = p0_all
            #p0 = 0
            
        
        # Step through X most frequent n-grams across corpus, the feature is the
        # relative frequency for each n-gram in each text 
        for ngram in ngrams:
            
            freq = freqs.freq(ngram)
            
            #if freq == 0:
            #    unseen = unseen + 1
            #print 'freq', freq
            if GT_SMOOTHING:
                r = freqs[ngram]
                if r > 0: # GT smoothing for seen objects
                    rstar = rsl[r]
                    pr = rstar/float(N)
                    #print ngram, r, pr, freq
                    # re-normalize probability
                    if GT_RENORM:
                        freq = (1-p0_all)*(rstar/Nstar)
                    else:
                        freq = pr
                elif GT_P0:
                    freq = p0
                
                #print 'gtfreq', freq
                #if freqs[ngram] > 0 and a is not None and \
                #b is not None and b <= -1:
                #    freq = gt_smoothing(freqs, N, ngram, a, b, X)
                
            feature_matrix[t].append(freq)
            
    #end = time.time()
    #print os.getpid(), ": Used", (end-start)/n_texts, "seconds per text"
    
    return feature_matrix

# Inefficient version!
#def create_char_ngrams(n_char_ngrams, all_char_ngrams, text_char_ngrams):
#    n_texts = len(text_char_ngrams)
#    print os.getpid(), ": Creating char n-grams features for", n_texts, "texts"
#    feature_matrix = [[] for i in range(n_texts)]
#    
#    # Frequency of all possible n-grams across corpus
#    all_char_ngrams_freqs = FreqDist(all_char_ngrams)
#    # we can't look for more n-grams than we have
#    tot_ngrams = min([n_char_ngrams, all_char_ngrams_freqs.B()])
#    
#    ss = 0
#    start = time.time()
#    # Select char n-gram features
#    for t in range(n_texts):
#        freqs = FreqDist(text_char_ngrams[t])
#        print 'Text', t
#            
#        # Step through X most frequent n-grams across corpus, the feature is the
#        # relative frequency for each n-gram in each text
#        for i in range(tot_ngrams):
#            #ss1 = time.time()
#            ngram = all_char_ngrams_freqs.keys()[i]
#            #ss2 = time.time()
#            #ss = ss + (ss2-ss1)            
#            freq = freqs.freq(ngram)
#            feature_matrix[t].append(freq)
#    end = time.time()
#    print os.getpid(), ": Used", (end-start)/n_texts, "seconds per text"
#    print os.getpid(), ": Used", ss, "seconds on finding keys"
#    return feature_matrix

def wrd_ngram_stats(texts, corpus, n_wrd_ngrams, wrd_ngram_size):
    n_texts = len(texts)
    feature_matrix = [[] for i in range(n_texts)]
    
    all_wd_ngrams = []
    text_wrd_ngrams = []
    
    for text in texts:
        
        if not text.endswith(".txt"):
            continue
        
        wrd_tokens = corpus.words(text)
        empty = len(corpus.raw(text)) == 0

        if not empty:
            lower_wrds = [w.lower() for w in wrd_tokens if w.isalnum()]
            wrd_ng = ngrams(lower_wrds, wrd_ngram_size)
            text_wrd_ngrams.append(wrd_ng)
            all_wd_ngrams.extend(wrd_ng)
        else:
            text_wrd_ngrams.append([])
            
    return all_wd_ngrams, text_wrd_ngrams

# Inefficient version!
#def create_wrd_ngrams(n_wrd_ngrams, all_wd_ngrams, text_wrd_ngrams):
#    print os.getpid(), ": Attaching word n-grams to list of features"
#    n_texts = len(text_wrd_ngrams)
#    feature_matrix = [[] for i in range(n_texts)]
#    all_wrd_ngrams_freqs = FreqDist(all_wd_ngrams)
#        
#    # we can't look for more n-grams than we have
#    tot_ngrams = min([n_wrd_ngrams, all_wrd_ngrams_freqs.B()])
#        
#    start = time.time()
#    # Select word n-gram features
#    for t in range(n_texts):
#        #print os.getpid(), 'Text', t
#        #freqs = text_wrd_ngrams[t]
#        freqs = FreqDist(text_wrd_ngrams[t])
#            
#        # Step through X most frequent n-grams across corpus, the feature is the
#        # relative frequency for each n-gram in each text
#        for r in range(tot_ngrams):
#            ngram = all_wrd_ngrams_freqs.keys()[r] # BUG!!!!!!!!!
#            freq = freqs.freq(ngram)
#            feature_matrix[t].append(freq)
#            
#    end = time.time()
#    print os.getpid(), "I used", (end-start)/n_texts, "seconds per text"
#    
#    return feature_matrix    

def extract_fws(texts, corpus, fw_root):
    n_texts = len(texts)
    feature_matrix = [[] for i in range(n_texts)]
    
    func_wrds = load_wrds(fw_root)
    text_fws = []
    
    for text in texts:
        
        if not text.endswith(".txt"):
            continue
        
        wrd_tokens = corpus.words(text)
        empty = len(corpus.raw(text)) == 0
        
        if not empty:
            lower_wrds = [w.lower() for w in wrd_tokens if w.isalnum()]
            my_func_wrds = [w for w in lower_wrds if func_wrds.count(w) > 0]
            text_fws.append(my_func_wrds)
        else:
            text_fws.append([])
            
    return func_wrds, text_fws

def create_fw_features(func_words, text_fws):
    print "Attaching function words to list of features"
    n_texts = len(text_fws)
    feature_matrix = [[] for i in range(n_texts)]
    for t in range(n_texts):
        print 'Text', t
        freqs = FreqDist(text_fws[t])
        for f in func_words:
            freq = freqs.freq(f)
            feature_matrix[t].append(freq)
            
    return feature_matrix
    
def save_features(feature_file, feature_matrix, class_file, text_classes):
    '''
    Save features of a feature matrix to a file, and a list of classes
    to another file
    '''
    
    print "Outputting features to", feature_file
    ff = open(feature_file,'w')
    for f in feature_matrix:
        strlist = [str(i) for i in f]
        ff.write(" ".join(strlist) + "\n")
    ff.flush()
    
    print "Outputting classes to", class_file
    distinct_classes = list(set(text_classes))
    cf = open(class_file,'w')
    for c in text_classes:
        i = distinct_classes.index(c) + 1
        cf.write(str(i) + "\n")
    cf.flush()
    