import nltk
import os
from math import sqrt
from nltk.corpus import PlaintextCorpusReader

#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/PersonaeCorpus_onlineVersion/data_formatted"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/fed_papers/all_single"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/dark_web_forum_portal/ansar1/all"
corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/a1_100_10"

corpus = PlaintextCorpusReader(corpus_root, '.*txt')
n_texts = len(corpus.fileids())

txt_lengths = []
text_classes = []

DISTINCT_AUTHORS = True
TEXT_STATS = True

# TODO: Add possiblity to not count urlLink etc.

for text in corpus.fileids():
    
    #if not text.endswith(".txt"):
    #    continue
    print text
    
    if DISTINCT_AUTHORS:
        found_category = text.partition(".")[0]
        text_classes.append(found_category)
        
        
    if TEXT_STATS:
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
            
        if len(txt_lengths) % 100 == 0:
            print len(txt_lengths)

if DISTINCT_AUTHORS:
    print "No. of distinct authors:", len(list(set(text_classes)))
if TEXT_STATS:
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



