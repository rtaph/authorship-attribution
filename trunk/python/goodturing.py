import math
import util

def gt_r_est(rl, nrl, a, b, X):
    '''
    Good-Turing smoothing: Find r* estimates for all r>=1
    @param rl: Integer-list of frequencies, r where r >= 1
    @param nrl: List of integer-frequencies of frequencies (Nr)
    @param a, b: Parameters of linear regression log(Nr) = a + b*log(r) that
    estimate Nr
    @param X: The first value of r to start using smoothed Nr's
    @return: Dictionary with key=r, value=r*
    '''
    
    rsl = {} # dict of r,r*
    
    for i in range(len(rl)):
        
        r = rl[i]
        nr = nrl[i] # Nr
        nr1 = 0 # The next Nr
        if i < len(rl)-1:
            nr1 = nrl[i+1]
        
        if a is not None and b is not None and b <= -1: 
            if nr == 0 or r >= X: # Good-Turing estimate for high r
                nr = math.pow(10, a + (b*math.log10(r)))
            if r+1 >= X:
                nr1 = math.pow(10, a + (b*math.log10(r+1)))
    
        # TODO: Is this right for r in short list of r's?
        rstar = (r+1) * (nr1/float(nr)) # calculate r*
        if rstar > 0:
            rsl[r] = rstar
        else:
            rsl[r] = r # Occurs when too few seen objects
    
    #print rsl
    return rsl

def gt_nr_smooth(rl, nrl):
    '''
    Smooth Nr-parameter for Good-Turing smoothing
    @param rl: Integer-list of frequencies (r)
    @param nrl: List of integer-frequencies of frequencies (Nr), non-zero
    @return: a, b, X for a linear regression of log(Nr) = a + b*log(r)
    and X is the first r-value to start using smoothed nr's
    '''
    #CONFID_FACTOR = 1.96 # Adapted from http://www.grsampson.net/D_SGT.c
    CONFID_FACTOR = 1.65
    if len(rl) < 4:
        # There are too few (r,Nr)-pairs to smooth Nr
        return None, None, None
    logzr = []
    for i in range(len(rl)):
        nr = nrl[i]
        if i > 0 and i < len(rl)-1:
            zr = (2*nr)/float(rl[i+1]-rl[i-1])
            #print zr
            logzr.append(math.log10(zr))
    logr = [math.log10(x) for x in rl[1:len(rl)-1]]
    a, b = util.slr(logr, logzr)
    
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

# TEST
#rl = [1,2,3,4,5,6,7,400,1918]
#nrl = [268,112,70,41,24,14,15,1,1]
#print gt_nr_smooth(rl, nrl)