import math
import operator

def slr(x, y):
    '''
    Simple Linear Regression, y = a + bx
    @return: a, b
    '''
    avgx = float(sum(x)) / len(x)
    avgy = float(sum(y)) / len(y)
    n = d = 0
    for i in range(len(x)):
        n = n + ((x[i]-avgx)*(y[i]-avgy))
        d = d + math.pow(x[i]-avgx,2)
    b = n/d
    a = avgy - (b*avgx)
    return a, b


def k_fold_cv_ind(classes, K):
    '''
    K-fold CV indices
    '''
    
    bla = []
    for i in range(len(classes)):
        bla.append((classes[i],i))
    
    sorted_bla = sorted(bla,key=operator.itemgetter(0))
    #print sorted_bla
    
    ind = [0 for i in range(len(classes))]
    x = 0
    for s in sorted_bla:
        k = s[1]
        ind[k] = x
        x = (x + 1) % K
        
    #print ' ---', classes
    #print ' ---', ind
    return ind
#    
#    psize_min = len(classes) / K
#    psize_max = psize_min + (len(classes) % K)
#    print 'psize', psize_min, psize_max
#    prev_count = 0
    
#    bins = [{'indices': [], 'classcounts': []} for i in range(K)]
#    next_bin = 0
#    
#    psize_max = psize_min + (len(classes) % K)
#    i = 0
#    c = 0
#    while c < len(classes):
#        cl = classes[i]
#        if bins[next_bin]


#    sortedcl = sorted(classes)
#    print sortedcl
#    
#    distinct = list(set(classes))
#    cind = {}
#    for i in range(len(classes)):
#        c = classes[i]
#        if not cind.has_key(c):
#            cind[c] = 0
#        cind[c] = cind[c] + 1 
#    
#    for c in cind:
#        len(classes) / K
    
    
    
#    next = {}
#    for c in distinct:
#        next[c] = 0
#        
#    ind = []
##    c_ind = {}
#    for i in range(len(classes)):
#        c = classes[i]
##        if not c_ind.has_key(c):
##            c_ind[c] = []
##        c_ind[c].append(i)
#        ind.append(next[c])
#        next[c] = (next[c] + 1) % K
#    #print c_ind
#    #for c in c_ind:
#          
#    return ind 
    
    #for k in xrange(K):
    #    training = [x for i, x in enumerate(X) if i % K != k]
    #    validation = [x for i, x in enumerate(X) if i % K == k]
    #    yield training, validation
    
    
  
# TEST
#k = 4
#c = [1,1,1,2,2,2,1,1,1,1,4,2,2,1,1,2,3,2,2,2,2,4,3,3,3,3,3,1,1]
#ind = k_fold_cv_ind(c, k)
#
#for i in range(k):
#    s = 0
#    t = []
#    for u in range(len(ind)):
#        j = ind[u]
#        if i == j:
#            s = s + 1
#            t.append(c[u])
#    print t
#    print s
#    
    
    
    
    
#print k_fold_cv_ind([1,1,1,1,2,2,1,1,3,3,3,3,3,2,2,2,2,2,1,1,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3], 3)

#for x in k_fold_cv([[1,2,3,4,5,6,7],[8,9,5,6,7,8,9],[0,0,0,0,10,10,10]],2):
#    print x