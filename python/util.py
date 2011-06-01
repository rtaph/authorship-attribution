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
    
    ind = [0 for i in range(len(classes))]
    x = 0
    for s in sorted_bla:
        k = s[1]
        ind[k] = x
        x = (x + 1) % K
        
    return ind