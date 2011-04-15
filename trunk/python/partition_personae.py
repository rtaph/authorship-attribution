import os
from nltk.corpus import PlaintextCorpusReader

#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/personae/data"
#output_folder = "/Users/epb/Documents/uni/kandidat/speciale/data/personae/data_50"

corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/fed_papers/all_known"
output_folder = "/Users/epb/Documents/uni/kandidat/speciale/data/fed_papers/F2"

FRAGMENTS = 100

corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding="utf-8")
n_texts = len(corpus.fileids())

for text in corpus.fileids():
    
    # This corpus is tokenized, so wrd_tokens will include
    # punctuation tokens 
    wrd_tokens = corpus.words(text)
    
    name = text.rpartition(".txt")[0]
    
    i = 0
    n_words = len(wrd_tokens)
    print n_words
    while n_words - i > FRAGMENTS*2:
        
        file_name = name + "_" + str(i) + ".txt"
        f = open(os.path.join(output_folder, file_name), "w")
        content = " ".join(wrd_tokens[i:i+FRAGMENTS])
        f.write(content.encode("utf-8"))
        f.flush()
        i = i + FRAGMENTS
    
    # Last file has more than FRAGMENTS words
    file_name = name + "_" + str(i) + ".txt"
    f = open(os.path.join(output_folder, file_name), "w")
    content = " ".join(wrd_tokens[i:])
    f.write(content.encode("utf-8"))
    f.flush()