import math
import util

class GoodTuring:
    
    def __init__(self, rl, nrl, N, unseen):
        self._rl = rl
        self._nrl = nrl
        self._N = N
        self._gt_nr_smooth() # finds a, b, X
        self._gt_r_est() # finds rsl
        
        # Probability for all unseen objects
        Nr1 = 0
        for i, r in enumerate(self._rl):
            if r == 1:
                Nr1 = self._nrl[i]
                break
        self._p0_all = 1.0
        if self._N > 0:
            self._p0_all = Nr1 / float(self._N)
        
        # Calculate p0 for unseen (r == 0) ngrams
        self._p0 = self._p0_all
        if unseen > 0:
            self._p0 = self._p0_all / float(unseen)
            
        self._renormalize() # finds renormalization parameter
        
    def _gt_r_est(self):
        '''
        Good-Turing smoothing: Find r* estimates for all r>=1
        @param rl: Integer-list of frequencies, r where r >= 1
        @param nrl: List of integer-frequencies of frequencies (Nr)
        @param a, b: Parameters of linear regression log(Nr) = a + b*log(r) that
        estimate Nr
        @param X: The first value of r to start using smoothed Nr's
        @return: Dictionary with key=r, value=r*
        '''
        
        self._rsl = {} # dict of r,r*
        
        for i in range(len(self._rl)):
            
            r = self._rl[i]
            nr = self._nrl[i] # Nr
            nr1 = 0 # The next Nr
            if i < len(self._rl)-1:
                nr1 = self._nrl[i+1]
            
            if self._a is not None and self._b is not None and self._b <= -1: 
                if nr == 0 or r >= self._X: # Good-Turing estimate for high r
                    #nr = math.pow(10, a + (b*math.log10(r)))
                    nr = math.exp(self._a + (self._b*math.log(r)))
                if r+1 >= self._X:
                    nr1 = math.exp(self._a + (self._b*math.log(r+1)))
        
            
            #print 'blu', r, math.pow(10, a + (b*math.log10(r)))
            rstar = (r+1) * (nr1/float(nr)) # calculate r*
            #print 'r, rstar', r, rstar
            if rstar > 0:
                self._rsl[r] = rstar
            else:
                self._rsl[r] = r # Occurs when too few seen objects
        
        #print self._rsl
        #return rsl
    
    #def _gt_nr_smooth(self, rl, nrl):
    def _gt_nr_smooth(self):
        '''
        Smooth Nr-parameter for Good-Turing smoothing
        @param rl: Integer-list of frequencies (r)
        @param nrl: List of integer-frequencies of frequencies (Nr), non-zero
        @return: a, b, X for a linear regression of log(Nr) = a + b*log(r)
        and X is the first r-value to start using smoothed nr's
        '''
        
        self._a = None
        self._b = None
        self._X = None
        
        CONFID_FACTOR = 1.96 # Adapted from http://www.grsampson.net/D_SGT.c
        #CONFID_FACTOR = 1.65
        if len(self._rl) < 2:
            # There are too few (r,Nr)-pairs to smooth Nr
            #return None, None, None
            return
        logzr = []
        for i in range(len(self._rl)):
            nr = self._nrl[i]
            l = self._rl[i-1] if i > 0 else 0
            k = self._rl[i+1] if i != len(self._rl)-1 else 2*self._rl[i]-l
            #if i > 0 and i < len(rl)-1:
            #zr = (2*nr)/float(rl[i+1]-rl[i-1])
            zr = (2*nr)/float(k-l)
            #print 'l', nr, k, l, zr
            #print zr
            logzr.append(math.log(zr))
        logr = [math.log(x) for x in self._rl]
        #print 'g', logr, logzr
        self._a, self._b = util.slr(logr, logzr)
        
        # Find point (r) where to start using smoothed Nr's. This is
        # the place where the Nr's are no longer significantly different
        # from the smoothed Nr's
        self._X = len(self._rl)
        for i in range(len(self._rl)-1):
            
            r = self._rl[i]
            nr = float(self._nrl[i])
            nr1 = float(self._nrl[i+1])
            if nr == 0:
                self._X = r
                break 
            snr = math.exp(self._a + (self._b*math.log(r))) # smoothed Nr
            snr1 = math.exp(self._a + (self._b*math.log(r+1))) # smoothed Nr1
            stdv = math.sqrt((r+1)*(r+1)*(nr1/(nr*nr))*(1+(nr1/nr)))
            urs = (r+1)*nr1 / float(nr) # Unsmoothed r*
            srs = (r+1)*snr1 / float(snr) # Smoothed r*
            #print r, stdv, nr, snr, srs, urs
            
            # OLD: If the difference between Nr and smoothed Nr has dropped
            # below CONFID_FACTOR * standard deviation, the Nr is no longer
            # significantly different and we will use smoothed Nr from here
            
            # If the difference between r* and smoothed r* has dropped
            # below CONFID_FACTOR * standard deviation, the r* is no longer
            # significantly different and we will use smoothed r* from here
            #if math.fabs(nr-snr) <= CONFID_FACTOR * stdv:
            if math.fabs(urs-srs) <= CONFID_FACTOR * stdv:
                self._X = r
                #print 'X',X
                break
        
        #return a, b, X
        
    def _renormalize(self):
        prob_cov = 0.0
        for r, nr in zip(self._rl, self._nrl):
            prob_cov  += nr * self._prob_unrenorm(r)
        if prob_cov:
            self._renorm = (1 - self._prob_unrenorm(0)) / prob_cov
    
    def _prob_unrenorm(self, r):
        if r > 0: # GT smoothing for seen objects
            rstar = self._rsl[r] # Good-Turing estimate
            
            # Turing estimate for low r
            if r < self._X:
                nr = 0
                nrp1 = 0
                for i, s in enumerate(self._rl):
                    if s == r:
                        nr = self._nrl[i]
                        break
                for i, s in enumerate(self._rl):
                    if s == r+1:
                        nrp1 = self._nrl[i]
                        break
                rstar = (r+1) * (nrp1/float(nr))
                
            return rstar/float(self._N)
        
        else: # Unseen object
            return self._p0_all
    
    def prob(self, r):
        if r > 0:
            return self._prob_unrenorm(r) * self._renorm
        else:
            return self._p0

# TEST
#rl = [1,2,3,4,5,6,7,400,1918]
#nrl = [268,112,70,41,24,14,15,1,1]
#print gt_nr_smooth(rl, nrl)