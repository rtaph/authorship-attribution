from nltk import FreqDist
from nltk.util import ngrams
import itertools

def calcbigns(ngram,ngs):
    '''
    Calculate N1, N2 and N3+ for Kneser-Ney smoothing.
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
    #print 'd', d
    
    return d, d1, d2, d3

def modkn(ngram, ngram_freqdists):
    '''
    Modified Kneser-Ney.
    Calculate probability for an ngram
    @param ngram: The n-gram to calculate probability for.
    @param ngram_freqdists: List of frequency distributions for 1-grams,
    2-grams, ..., n-grams for a text.
    '''
    
    print 'ngram', ngram
    order = len(ngram) # order of given n-gram
    ngs = ngram_freqdists[order-1] # freq. dist for the ngrams of same order
    #print 'ngs', ngs
        
    if order == 1:
        
        myp = ngs.freq(ngram) # MLE for 1-grams
        print 'myp', myp
        return myp
    
    else:    
        
        # c
        c = ngs[ngram]
        #print 'c', c
        
        # Count of history
        lowerorder_ngs = ngram_freqdists[order-2]
        csum = lowerorder_ngs[ngram[:-1]]
        #print 'csum', csum
        
        # Discount, d
        d, d1, d2, d3 = calc_discount(ngram, c, ngs)
        #print 'd', d, 'd1', d1, 'd2', d2, 'd3', d3
        
        # N1, N2, N3
        #print ngs.samples()
        N1, N2, N3 = calcbigns(ngram, ngs)
        #print 'N1', N1, 'N2', N2, 'N3', N3
        
        # Gamma
        gamma = ((d1*N1)+(d2*N2)+(d3*N3))/float(csum)
        #print 'gamma', gamma
        
        # Interpolated probability
        myp = ((c-d)/float(csum))
        print 'myp', myp
        return myp + (gamma*modkn(ngram[1:],ngram_freqdists))
        
    
if __name__ == '__main__':
    #print modkn(('a','b','c'))
    
    text = "hej med dig hej hej den er god med dig hvordan gaar det"
    #ng = ('j', ' ', 'm')
    
    ng_freqdists = []
    for i in range(1,4):
        nglist = ngrams(text,i)
        ng_fd = FreqDist(nglist)
        print ng_fd
        ng_freqdists.append(ng_fd)
    
    #bla = 0
    for ng in ngrams(text,3):
        pkn = modkn(ng, ng_freqdists)
        print 'pKN:', pkn
        csum = ng_freqdists[1][ng[:-1]]
        #print 'p:  ', ng_freqdists[2].freq(ng)
        print 'p:  ', ng_freqdists[2][ng] / float(csum)
        #bla = bla + ng_freqdists[2].freq(ng)
        print '------------------------\n\n\n'
    
    #print 'bla', bla
    #ng = ('a','b','c')
    #ngs = [('a','b','c'),('a','b','c'),('a','b','d'),('a','b','c'),('f','b','d'),('b','b','c'),('a','b','d')]
    #wc = 1
    #lower = False
    #print calcbign(ng, ngs, wc, lower)