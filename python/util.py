import math

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


#TODO: Returns something weird!

def k_fold_cv_ind(classes, K):
    '''
    K-fold CV indices
    '''
    
    distinct = list(set(classes))
    next = {}
    for c in distinct:
        next[c] = 0
        
    ind = []
    for i in range(len(classes)):
        c = classes[i]
        ind.append(next[c])
        next[c] = (next[c] + 1) % K  
    return ind 
    
    #for k in xrange(K):
    #    training = [x for i, x in enumerate(X) if i % K != k]
    #    validation = [x for i, x in enumerate(X) if i % K == k]
    #    yield training, validation
    
    
    
    
    
    
    
    
    
#print k_fold_cv_ind([1,1,1,1,2,2,1,1,3,3,3,3,3,2,2,2,2,2,1,1,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3], 3)

#for x in k_fold_cv([[1,2,3,4,5,6,7],[8,9,5,6,7,8,9],[0,0,0,0,10,10,10]],2):
#    print x