import math

def slr(x, y):
    '''
    Simple Linear Regression, y = a + bx
    @return: a, b
    '''
    a = b = 0
    avgx = float(sum(x)) / len(x)
    avgy = float(sum(y)) / len(y)
    n = d = 0
    for i in range(len(x)):
        n = n + ((x[i]-avgx)*(y[i]-avgy))
        d = d + math.pow(x[i]-avgx,2)
    b = n/d
    a = avgy - (b*avgx)
    return a, b  