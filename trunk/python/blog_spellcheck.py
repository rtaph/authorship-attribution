from spellcorrect import SpellCorrector
import time
from nltk.corpus import PlaintextCorpusReader

data_base = "/Users/epb/Documents/uni/kandidat/speciale/data/"
#train_dirs = ["blog_corpus/data_formatted1", "blog_corpus/data_formatted2", "blog_corpus/data_formatted3", "blog_corpus/data_formatted4", "blog_corpus/data_formatted5"]
#train_dirs = ["blog_corpus/data_formatted7"]
train_dirs = ["dw/almedad/all_known"]
#testtexts = "blog_corpus/a1_010_10"
testtexts = "dw/almedad/a1_3_40"

sc_file = "/Users/epb/Documents/uni/kandidat/speciale/code/sc.txt"

def train(alphabet):
    
    train_start = time.time()
    sc = SpellCorrector(alphabet)
    #all_words = []
    z = 0
    t = 0
    
    for td in train_dirs:
        print 'Training on', td
        corpus = PlaintextCorpusReader(data_base+td, '.*txt', encoding='UTF-8')
        t = t + len(corpus.fileids())
        i = 0
        for text in corpus.fileids():
            
            i = i + 1
            if i % 500 == 0:
                print i
            wrd_tokens = corpus.words(text)
            empty = len(corpus.raw(text)) == 0
        
            if not empty:
                lower_wrds = [w.lower() for w in wrd_tokens if w.isalnum()]
                
                sc.train(lower_wrds)
                z = z + len(lower_wrds)
                #if i % 500 == 0:
                    #print lower_wrds[:10]
                #all_words.extend(lower_wrds)
    
    
    #sc.train(all_words)
    train_end = time.time()
    print 'Training done ({0} s) with {1} texts and {2} words'.format(train_end-train_start, t, z)
    #print len(NWORDS)
    #print NWORDS.items()[:20]
    return sc

def test(sc):
    test_corpus = PlaintextCorpusReader(data_base+testtexts, '.*txt', encoding='UTF-8')
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
    
    #sc = SpellCorrector(alphabet)
    #sc = train(alphabet)
    #sc.save_to_file(sc_file)
    
    sc = SpellCorrector(alphabet)
    sc.load_from_file(sc_file)
    test(sc)
    
