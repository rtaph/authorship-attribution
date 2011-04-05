'''
Copy a number of non-emtpy texts from one folder to another.
'''

import nltk
import os
from math import sqrt
from nltk.corpus import PlaintextCorpusReader
import random
import shutil

#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/data_formatted5"
corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/personae/data_20"
output = "/Users/epb/Documents/uni/kandidat/speciale/data/personae/set20_10_1"

NAUTHORS = 10
a = 0
authors = {}
NTEXTS = 10
#t = 0
#texts = []

files = os.listdir(corpus_root)
nfiles = len(files)

while a < NAUTHORS:
    x = random.randint(0,nfiles)
    #print "x:", x
    
    txt = files[x]
    p = os.path.join(corpus_root, txt)
    if os.path.isfile(p) and txt.endswith(".txt"):
        
        author = txt.partition(".")[0]
        #print "Found author:", author
        content = open(p,"r").read()
        
        #if authors.count(author) == 0:
        if not authors.has_key(author) and len(content) > 0:
            #print "Author is new"
            #authors.append(author)
            
            #print "First text:", txt
            my_texts = [txt]
            
            #texts.append(txt)
            #t = 1
            i = 1 # increment/decrement
            y = x + i
            
            while len(my_texts) < NTEXTS:
                #print "y:", y
                if y < nfiles: 
                    next_txt = files[y]
                    next_author = next_txt.partition(".")[0]
                    #print "Next author:", next_author
                    if author == next_author:
                        #print "Found new text by", author
                        p = os.path.join(corpus_root, next_txt)
                        #texts.append(next_txt)
                        content = open(p,"r").read()
                        if len(content) > 0:
                            my_texts.append(next_txt)
                            #t = t + 1
                    elif y < x:
                        break # no more texts by this author
                    else:
                        print "Start from x, backtracking"
                        y = x
                        i = -1
                elif y > 0:
                    print "Reached end of files, start from x, backtracking"
                    y = x
                    i = -1
                else:
                    break # no more texts to find by author
                y = y + i
                
            #print "Found", len(my_texts), "texts for", author
            if len(my_texts) == NTEXTS:
                authors[author] = my_texts
                #texts.extend(my_texts)
                a = a + 1
        
#print authors
o = 0
for a in authors.keys():
    print "Copying", len(authors[a]), "texts for", a
    for t in authors[a]:
        o = o + 1
        fr = os.path.join(corpus_root, t)
        to = os.path.join(output, t)
        #print fr, to
        shutil.copy(fr, to)
print o

