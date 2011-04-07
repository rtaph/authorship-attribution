import fextract_helper
from nltk.probability import FreqDist
from nltk.corpus import PlaintextCorpusReader
import numpy
import math
import util

n_char_ngrams = 10
char_ngram_size = 3 

corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/a1_005_10"

def nb_train(data_classes, data, features, D):
    '''
    Train Naive Bayes classifier
    @param ctfeatures: Class-text features: For each class, the texts that
    belong to the class and for each text the features that are found in the
    text
    @param features: The features that should be taken into account 
    
    @return: Prior class probabilities, 
    '''
    
    classes = list(set(data_classes))    
    ntexts_perclass = {} # no. of texts per class
    
    fcps = {}
    for c in classes:
        mydata = []
        for i in range(len(data_classes)):
            if data_classes[i] == c:
                mydata.append(data[i])
        fps = nb_trainclass(mydata, features, D) # feature probabilities (no. of features x no. of feature bins)
        #print 'X', len(fps[0])
        fcps[c] = fps
        ntexts_perclass[c] = data_classes.count(c)
    
    cps = {} # prior probability per class
    ntexts = len(text_classes) # no. of texts
    
    # Find prior probability for each class
    for c in classes:
        cps[c] = ntexts_perclass[c] / float(ntexts)

    return cps, fcps 

def nb_trainclass(data, features, D):
    '''
    Naive Bayes training for a single class.
    @param data: Features of the class
    @param features: Features to look for
    '''
    
    # Frequency distributions for each text in data
    # TODO: Should not depend on nltk module
    freqs = []
    for d in data:
        freqs.append(FreqDist(d))
   
    fpf = []
     
    for feature in features:
        feature_bins = int(math.pow(10, D))
        #print 'bins', feature_bins
        
        #l = range(feature_bins)
        
        # For each bin; for how many documents did the feature fit into that bin 
        fb = [0 for i in range(feature_bins)]
        for fr in freqs:
            # TODO: This could be smoothed...?
            f = fr.freq(feature)
            #print f
            bin = int(round(f,D) * feature_bins)
            fb[bin] = fb[bin] + 1
        
        #print fb
        # Incorporate a small-sample correction in all probability estimates
        # such that no probability is ever set to be exactly zero
        minp = 1/float(feature_bins*feature_bins) # min. probability for unseen
        r0 = fb.count(0) # no. of unseen
        #print 'r0', r0
        #totminp = r0 / float(feature_bins*10)
        totminp = r0 * minp # total prob. for unseen 
        #print 'totminp', totminp
        #minp = totminp / float(r0)
        #print 'minp', minp
        rpos = feature_bins - r0 # no. of seen
        #print 'rpos', rpos
        negp = totminp / float(rpos) # prob. to subtract from seen probs
        #print 'negp', negp
        
        # Find probabilities
        pf = [minp for i in range(feature_bins)] # probabilities for each value of a feature in this class
        for i in range(feature_bins):
            if fb[i] != 0:
                # TODO: Correct to divide by docs here?
                pf[i] = (fb[i] / float(len(data))) - negp
        
        #print pf
        #print sum(pf)
        fpf.append(pf)
      
    return fpf

def nb_classify(cps, fcps, classes, data):
    
    for d in data:
        bestc, bestp = nb_classify_text(cps, fcps, d)
        print bestc, bestp

def nb_classify_text(cps, fcps, tfeat):
    '''
    @param cps: Dict of prior class probabilities
    @param fcps: Dict of probabilities for each feature occurring in the class (key)
    @param tfeat: Features of a text to be classified
    
    @return: A tuple c, p. c is the class that the tfeat most likely
    occur in. p is the probability with which they occur.
    '''
    
    # For each class: Find probability for tfeat belonging to class
    ps = {}
    for c in cps:
        cp = cps[c] # prior class probability
        p = math.log(cp)
        for f in tfeat:
            print f
            fp = fcps[c][f] # probability for feature belonging to class
            p = p + math.log(fp)
        ps[c] = p
    
    # Find highest probability and hereby most likely class
    bestc = None
    bestp = 0
    for c in ps:
        p = ps[c] # probability for assigning text to class
        if p > bestp: # found better probability
            bestc = c
            bestp = p
    
    return bestc, bestp

if __name__ == '__main__':
    
    corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding='UTF-8')
    texts = corpus.fileids()
    text_classes = fextract_helper.find_classes(texts)
    #classes = list(set(text_classes))
    
    all_ngrams, text_ngrams = fextract_helper.char_ngram_stats(texts, corpus, n_char_ngrams, char_ngram_size)
    
    # Determine features
    afreqs = FreqDist(all_ngrams)
    tot_cngs = min([n_char_ngrams, afreqs.B()])
    features = afreqs.keys()[:tot_cngs]
    
    # TODO: Should be calculated (?)
    d = 3
    feature_bins = int(math.pow(10, d))
    
    # Cross-validation
    K = 3
    k_indices = util.k_fold_cv_ind(text_classes,K)
    for k in range(K):
        trainc = [text_classes[i] for i in range(len(text_classes)) if k_indices[i] != k]
        traint = [text_ngrams[i] for i in range(len(text_ngrams)) if k_indices[i] != k]
        testc = [text_classes[i] for i in range(len(text_classes)) if k_indices[i] == k]
        testt = [text_ngrams[i] for i in range(len(text_ngrams)) if k_indices[i] == k]
        

        
        featfreqs = []
        for t in testt:
            freqs = FreqDist(t)
            f = [] # features for this text
            for feat in features:
                bin = int(round(freqs.freq(feat),d) * feature_bins)
                print 'bin', bin
                f.append(bin)
            featfreqs.append(f)
        
        print trainc
        print testc
    
        # TODO: Extract features that we need before calling the functions below?
    
        cps, fcps = nb_train(trainc, traint, features, d)
        nb_classify(cps, fcps, testc, featfreqs)
        
    #print cps
    #for x in fcps['620124']:
    #    print x
    
    
            

    
#    for j in l:
#        
#        # find bin
#        freq = freqs
#    
#    bla = 10
#    s = 0
#    for i in range(bla):
#        print freqs[i][(u' ', u't', u'h')]
#        print freqs[i].freq((u' ', u't', u'h'))
#        s = s + freqs[i][(u' ', u't', u'h')]
#    avg = s / float(bla)
#    print 'Avg', avg
#    
#    # pop. variance
#    b = 0
#    for i in range(bla):
#        b = b + math.pow(freqs[i][(u' ', u't', u'h')] - avg,2)
#    varsq = 1/float(bla) *  b
#    print 'Var', math.sqrt(varsq)
#    
#    v = 34.3
#    print 1/math.sqrt(2*math.pi*varsq)
#    print math.pow(v-avg,2)
#    print -(math.pow(v-avg,2)/2*varsq)
#    print math.pow(math.e,-(math.pow(v-avg,2)/2*varsq))
#    p = 1/math.sqrt(2*math.pi*varsq)*math.pow(math.e,-(math.pow(v-avg,2)/2*varsq))
#    print 'p', p
        
    