import fextract_helper
from nltk.probability import FreqDist
from nltk.corpus import PlaintextCorpusReader
import numpy
import math
import util

n_char_ngrams = 10
char_ngram_size = 3 

corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/a1_005_10"

def nb_train(data_classes, data, D):
    '''
    Train Naive Bayes classifier
        
    @return: Prior class probabilities, 
    '''
    
    classes = list(set(data_classes))    
    ntexts_perclass = {} # no. of texts per class
    
    # Find probability for a feature having a specific value
    # given a class
    fcps = {}
    for c in classes:
        mydata = []
        for i in range(len(data_classes)):
            if data_classes[i] == c:
                mydata.append(data[i])
        # feature probabilities (no. of features x no. of feature bins)
        print 'Training for', c, 'with', len(mydata), 'texts'
        fps = nb_trainclass(mydata, D)
        #print 'X', len(fps[0])
        fcps[c] = fps
        ntexts_perclass[c] = data_classes.count(c)
    
    # Find prior probability for each class
    cps = {}
    ntexts = len(text_classes)
    for c in classes:
        cps[c] = ntexts_perclass[c] / float(ntexts)

    #print cps
    return cps, fcps 

def nb_trainclass(features, D):
    '''
    Naive Bayes training for a single class. Uses F features from N texts
    of a given class.
    @param features: A matrix of features for each text, size N x F
    '''
   
    fpf = []
    
    feature_bins = int(math.pow(10, D)) 
    #print 'bins', feature_bins
    
    for i in range(len(features[0])):
        
        # For each bin; for how many documents did the feature fit into that bin 
        fb = [0 for j in range(feature_bins)]
        for row in features:
            
            #f = fr.freq(feature)
            f = row[i] # feature value
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
                pf[i] = (fb[i] / float(len(features))) - negp
        
        #print pf
        #print sum(pf)
        fpf.append(pf)
      
    return fpf

def nb_classify(cps, fcps, classes, data, D):
    
    classified = []
    for i in range(len(data)):
        d = data[i]
        c = classes[i]
        bestc, bestp = nb_classify_text(cps, fcps, d, D)
        classified.append(bestc)
    return classified
    #print bestc, bestp

def nb_classify_text(cps, fcps, tfeat, D):
    '''
    @param cps: Dict of prior class probabilities
    @param fcps: Dict of probabilities for each feature occurring in the class (key)
    @param tfeat: Features of a text to be classified
    
    @return: A tuple c, p. c is the class that the tfeat most likely
    occur in. p is the probability with which they occur.
    '''
    feature_bins = int(math.pow(10, D)) 
    
    # For each class: Find probability for each feature
    ps = {}
    for c in cps:
        cp = cps[c] # prior class probability
        #p = math.log(cp)
        p = cp
        #print 'Before', cp, p
        for i in range(len(tfeat)):
            f = tfeat[i]
            #print f
            bin = int(round(f,D) * feature_bins)
            fp = fcps[c][i][bin] # probability for feature belonging to class
            #fp = fcps[c][i][f] # probability for feature belonging to class
            #p = p + math.log(fp)
            p = p * fp
        #print p
        ps[c] = p
    
    # Find highest probability and hereby most likely class
    bestc = None
    bestp = None
    for c in ps:
        p = ps[c] # probability for assigning text to class
        if bestp is None or p > bestp: # found better probability
            bestc = c
            bestp = p
    
    return bestc, bestp

if __name__ == '__main__':
    
    corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding='UTF-8')
    texts = corpus.fileids()
    text_classes = fextract_helper.find_classes(texts)
    ntexts = len(texts)
    #classes = list(set(text_classes))
    
    all_ngrams, text_ngrams = fextract_helper.char_ngram_stats(texts, corpus, n_char_ngrams, char_ngram_size)
    
    # Determine features
    afreqs = FreqDist(all_ngrams)
    tot_cngs = min([n_char_ngrams, afreqs.B()])
    mostfreqngs = afreqs.keys()[:tot_cngs]
    
    # TODO: This could be smoothed...?
    # Calculate features for each text
    features = []
    for t in text_ngrams:
        myfeats = [] # features for the current text
        freqdist = FreqDist(t)
        for f in mostfreqngs:
            myfeats.append(freqdist.freq(f))
        features.append(myfeats)
    
    # TODO: Should be calculated (?)
    d = 3
    feature_bins = int(math.pow(10, d))
    
    # Cross-validation
    K = 3
    k_indices = util.k_fold_cv_ind(text_classes,K)
    
    for k in range(K):
        
        print '---------------   k=' + str(k) + '  ------------------'
        
        trainc = [text_classes[i] for i in range(len(text_classes)) if k_indices[i] != k]
        traint = [features[i] for i in range(len(features)) if k_indices[i] != k]
        testc = [text_classes[i] for i in range(len(text_classes)) if k_indices[i] == k]
        testt = [features[i] for i in range(len(features)) if k_indices[i] == k]
        
        print 'Train texts:', len(traint)
        print 'Test texts:', len(testt)
    
        cps, fcps = nb_train(trainc, traint, d)
        classified = nb_classify(cps, fcps, testc, testt, d)
        
        correct = 0
        for i in range(len(classified)):
            if classified[i] == testc[i]:
                correct = correct + 1
        print 'A:', correct / float(len(testc))
        
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
        
    