import numpy
import math

def nb_train(data_classes, data, bins):
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
        fps = nb_trainclass(mydata, bins)
        #print 'X', len(fps[0])
        fcps[c] = fps
        ntexts_perclass[c] = data_classes.count(c)
    
    # Find prior probability for each class
    cps = {}
    ntexts = len(data_classes)
    for c in classes:
        cps[c] = ntexts_perclass[c] / float(ntexts)

    #print cps
    return cps, fcps 

#def nb_trainclass(features, D):

def nb_trainclass(features, bins):
    '''
    Naive Bayes training for a single class. Uses F features from N texts
    of a given class.
    @param features: A matrix of features for each text, size N x F
    '''
   
    fpf = []
    
    #feature_bins = int(math.pow(10, D)) 
    #print 'bins', feature_bins
    nbins = len(bins)
    
    for i in range(len(features[0])):
        
        # For each bin; for how many documents did the feature fit into that bin 
        #fb = [0 for j in range(feature_bins)]
        fb = [0 for j in range(nbins)]
        for row in features:
            
            #f = fr.freq(feature)
            f = row[i] # feature value
            #bin = nbins-1
            #for b in range(nbins):
            #    if f < bins[b]:
            #        bin = b
            #        break
            bin = find_feat_bin(f, bins)
            #print 'f', f, 'bin', bin
            #bin = int(round(f,D) * feature_bins)
            fb[bin] = fb[bin] + 1
        
        #print fb
        # Incorporate a small-sample correction in all probability estimates
        # such that no probability is ever set to be exactly zero
        #minp = 1/float(feature_bins*feature_bins) # min. probability for unseen
        minp = 1/float(nbins*nbins) # min. probability for unseen
        r0 = fb.count(0) # no. of unseen
        #print 'r0', r0
        #totminp = r0 / float(feature_bins*10)
        totminp = r0 * minp # total prob. for unseen 
        #print 'totminp', totminp
        #minp = totminp / float(r0)
        #print 'minp', minp
        #rpos = feature_bins - r0 # no. of seen
        rpos = nbins - r0 # no. of seen
        #print 'rpos', rpos
        negp = totminp / float(rpos) # prob. to subtract from seen probs
        #print 'negp', negp
        
        # Find probabilities
        #pf = [minp for i in range(feature_bins)] # probabilities for each value of a feature in this class
        pf = [minp for i in range(nbins)] # probabilities for each value of a feature in this class
        #for i in range(feature_bins):
        for i in range(nbins):
            if fb[i] != 0:
                # TODO: Correct to divide by docs here?
                pf[i] = (fb[i] / float(len(features))) - negp
        
        #print pf
        #print sum(pf)
        fpf.append(pf)
      
    return fpf

#def nb_classify(cps, fcps, classes, data, D):

def nb_classify(cps, fcps, classes, data, bins):
    
    classified = []
    for i in range(len(data)):
        d = data[i]
        #bestc, bestp = nb_classify_text(cps, fcps, d, D)
        bestc, bestp = nb_classify_text(cps, fcps, d, bins)
        classified.append(bestc)
    return classified
    #print bestc, bestp

#def nb_classify_text(cps, fcps, tfeat, D):

def nb_classify_text(cps, fcps, tfeat, bins):
    '''
    @param cps: Dict of prior class probabilities
    @param fcps: Dict of probabilities for each feature occurring in the class (key)
    @param tfeat: Features of a text to be classified
    
    @return: A tuple c, p. c is the class that the tfeat most likely
    occur in. p is the probability with which they occur.
    '''
    #feature_bins = int(math.pow(10, D))
    #nbins = len(bins) 
    
    # For each class: Find probability for each feature
    ps = {}
    for c in cps:
        cp = cps[c] # prior class probability
        p = math.log(cp)
        #p = cp
        #print 'Before', cp, p
        for i in range(len(tfeat)):
            f = tfeat[i]
            #print f
            #bin = int(round(f,D) * feature_bins)
            bin = find_feat_bin(f, bins)
            fp = fcps[c][i][bin] # probability for feature belonging to class
            p = p + math.log(fp)
            #p = p * fp
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

def find_feat_bin(f, bins):
    '''
    Find the bin that a feature fits into.
    @param bins: Holds upper-bounds of each bin.
    '''
    nbins = len(bins)
    bin = nbins-1
    for b in range(nbins):
        if f < bins[b]:
            bin = b
            break
    return bin
    
def build_feat_bins(features, b):
    '''
    Build a list of feature-bins. Each bin is represented
    by the upper-bound of the bin. Given features are expected to be
    floats between 0 and 1.
    @return: A list of upper-bounds for each of b bins.
    '''
    max = 0
    min = 1
    for t in features:
        s = list(set(sorted(t)))
        lclmin = s[0]
        if lclmin == 0:
            if len(s) > 1:
                lclmin = s[1]
            else:
                lclmin = 1
        lclmax = s[-1]
        if lclmin < min:
            min = lclmin
        if lclmax > max:
            max = lclmax
    
    return numpy.arange(min,max,(max-min)/float(b)).tolist()
        
    