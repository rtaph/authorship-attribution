'''
Copy all text-files that has content from one folder to another.
'''
import nltk
import os
from math import sqrt
from nltk.corpus import PlaintextCorpusReader
import random
import shutil

#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/data_formatted5"
#output = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/a1_200_10"
corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/dark_web_forum_portal/ansar1/all"
output = "/Users/epb/Documents/uni/kandidat/speciale/data/dark_web_forum_portal/ansar1/all_nonempty"

files = os.listdir(corpus_root)
nfiles = len(files)

for f in files:
    
    p = os.path.join(corpus_root, f)
    if os.path.isfile(p) and f.endswith(".txt"):
        content = open(p,"r").read()
        if len(content) > 0:
            #fr = os.path.join(corpus_root, t)
            to = os.path.join(output, f)
            #print p, to
            print f
            shutil.copy(p, to)
            
            #if len(content) > 120000:
            #    print f
