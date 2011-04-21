from nltk import FreqDist
from nltk.util import ngrams
import itertools

def calcbigns(ngram,ngs):
    '''
    Calculate N_1, N_2 and N_3+ for Kneser-Ney smoothing.
    '''
    
    # Find chars/words that occur after the n-1 first chars/words in
    # the given ngram
    c = []
    for ng in ngs:
        #print 'Compare', ng,  ng[:-1], ngram[:-1] 
        if ng[:-1] == ngram[:-1]:
            for _ in itertools.repeat(None, ngs[ng]):
                c.append(ng[-1])
    #print 'c-list', c
            
    # Count how many words/chars occur 1, 2 and 3+ times
    N1 = N2 = N3 = 0
    d = set(c)
    for x in d:
        co = c.count(x)
        if co == 1:
            N1 = N1 + 1
        if co == 2:
            N2 = N2 + 1
        if co > 2:
            N3 = N3 + 1
            
    return N1, N2, N3

def calc_discount(ngram, c, ngs):
    '''
    Calculate discount for Kneser-Ney
    '''
    
    # n1, n2, n3, n4
    n1 = ngs.Nr(1)
    n2 = ngs.Nr(2)
    n3 = ngs.Nr(3)
    n4 = ngs.Nr(4)
    #print 'n1-n4:', n1, n2, n3, n4
    
    # D1, D2 and D3+
    d1 = d2 = d3 = y = 0
    if n1 > 0:
        y = n1 / float(n1+(2*n2))
        d1 = 1 - (2*y*(n2/float(n1)))
    if n2 > 0:
        d2 = 2 - (3*y*(n3/float(n2))) 
    if n3 > 0:
        d3 = 3 - (4*y*(n4/float(n3)))
    #print 'd1-d3:', d1, d2, d3
    #print 'y', y
    
    # Determine discount
    d = 0
    if c == 1:
        d = d1
    elif c == 2:
        d = d2
    elif c > 2:
        d = d3
    
    return d, d1, d2, d3

def continuation_prob(ngram, ng_fds):
    '''
    Used to end recursion in modified KN.
    @param ng_fds: Freq.dists for each order of n-grams. Expected that
    n < len(ng_fds)-1 
    '''
    
    order = len(ngram)
    myorder_ngs = ng_fds[order-1]
    highorder_ngs = ng_fds[order]
    
    # Numerator: Number of distinct words/chars that precedes the latter
    # part (or the entire ngram if n=1) of the given ngram.
    
    # Denominator: The sum of number of distinct words/chars that precedes the
    # middle part of ngram, using different ends of the ngram. If given an
    # unigram, this equals the count of all distinct bigrams.
    
    if order == 1: # unigram
        num = 0
        #print 'n', ngram
        for hng in highorder_ngs:
            #print 'n+1', hng
            if hng[1:] == ngram:
                num = num + 1
        denom = len(highorder_ngs)
    else:
        num = 0
        for ng in myorder_ngs:
            if ng[1:] == ngram[1:]:
                num = num + 1
        denom = 0
        for ng in myorder_ngs:
            if ng[1:-1] == ngram[1:-1]:
                denom = denom + 1
    
    # TODO: Does denom == 0 ever occur?
    return num / float(denom)


def modkn(ngram, ngram_freqdists, recursion_stop=1):
    '''
    Modified Kneser-Ney.
    Calculate probability for an ngram
    @param ngram: The n-gram to calculate probability for.
    @param ngram_freqdists: List of frequency distributions for 1-grams,
    2-grams, ..., n-grams for a text.
    '''
    
    order = len(ngram) # order of given n-gram
    ngs = ngram_freqdists[order-1] # freq. dist for the ngrams of same order
        
    # To end recursion, we use N_1+(x w_i) / N_1+(x x) 
    if order == recursion_stop:
        myp = continuation_prob(ngram, ngram_freqdists)
        return myp
    
    else:    
        
        # count of n-gram
        c = ngs[ngram]
        
        # Count of history
        lowerorder_ngs = ngram_freqdists[order-2] 
        c_hist = lowerorder_ngs[ngram[:-1]]
        
        if c_hist > 0:
            
            # Discount, d
            d, d1, d2, d3 = calc_discount(ngram, c, ngs)
            
            # N_1, N_2, N_3+
            N1, N2, N3 = calcbigns(ngram, ngs)
            
            # Gamma
            gamma = ((d1*N1)+(d2*N2)+(d3*N3))/float(c_hist)
            
            # Probability of this ngram
            myp = ((c-d)/float(c_hist))
            
            # Return interpolated probability
            return myp + (gamma*modkn(ngram[1:],ngram_freqdists,recursion_stop))
        
        else:
            # Mod. KN does not state with what factor we should interpolate
            # the prob. of n-1-order ngrams if the count of this n-1-gram is 0,
            # so we just return 0 
            return 0
        
    
if __name__ == '__main__':
    #print modkn(('a','b','c'))
    
    text = "hej med dig hej hej den er god med dig hvordan g haar det heerre eheerhe"
    #ng = ('j', ' ', 'm')
    
    ng_freqdists = []
    for i in range(1,5):
        nglist = ngrams(text,i)
        ng_fd = FreqDist(nglist)
        print len(ng_fd), ng_fd
        ng_freqdists.append(ng_fd)
    
    #bla = 0
    for ng in ngrams(text,4):
        ng = ('g',' ','h','e')
        print 'Input', ng
        pkn = modkn(ng, ng_freqdists,3)
        print 'pKN:', pkn
        c_hist = ng_freqdists[2][ng[:-1]]
        print 's', c_hist
        #print 'p:  ', ng_freqdists[2].freq(ng)
        print 'p:  ', ng_freqdists[3][ng] / float(c_hist)
        #bla = bla + ng_freqdists[2].freq(ng)
        print '------------------------\n\n\n'
        exit()
    
    #print 'bla', bla
    #ng = ('a','b','c')
    #ngs = [('a','b','c'),('a','b','c'),('a','b','d'),('a','b','c'),('f','b','d'),('b','b','c'),('a','b','d')]
    #wc = 1
    #lower = False
    #print calcbign(ng, ngs, wc, lower)