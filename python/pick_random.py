import random
import os
import shutil
from nltk.corpus import PlaintextCorpusReader

corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/dw/almedad/all_known"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/dw/ansar1/all"
output_dir = "/Users/epb/Documents/uni/kandidat/speciale/data/dw/almedad/al3"
#output_dir = "/Users/epb/Documents/uni/kandidat/speciale/data/dw/ansar1/an9"

N_TEXTS = 3000

B = 50

corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding="UTF-8")
n = len(corpus.fileids())

#start = random.randint(0,n)
#print 'start', start
count = 0
#next = start
picked = []

b = 0
next = random.randint(0,n-B)

while count < N_TEXTS:
    
    b = 0
    
    while b < B:
        
        if picked.count(next+b) > 0 or count >= N_TEXTS:
            break
        
        print next+b
        f = corpus.fileids()[next+b]
        print f
        p = os.path.join(corpus_root, f)
        content = open(p,"r").read()
        to = os.path.join(output_dir, f)
        shutil.copy(p, to)
        print 'Copied'
        count = count + 1
        picked.append(next+b)
        b = b + 1
        
    next = random.randint(0,n-B) 
#    
#    if picked.count(next) == 0:
#        f = corpus.fileids()[next]
#        print f
#        
#        p = os.path.join(corpus_root, f)
#        content = open(p,"r").read()
#        to = os.path.join(output_dir, f)
#        shutil.copy(p, to)
#        print 'Copied'
#        count = count + 1
#    else:
#        next = random.randint(0,n)
#        
#    if  
           
    #next = (next + 1) % n
    #print 'next', next