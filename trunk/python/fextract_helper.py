from nltk.util import ngrams
from nltk.probability import FreqDist
from nltk.corpus import PlaintextCorpusReader
import os
import time
import math
import goodturing

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
    
    all_char_ngrams = [] # All n-grams found in entire corpus
    text_char_ngrams = [] # Char n-grams found in each text
    
    for text in texts:
        #print text
        
        if not text.endswith(".txt"):
            continue
        
        empty = len(corpus.raw(text)) == 0 
    
        # One list per n
        text_ngrams = []
        for _ in range(order):
            text_ngrams.append([])
            
        if not empty:
            text_str = corpus.raw(text).replace('\r','').replace('\n', ' ')
            
            if include_lower:
                for n in range(1, order+1):
                    char_ng = ngrams(text_str, n)
                    text_ngrams[n-1] = char_ng
                    if n == order:
                        all_char_ngrams.extend(char_ng)
            else:
                char_ng = ngrams(text_str, order)
                text_ngrams[order-1] = char_ng
                all_char_ngrams.extend(char_ng)
            
        text_char_ngrams.append(text_ngrams)
            
    return all_char_ngrams, text_char_ngrams

# TODO: Only used for multi-version
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

# TODO: Only used for multi-version
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

    
def create_ngram_feats(ngrams, order, text_ngrams, cg_representation=False):
    '''
    Create n-gram features for each text, using the list of n-grams
    to consider given in ngrams argument. Can be used for both
    chars and words
    @param order: Size of n-gram, where order > 1
    @param cg_representation: The probability of an ngram is calculated as in CG98
    '''
    GT_SMOOTHING = False
    GT_RENORM = True
    GT_P0 = True
    
    n_texts = len(text_ngrams)
    print os.getpid(), ": Creating n-grams features for", n_texts, "texts"
    feature_matrix = [[] for i in range(n_texts)]
    
    #start = time.time()
    # Select char n-gram features
    for t in range(n_texts):
        
        # Frequencies for n-gram
        freqs = FreqDist(text_ngrams[t][order-1])
        
        # Frequencies for n-1-gram
        if cg_representation:
            lowerord_fd = FreqDist(text_ngrams[t][order-2])
        
        if GT_SMOOTHING:
            
            # Frequencies
            rl = sorted(list(set(freqs.values()))) # list of r
            # Frequencies of frequencies
            nrl = []
            for r in rl:
                nrl.append(freqs.Nr(r))
            #print rl
            #print nrl
            
            # Find parameters for smoothed Nr
            a, b, X = goodturing.gt_nr_smooth(rl, nrl)
            N = freqs.N()
            p0_all = 1.0
            if N > 0: 
                p0_all = freqs.Nr(1) / float(N) # Probability for all unseen objects
            #print 'p0_all', p0_all
            # Dict of r,r*
            #print 'X', X
            
            
            rsl = goodturing.gt_r_est(rl, nrl, a, b, X)
            #print rsl
            # Nstar is the total number of objects, using estimated r
            Nstar = 0
            for p in rsl.items():
                Nr = freqs.Nr(p[0])
                Nstar = Nstar + (Nr * p[1])
            #if Nstar == 0:
            #    print 'X', X
            #    print freqs.items()
            
            # Calculate p0 for unseen (r == 0) ngrams
            unseen = 0
            for ngram in ngrams:
                if freqs[ngram] == 0: # This checks r == 0
                    unseen = unseen + 1
            if unseen > 0:
                p0 = p0_all / float(unseen)   
                print 'Unseen', unseen, 'p0', p0         
        
        # Step through X most frequent n-grams across corpus, the feature is the
        # relative frequency for each n-gram in each text 
        for ngram in ngrams:
            
            if cg_representation:
                freq = 0
                occurrences = freqs[ngram]
                if occurrences > 0:
                    lowerord_ng = ngram[:-1]
                    c_sum = lowerord_fd[lowerord_ng]
                    #print ngram, lowerord_ng, occurrences, c_sum
                    freq = occurrences / float(c_sum)
                print freq, freqs.freq(ngram)
            else:
                freq = freqs.freq(ngram)
            
            #if freq == 0:
            #    unseen = unseen + 1
            #print 'freq', freq
            if GT_SMOOTHING:
                r = freqs[ngram]
                if r > 0: # GT smoothing for seen objects
                    rstar = rsl[r]
                    pr = rstar/float(N)
                    #print ngram, pr
                    # re-normalize probability
                    if GT_RENORM:
                        freq = (1-p0_all)*(rstar/Nstar)
                    else:
                        freq = pr
                elif GT_P0:
                    freq = p0
                
                # TODO: In personae, all word ngrams have freq = 0
                #print ngram, freq
                #if freqs[ngram] > 0 and a is not None and \
                #b is not None and b <= -1:
                #    freq = gt_r_est(freqs, N, ngram, a, b, X)
                
            feature_matrix[t].append(freq)
        
        #print sum(feature_matrix[t])
            
    #end = time.time()
    #print os.getpid(), ": Used", (end-start)/n_texts, "seconds per text"
    
    return feature_matrix


# TODO: Has only been used for baseline tests
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
    