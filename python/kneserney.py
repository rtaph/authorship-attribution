
def calcbign(ngram, ngrams,ncount,lowerbound=False):
    
    # Find chars/words that occur after the n-1 first chars/words in
    # the given ngram
    c = []
    for ng in ngrams:
        if ng[:-1] == ngram[:-1]:
            c.append(ng[-1])
            
    # Count how many words occur ncount times
    d = set(c)
    dsum = 0
    for x in d:
        co = c.count(x)
        if (lowerbound and co >= ncount) or \
        (not lowerbound and co == ncount):
            dsum = dsum + 1
    return dsum

def modkn(ngram):
    '''
    Modified Kneser-Ney.
    Calculate probability for an ngram
    '''
    
    # TODO: c
    c = 10 
    
    # TODO: csum
    csum = 100
    
    # TODO: n1, n2 etc.
    n1 = 4
    n2 = 5
    n3 = 4
    n4 = 9
    
    # TODO: N1, N2, N3
    bign1 = 10
    bign2 = 10
    bign3 = 10
    
    # Determine discount (d)
    d = 0
    y = n1 / float(n1+(2*n2))
    d1 = 1 - (2*y*(n2/float(n1)))
    d2 = 2 - (3*y*(n3/float(n2)))
    d3 = 3 - (4*y*(n4/float(n3)))
    print y, d1, d2, d3
    if c == 1:
        d = d1
    elif c == 2:
        d = d2
    elif c > 2:
        d = d3
    print 'd', d
    
    # Gamma
    gamma = ((d1*bign1)+(d2*bign2)+(d3*bign3))/float(csum)
    
    # Interpolated probability
    if len(ngram) > 1:
        return ((c-d)/float(csum)) + (gamma*modkn(ngram[1:]))
    else:
        return 0 # TODO: 1-gram prob. 
        
    
if __name__ == '__main__':
    #print modkn(('a','b','c'))
    
    ng = ('a','b','c')
    ngs = [('a','b','c'),('a','b','c'),('a','b','d'),('a','b','c'),('f','b','d'),('b','b','c'),('a','b','d')]
    wc = 1
    lower = False
    print calcbign(ng, ngs, wc, lower)