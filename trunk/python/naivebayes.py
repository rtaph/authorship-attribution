import numpy
import math
import operator

class NaiveBayes:

    def __init__(self, bins):
        self.bins = bins

    def train(self, data_classes, data):
        '''
        Train Naive Bayes classifier
        '''
        
        print 'Training classifier with', len(data), 'texts'
        classes = list(set(data_classes))    
        ntexts_perclass = {} # no. of texts per class
        
        # Find probability for a feature having a specific value
        # given a class
        self.fcps = {}
        for c in classes:
            mydata = []
            for i in range(len(data_classes)):
                if data_classes[i] == c:
                    mydata.append(data[i])
            # feature probabilities (no. of features x no. of feature bins)
            fps = self._trainclass(mydata)
            self.fcps[c] = fps
            ntexts_perclass[c] = data_classes.count(c)
        
        # Find prior probability for each class
        self.cps = {}
        ntexts = len(data_classes)
        for c in classes:
            self.cps[c] = ntexts_perclass[c] / float(ntexts)
    
    def _trainclass(self, features):
        '''
        Naive Bayes training for a single class. Uses F features from N texts
        of a given class.
        @param features: A matrix of features for each text, size N x F
        '''
       
        # feature-wise probabilities 
        fpf = []
        
        nbins = len(self.bins)
        
        for i in range(len(features[0])): # For each feature
            
            # For each bin; for how many documents did the feature fit into that bin 
            fb = [0 for j in range(nbins)]
            for row in features:
                f = row[i] # feature value for the current feature in current text
                bin = find_feat_bin(f, self.bins)
                fb[bin] = fb[bin] + 1
            
            # Incorporate a small-sample correction in all probability estimates
            # such that no probability is ever set to be exactly zero
            minp = 1/float(math.pow(nbins, 3)) # low min. probability for unseen
            r0 = fb.count(0) # no. of unseen
            totminp = r0 * minp # total prob. for unseen 
            rpos = nbins - r0 # no. of seen
            negp = totminp / float(rpos) # prob. to subtract from seen probs
            
            # Find probabilities
            pf = [minp for i in range(nbins)] # probabilities for each value of a feature in this class
            for i in range(nbins):
                if fb[i] != 0:
                    pf[i] = (fb[i] / float(len(features))) - negp
                    if pf[i] <= 0:
                        pf[i] = minp
            
            fpf.append(pf)
          
        return fpf
    
    def classify(self, data, top=1):
        
        print 'Classifying', len(data), 'texts...'
        classified = []
        for d in data:
            best = self._classify_text(d, top)
            classified.append(best)
        return classified
    
    def _classify_text(self, tfeat, ntop=1):
        '''
        @param tfeat: Features of a text to be classified
        
        @return: A list of tuples (class, log(p(class|tfeat))). List will
        hold the ntop classes with best probability. 
        '''
        
        # For each class: Find probability for each feature
        ps = {}
        for c in self.cps:
            cp = self.cps[c] # prior class probability
            p = math.log(cp) # using log so we can use addition below
            for i in range(len(tfeat)):
                f = tfeat[i]
                bin = find_feat_bin(f, self.bins)
                try:
                    fp = self.fcps[c][i][bin] # probability for feature belonging to class
                except Exception:
                    print c, i, bin
                    print self.cps.keys()
                    print self.fcps.keys()
                    exit()
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

    # New: Construct features so the average feature-value is in the middle bin            
    avg = sum([sum(f) for f in features]) / float(len(features)*len(features[0]))
    interval = (avg/float(b)) * 2 # b/2 bins on each side of the avg    
    return numpy.arange(interval,avg+(((b/2.0)+1)*interval),interval).tolist()
        
    