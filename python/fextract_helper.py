from nltk.util import ngrams
from nltk.probability import FreqDist, SimpleGoodTuringProbDist
from nltk.corpus import PlaintextCorpusReader
import os
from goodturing import GoodTuring
import kneserney
import csv

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

def wrd_ngram_stats(texts, corpus, order, include_lower=False):
    #n_texts = len(texts)
    #feature_matrix = [[] for i in range(n_texts)]
    
    all_wd_ngrams = FreqDist()
    text_wrd_ngrams = []
    
    for text in texts:
        
        if not text.endswith(".txt"):
            continue
        
        wrd_tokens = corpus.words(text)
        empty = len(corpus.raw(text)) == 0
        
        # One freq. dist per n
        text_ngrams = []
        for _ in range(order):
            text_ngrams.append(FreqDist())

        if not empty:
            lower_wrds = [w.lower() for w in wrd_tokens if w.isalnum()]
            
            if include_lower:
                for n in range(1, order+1):
                    wd_ng = ngrams(lower_wrds, n)
                    text_ngrams[n-1].update(wd_ng)
                    if n == order:
                        all_wd_ngrams.update(wd_ng)
            else:
                wd_ng = ngrams(lower_wrds, order)
                text_ngrams[order-1].update(wd_ng)
                all_wd_ngrams.update(lower_wrds)
                
#            wrd_ng = ngrams(lower_wrds, wrd_ngram_size)
#            text_wrd_ngrams.append(wrd_ng)
#            all_wd_ngrams.extend(wrd_ng)
        #else:
        #    text_wrd_ngrams.append([])
        text_wrd_ngrams.append(text_ngrams)
            
    return all_wd_ngrams, text_wrd_ngrams

def char_ngram_stats(texts, corpus, order, include_lower=False):
    '''
    Find character n-grams in some texts.
    @param texts: List of texts
    @param corpus: The corpus that holds the texts
    @param order: The order of the n-grams to consider.
    @param include_lower: Whether to include list of lower-order n-grams in output
    @return: A tuple: First element is a list of all n-grams (only of
    given order) across all texts. Second element is a a matrix with a list of
    lists of 1-grams, 2-grams, ..., n-grams per text.
    ''' 
    
    all_char_ngrams = FreqDist()
    text_char_ngrams = [] # Char n-grams found in each text
    
    for text in texts:
        #print text
        
        if not text.endswith(".txt"):
            continue
        
        empty = len(corpus.raw(text)) == 0 
    
        # One freq. dist per n
        text_ngrams = []
        for _ in range(order):
            text_ngrams.append(FreqDist())
            
        if not empty:
            text_str = corpus.raw(text).replace('\r','').replace('\n', ' ')
            
            if include_lower:
                for n in range(1, order+1):
                    char_ng = ngrams(text_str, n)
                    text_ngrams[n-1].update(char_ng)
                    if n == order:
                        all_char_ngrams.update(char_ng)
            else:
                char_ng = ngrams(text_str, order)
                text_ngrams[order-1].update(char_ng)
                all_char_ngrams.update(char_ng)
            
        text_char_ngrams.append(text_ngrams)
            
    return all_char_ngrams, text_char_ngrams

def create_ngram_feats(ngrams, order, text_fds, cg_representation=False, kn_smooth=False, gt_smooth=False):
    '''
    Create n-gram features for each text, using the list of n-grams
    to consider given in ngrams argument. Can be used for both
    chars and words
    @param order: Size of n-gram, where order > 1
    @param cg_representation: The probability of an ngram is calculated as in CG98
    @param kn_smooth: Whether to use Kneser-Ney smoothing
    '''
    
    # We can only use one kind of smoothing
    if kn_smooth and gt_smooth:
        print 'Cannot use two types of smoothing. Exiting...'
        exit()
    
    n_texts = len(text_fds)
    print os.getpid(), ": Creating n-grams features for", n_texts, "texts"
    feature_matrix = [[] for i in range(n_texts)]
    
    #start = time.time()
    # Select char n-gram features
    for t in range(n_texts):
        
        # Frequencies for n-gram
        #freqs = FreqDist(text_ngrams[t][order-1])
        freqs = text_fds[t][order-1]
        
        if gt_smooth:
            
            # TODO: Gt smoothing does not use CG representation
            gts = []
            
            # Frequencies
            rl = sorted(list(set(freqs.values()))) # list of r
            # Frequencies of frequencies
            nrl = []
            for r in rl:
                nrl.append(freqs.Nr(r))
                
            unseen = 0
            for ngram in ngrams:
                if freqs[ngram] == 0: # This checks r == 0
                    unseen = unseen + 1
            #print 'un', unseen, freqs.B()
                
            gt = GoodTuring(rl, nrl, freqs.N(), unseen)
            #gt_freq = SimpleGoodTuringProbDist(freqs, freqs.B()+unseen)
        
        # Step through X most frequent n-grams across corpus, the feature is the
        # relative frequency for each n-gram in each text 
        for ngram in ngrams:
            
            #if freq == 0:
            #    unseen = unseen + 1
            #print 'freq', freq
            if gt_smooth:
                
                if cg_representation:
                    pass # TODO: Gt smoothing does not use CG representation
                else:
                    r = freqs[ngram]
                    freq = gt.prob(r)
                    #print r
                    #print 'myfreq', freq
                    #print 'defreq', gt_freq.prob(ngram)
            
            elif kn_smooth:
                freq = kneserney.modkn(ngram, text_fds[t])
            
            elif cg_representation:
                freq = 0
                occurrences = freqs[ngram]
                if occurrences > 0:
                    lowerord_ng = ngram[:-1]
                    c_sum = text_fds[t][order-2][lowerord_ng]
                    #print ngram, lowerord_ng, occurrences, c_sum
                    freq = occurrences / float(c_sum)
                #if ngram == (u't', u'h', u'e'):
                #    print ngram, occurrences, c_sum, freq, freqs.freq(ngram)
            else:
                freq = freqs.freq(ngram)
                
            feature_matrix[t].append(freq)
        
        #print sum(feature_matrix[t])
            
    #end = time.time()
    #print os.getpid(), ": Used", (end-start)/n_texts, "seconds per text"
    
    return feature_matrix

##  Only used for multi-version

#def get_text_cngs(texts, corpus_root, ngram_size):
#    '''
#    For each text, get a list of all char n-grams occurring the text
#    '''
#    
#    ngs = []
#    corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding='UTF-8')
#    for text in texts:
#        
#        if not text.endswith(".txt"):
#            continue
#    
#        if not len(corpus.raw(text)) == 0:
#            text_str = corpus.raw(text).replace('\r','').replace('\n', ' ')
#            char_ng = ngrams(text_str, ngram_size)
#            ngs.append(char_ng)
#        else:
#            ngs.append([])
#            
#    return ngs

## Only used for multi-version ##

#def get_cngs(texts, corpus_root, ngram_size):
#    '''
#    Get a list of all char n-grams occurring in some texts
#    '''
#    
#    ngs = []
#    
#    corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding='UTF-8')
#    for text in texts:
#        
#        if not text.endswith(".txt"):
#            continue
#    
#        if not len(corpus.raw(text)) == 0:
#            text_str = corpus.raw(text).replace('\r','').replace('\n', ' ')
#            char_ng = ngrams(text_str, ngram_size)
#            ngs.extend(char_ng)
#            
#    return ngs 

    

   
# TODO: Not used(?)
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

# TODO: Not used(?)
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
    
def save_features(feature_file=None, feature_matrix=None,\
                  class_file=None, text_classes=None, orig_classes=False):
    '''
    Save features of a feature matrix to a file, and a list of classes
    to another file
    '''
    
    if feature_file is not None and feature_matrix is not None:
        print "Outputting features to", feature_file
        ff = open(feature_file,'w')
        for f in feature_matrix:
            strlist = [str(i) for i in f]
            ff.write(" ".join(strlist) + "\n")
        ff.flush()
    
    if class_file is not None and text_classes is not None:
        print "Outputting classes to", class_file
        distinct_classes = list(set(text_classes))
        cf = open(class_file,'w')
        for c in text_classes:
            i = distinct_classes.index(c) + 1
            cf.write(str(i) + "\n")
        cf.flush()
        
def load_features(feature_file):
    
    feature_matrix = []
    ff = open(feature_file, 'r')
    ffr = csv.reader(ff, delimiter=' ')
    for f in ffr:
        l = []
        for x in f:
            l.append(float(x))
        feature_matrix.append(l)
    ff.close()
    return feature_matrix
    