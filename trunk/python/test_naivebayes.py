import naivebayes
import fextract_helper
import util
from nltk.probability import FreqDist
from nltk.corpus import PlaintextCorpusReader


n_char_ngrams = 200
char_ngram_size = 3 

corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/a1_005_10"

if __name__ == '__main__':
    
    corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding='UTF-8')
    texts = corpus.fileids()
    text_classes = fextract_helper.find_classes(texts)
    ntexts = len(texts)
    #classes = list(set(text_classes))
    
    all_ngrams, text_ngrams = fextract_helper.char_ngram_stats(texts, corpus, n_char_ngrams, char_ngram_size)
    
    # Determine features
    afreqs = FreqDist(all_ngrams)
    tot_cngs = min([n_char_ngrams, afreqs.B()])
    mostfreqngs = afreqs.keys()[:tot_cngs]
    
    # TODO: This could be smoothed...?
    # Calculate features for each text
    features = []
    for t in text_ngrams:
        myfeats = [] # features for the current text
        freqdist = FreqDist(t)
        for f in mostfreqngs:
            myfeats.append(freqdist.freq(f))
        features.append(myfeats)
        
    nbins = 10
    bins = naivebayes.build_feat_bins(features, nbins)
    print 'bins', bins
    
    #d = 3
    #feature_bins = int(math.pow(10, d))    
    
    # Cross-validation
    K = 3
    k_indices = util.k_fold_cv_ind(text_classes,K)
    
    for k in range(K):
        
        print '---------------   k=' + str(k) + '  ------------------'
        
        trainc = [text_classes[i] for i in range(len(text_classes)) if k_indices[i] != k]
        traint = [features[i] for i in range(len(features)) if k_indices[i] != k]
        testc = [text_classes[i] for i in range(len(text_classes)) if k_indices[i] == k]
        testt = [features[i] for i in range(len(features)) if k_indices[i] == k]
        
        print 'Train texts:', len(traint)
        print 'Test texts:', len(testt)
    
        cps, fcps = naivebayes.nb_train(trainc, traint, bins)
        classified = naivebayes.nb_classify(cps, fcps, testc, testt, bins)
        
        correct = 0
        for i in range(len(classified)):
            if classified[i] == testc[i]:
                correct = correct + 1
        print 'A:', correct / float(len(testc))
        