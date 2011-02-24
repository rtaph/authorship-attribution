import nltk
import os
from math import sqrt
from nltk.corpus import PlaintextCorpusReader

#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/PersonaeCorpus_onlineVersion/data"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/fed_papers/all"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/dark_web_forum_portal/ansar1/all"
corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/set3_10_4_first_eight"

corpus = PlaintextCorpusReader(corpus_root, '.*')
n_texts = len(corpus.fileids())

txt_lengths = []

# TODO: Add possiblity to not count urlLink etc.

for text in corpus.fileids():
    
    #print text
    wrd_tokens = corpus.words(text)
    
    if len(corpus.raw(text)) > 0 and len(wrd_tokens) > 0:
        lower_wrds = [w.lower() for w in wrd_tokens if w.isalnum()]
        
        if len(lower_wrds) > 0:
            txt_lengths.append(len(lower_wrds))
        #else:
        #    print text
    else:
        txt_lengths.append(0)

n_txt = len(txt_lengths)
mean = sum(txt_lengths) / float(n_txt)
std = 0
for a in txt_lengths:
    std = std + (a - mean)**2
std = sqrt(std / float(n_txt-1))
print "Texts:", n_txt
print "Average length:", mean 
print "Min:", min(txt_lengths)
print "Max:", max(txt_lengths)
print "Std. dev.:", std

