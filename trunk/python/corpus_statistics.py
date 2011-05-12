'''
Statistics about a given corpus
'''
from math import sqrt
from nltk.corpus import PlaintextCorpusReader

#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/personae/data_50"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/fed_papers/F3"
corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/dw/almedad/al3"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/dw/ansar1/an9"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/B2"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/test/test1_64"

corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding="UTF-8")
n_texts = len(corpus.fileids())

txt_lengths = []
text_classes = []

DISTINCT_AUTHORS = True
TEXT_STATS = True

for text in corpus.fileids():
    
    if DISTINCT_AUTHORS:
        found_category = text.partition(".")[0]
        text_classes.append(found_category)
        
        
    if TEXT_STATS:
        wrd_tokens = corpus.words(text)
        
        l = 0
        if len(corpus.raw(text)) > 0 and len(wrd_tokens) > 0:
            
            l = len(wrd_tokens)
            
            #lower_wrds = [w.lower() for w in wrd_tokens if w.isalnum()]
            
            #if len(lower_wrds) > 0:
            #    l = len(lower_wrds)
            #else:
            #    print text
            
        else:
            print text
        txt_lengths.append(l)
            
        if len(txt_lengths) % 100 == 0:
            print len(txt_lengths)

if DISTINCT_AUTHORS:
    print "No. of distinct authors:", len(list(set(text_classes)))
if TEXT_STATS:
    n_txt = len(txt_lengths)
    print "Texts:", n_txt
    if n_txt > 0:
        mean = sum(txt_lengths) / float(n_txt)
        std = 0
        for a in txt_lengths:
            std = std + (a - mean)**2
        std = sqrt(std / float(n_txt-1))
    
        print "Average length:", mean 
        print "Min:", min(txt_lengths)
        print "Max:", max(txt_lengths)
        print "Std. dev.:", std



