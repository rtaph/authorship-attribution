import nltk
import os
from nltk.corpus import PlaintextCorpusReader

corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/PersonaeCorpus_onlineVersion/data"

output_folder = "/Users/epb/Documents/uni/kandidat/speciale/data/PersonaeCorpus_onlineVersion/data_formatted"

FRAGMENTS = 100

corpus = PlaintextCorpusReader(corpus_root, '.*')
n_texts = len(corpus.fileids())

for text in corpus.fileids():
    
    
    wrd_tokens = corpus.words(text)
    #lower_wrds = [w.lower() for w in wrd_tokens if w.isalnum()]
    
    #bla = len(wrd_tokens) / 100
    #print bl
    #print len(wrd_tokens) / float(bla)
    
    name = text.rpartition(".txt")[0]
    author_id = text.partition(".")[0]
    
    i = 0
    n_words = len(wrd_tokens)
    print n_words
    while n_words - i > FRAGMENTS*2:
        
        #print i
        file_name = name + "_" + str(i) + "_" + author_id + ".txt"
        f = open(os.path.join(output_folder, file_name), "w")
        open
        f.write(" ".join(wrd_tokens[i:i+FRAGMENTS]))
        f.flush()
        i = i + FRAGMENTS
    
    # Last file has more than FRAGMENTS words
    file_name = name + "_" + str(i) + "_" + author_id + ".txt"
    f = open(os.path.join(output_folder, file_name), "w")
    f.write(" ".join(wrd_tokens[i:]))
    f.flush()
    #print i