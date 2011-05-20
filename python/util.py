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
        
    return ind

#def avgwith_none(l):
#    suml = 0
#    avgl = None
#    totl = 0 
#    for x in l:
#        if x != None:
#            suml = suml + x
#            totl = totl + 1
#    if totl > 0:
#        avgl = suml / float(totl)
#    return avgl
  
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
    
    
    
    
#print k_fold_cv_ind(['A','A','A','A','B','B','A','A','C','C','C','C','C','B','B','B','B','B','A','A','B','B','B','B','C','C','C','C','C','C','C','C','C','C','C'], 3)

#for x in k_fold_cv([[1,2,3,4,5,6,7],[8,9,5,6,7,8,9],[0,0,0,0,10,10,10]],2):
#    print x