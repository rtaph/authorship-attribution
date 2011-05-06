from spellcorrect import SpellCorrector
import time
from nltk.corpus import PlaintextCorpusReader

traintexts = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/data_formatted1"

testtexts = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/a1_010_10"

sc_file = "/Users/epb/Documents/uni/kandidat/speciale/code/spellcorrector.csv"

corpus = PlaintextCorpusReader(traintexts, '.*txt', encoding='UTF-8')

def train(alphabet):
    
    all_words = []
    
    train_start = time.time()
    i = 0
    for text in corpus.fileids():
        
        i = i + 1
        if i % 500 == 0:
            print i
        wrd_tokens = corpus.words(text)
        empty = len(corpus.raw(text)) == 0
    
        if not empty:
            lower_wrds = [w.lower() for w in wrd_tokens if w.isalnum()]
            
            #if i % 500 == 0:
                #print lower_wrds[:10]
            all_words.extend(lower_wrds)
    
    sc = SpellCorrector(alphabet)
    sc.train(all_words)
    train_end = time.time()
    print 'Training done ({0} s)'.format(train_end-train_start)
    #print len(NWORDS)
    #print NWORDS.items()[:20]
    return sc

def test(sc):
    test_corpus = PlaintextCorpusReader(testtexts, '.*txt', encoding='UTF-8')
    c = 0
    d = 0
    i = 0
    for text in test_corpus.fileids():
        
        i = i + 1
        if i % 100 == 0:
            print i
            
        wrd_tokens = test_corpus.words(text)
        empty = len(test_corpus.raw(text)) == 0
    
        if not empty:
            lower_wrds = [w.lower() for w in wrd_tokens if w.isalnum()]
            
            for wrd in lower_wrds:
                d = d + 1
                correct_wrd = sc.correct(wrd)
                if wrd != correct_wrd:
                    try:
                        print wrd, '->', correct_wrd
                    except UnicodeEncodeError:
                        pass
                    c = c + 1
    
    print 'Corrections for {0} texts with {1} words: {2}'.format(len(test_corpus.fileids()),d,c)

if __name__ == '__main__':
    
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    
    sc = train(alphabet)
    #sc.save_to_file(sc_file)
    
    #sc = SpellCorrector(alphabet)
    #sc.load_from_file(sc_file)
    test(sc)
    
