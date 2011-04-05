import fextract_helper
from nltk.probability import FreqDist
from nltk.corpus import PlaintextCorpusReader
import numpy

n_char_ngrams = 10
char_ngram_size = 3 

corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/a1_005_10"

def nb_train(text_classes, text_ngrams):
    
    classes = list(set(text_classes))
    
    # For each class: make frequency distribution and
    # calculate prior class probability
    cngrams = {} # all ngrams per class
    cfreqs = {} # frequency distribution of ngrams per class
    nds = {} # no. of texts per class
    cps = {} # prior probability per class
    d = len(text_classes) # no. of texts
    
    for t in range(len(text_ngrams)):
        c = text_classes[t] # text class
        if not cngrams.has_key(c):
            cngrams[c] = []
        cngrams[c].extend(text_ngrams[t])
        if not nds.has_key(c):
            nds[c] = 0
        nds[c] = nds[c] + 1
    for c in classes:
        cfreqs[c] = FreqDist(cngrams[c])
        cps[c] = nds[c] / float(d)

    print cfreqs
    #print cps
    return cfreqs, cps

def nb_classify(text_classes, text_ngrams, ngrams, cfreqs, cps):
    
    classes = list(set(text_classes))
    
    for t in len(text_classes):
        pc = {} # prosterior probability for each class that the text belongs to that class 
     
        freqs = FreqDist(text_ngrams[t])
        
        for c in classes:
     
            cfreq = cfreqs[c] # freq. dist across entire training texts for class
            cp = cps[c] # prior prob. for class
            
            for ngram in ngrams:
                r = freqs[ngram]
                
        


def k_fold_cv(X, K, randomise = False):
    """
    From http://code.activestate.com/recipes/521906/
    Generates K (training, validation) pairs from the items in X.

    Each pair is a partition of X, where validation is an iterable
    of length len(X)/K. So each training iterable is of length (K-1)*len(X)/K.

    If randomise is true, a copy of X is shuffled before partitioning,
    otherwise its order is preserved in training and validation.
    """
    if randomise: from random import shuffle; X=list(X); shuffle(X)
    for k in xrange(K):
        training = [x for i, x in enumerate(X) if i % K != k]
        validation = [x for i, x in enumerate(X) if i % K == k]
        yield training, validation

#X = [i for i in xrange(97)]
#for training, validation in k_fold_cross_validation(X, K=7):
#    for x in X: assert (x in training) ^ (x in validation), x
## end of http://code.activestate.com/recipes/521906/ }}}
 
    

if __name__ == '__main__':
    
    corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding='UTF-8')
    texts = corpus.fileids()
    text_classes = fextract_helper.find_classes(texts)
    
    
    all_ngrams, text_ngrams = fextract_helper.char_ngram_stats(texts, corpus, n_char_ngrams, char_ngram_size)
    afreqs = FreqDist(all_ngrams)
    tot_cngs = min([n_char_ngrams, afreqs.B()])
    mostfreq_ngs = afreqs.keys()[:tot_cngs]
    
    nb_train(text_classes[:20],text_ngrams[:20])
    
    # TODO: NOT STRATIFIED!!
    #k = 4
    #folds = k_fold_cv(text_classes,k)
    #for train, test in folds:
        
        
    
    
    #tfreqs = []
    #for ngrams in text_ngrams:
    #    tfreqs.append(FreqDist(ngrams))
    
    # --------- TRAINING --------- #
    
    
    
    #    pcs = {} # for each class, the probability of each feature occurring in the class
    #    for o in range(len(mostfreq_ngs)):
    #        
    #        ngram = mostfreq_ngs[o]
    #        N = afreqs[ngram]
    #        #print ngram, 'N', N
    #    
    #        crs = {} # for each class, the number of occurrences for the ngram in question
    #        
    #        for t in range(len(texts)):
    #        
    #            c = text_classes[t] # text class
    #            
    #            if not crs.has_key(c):
    #                crs[c] = 0
    #        
    #            freqs = tfreqs[t] # object frequencies for the current text
    #        
    #            crs[c] = crs[c] + freqs[ngram]
    #            
    #        #print crs
    #        
    #        for c in crs:
    #            
    #            if not pcs.has_key(c):
    #                pcs[c] = [0 for i in range(len(mostfreq_ngs))]
    #        
    #            #print crs[c]
    #            pcs[c][o] = crs[c] / float(N)
    #    
    #    #for p in pcs:
    #    #    print pcs[p][2]
    #    
    #    # argmax c
    #    
    #    for c in classes:
    #        pass
        
    # --------- TEST --------- #
        
    