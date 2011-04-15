import numpy
import math
import operator

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
        #print '------ Training for', c, 'with', len(mydata), 'texts -------'
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

def nb_trainclass(features, bins):
    '''
    Naive Bayes training for a single class. Uses F features from N texts
    of a given class.
    @param features: A matrix of features for each text, size N x F
    '''
   
    # feature-wise probabilities 
    fpf = []
    
    nbins = len(bins)
    
    for i in range(len(features[0])):
        
        # For each bin; for how many documents did the feature fit into that bin 
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
        minp = 1/float(math.pow(nbins, 3)) # low min. probability for unseen
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
                pf[i] = (fb[i] / float(len(features))) - negp
                if pf[i] <= 0:
                    pf[i] = minp
                    #print 'Too low', minp, totminp, rpos, r0, negp, fb, (fb[i] / float(len(features))),  pf[i]
                    #exit()
        
        #print pf
        #print sum(pf)
        fpf.append(pf)
      
    return fpf

def nb_classify(cps, fcps, classes, data, bins, top=1):
    
    classified = []
    for d in data:
        best = nb_classify_text(cps, fcps, d, bins, top)
        classified.append(best)
    return classified

def nb_classify_text(cps, fcps, tfeat, bins, ntop=1):
    '''
    @param cps: Dict of prior class probabilities, key: class.
    @param fcps: Dict of dict of list of probabilities for each feature-bin.
    1st key: class, 2nd key: feature no., list-index: feature-bin.
    @param tfeat: Features of a text to be classified
    @param bins: Feature-bins, defined by frequency upper-bounds
    
    @return: A list of tuples (class, log(p(class|tfeat))). List will
    hold the ntop classes with best probability. 
    '''
    
    # For each class: Find probability for each feature
    ps = {}
    for c in cps:
        cp = cps[c] # prior class probability
        p = math.log(cp) # using log so we can use addition below
        for i in range(len(tfeat)):
            f = tfeat[i]
            bin = find_feat_bin(f, bins)
            fp = fcps[c][i][bin] # probability for feature belonging to class
            p = p + math.log(fp) # we can add log(p) instead of multiplying p
        ps[c] = p
    
    # Find highest probability and hereby most likely class
    # Start by sorting by probability
    sorted_ps = sorted(ps.iteritems(),key=operator.itemgetter(1),reverse=True)
    
    # Return the top probabilities
    nbest = min([len(sorted_ps),ntop])
    return sorted_ps[:nbest]

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
#    # Old: Construct bins so they range from min to max
#    max = 0
#    min = 1
#    for t in features:
#        s = list(set(sorted(t)))
#        lclmin = s[0]
#        if lclmin == 0:
#            if len(s) > 1:
#                lclmin = s[1]
#            else:
#                lclmin = 1
#        lclmax = s[-1]
#        if lclmin < min:
#            min = lclmin
#        if lclmax > max:
#            max = lclmax
#    print min, max, (max-min)/float(b)
#    return numpy.arange(min,max,(max-min)/float(b)).tolist()

    # New: Construct features so the average feature-value is in the middle bin            
    avg = sum([sum(f) for f in features]) / float(len(features)*len(features[0]))
    print 'avg', avg
    print avg / float(b)
    interval = avg / float(b) * 2 # b/2 bins on each side of the avg
    print 'interval', interval, interval*(b/float(2)) 
    
    return numpy.arange(interval,avg+(((b/2.0)+1)*interval),interval).tolist()
        
    