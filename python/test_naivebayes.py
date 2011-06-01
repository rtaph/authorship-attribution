import naivebayes
import fextract_helper
import util
from nltk.probability import FreqDist
from nltk.corpus import PlaintextCorpusReader
import csv
import time

NBINS = 10

CV_K = 10

top=10

PERFORMANCE_FILE = "/Users/epb/Documents/uni/kandidat/speciale/code/perf_nb.csv"

#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/b1"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/personae/p1"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/dw/ansar1/an2"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/dw/almedad/al2"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/fed_papers/F2"

output_dir = "/Users/epb/Documents/uni/kandidat/speciale/output/"
data_dir = "/Users/epb/Documents/uni/kandidat/speciale/data/"

feature_dir = "2000_3char_gt"
#corpus = "blogs"
#dataset = "b1"
#corpus = "personae"
#dataset = "p2"
#corpus = "almedad"
#dataset = "al2"
#corpus = "fed"
#dataset = "all_known"
corpus = "ansar1"
dataset = "an2"


if __name__ == '__main__':
    
    print 'Dataset:', dataset
    feature_file = output_dir + corpus + "/" + feature_dir + "/" + dataset + ".out.txt"
    print 'Features:', feature_file
    
    corpus_root = data_dir + corpus + "/" + dataset
    print 'Corpus:', corpus_root
    
    start = time.time()
    
    corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding='UTF-8')
    texts = corpus.fileids()
    text_classes = fextract_helper.find_classes(texts)
    ntexts = len(texts)
    distinct_classes = list(set(text_classes))
    
    print 'Loading features'
    features = fextract_helper.load_features(feature_file)
        
    # Find feature-value bins
    bins = naivebayes.build_feat_bins(features, NBINS)
    print 'bins', bins, len(bins)
    
    # Cross-validation
    print 'Doing cross-validation...'
    k_indices = util.k_fold_cv_ind(text_classes,CV_K)
    
    class_p = dict.fromkeys(distinct_classes)
    for c in class_p:
        class_p[c] = [None for i in range(CV_K)]
    class_r = dict.fromkeys(distinct_classes)
    for c in class_r:
        class_r[c] = [None for i in range(CV_K)]
    class_f1 = dict.fromkeys(distinct_classes)
    for c in class_f1:
        class_f1[c] = [None for i in range(CV_K)]
    
    # All performance measures
    perf = [[None for j in range(7)] for i in range(max(len(distinct_classes),CV_K))]
    
    for k in range(CV_K):
        
        print '---------------   k=' + str(k+1) + '  ------------------'
        
        trainc = [text_classes[i] for i in range(len(text_classes)) if k_indices[i] != k]
        traint = [features[i] for i in range(len(features)) if k_indices[i] != k]
        testc = [text_classes[i] for i in range(len(text_classes)) if k_indices[i] == k]
        testt = [features[i] for i in range(len(features)) if k_indices[i] == k]
        
        print 'Train texts:', len(traint)
        print 'Test texts:', len(testt)
        
        nb = naivebayes.NaiveBayes(bins)
        nb.train(trainc, traint)
        print 'Classifying..'
        classified = nb.classify(testt, top)
        
        # --- Calculate performance measures --- #
        class_classified = dict.fromkeys(distinct_classes,0)
        actual = dict.fromkeys(distinct_classes,0)
        correct = dict.fromkeys(distinct_classes,0)
        top_correct = 0
        for i in range(len(classified)):
            best_classes = [x[0] for x in classified[i]]
            
            if len(best_classes) > 0:
                cc = best_classes[0] # classified class 
                tc = testc[i] # test class
                class_classified[cc] = class_classified[cc] + 1
                actual[tc] = actual[tc] + 1
                
                if cc == tc:
                    correct[cc] = correct[cc] + 1
            
            # Accurracy for for test-classes being in top-X best classes
            if best_classes.count(tc) > 0:
                top_correct = top_correct + 1
        
        # Accuracy for this fold
        acc = sum(correct.values()) / float(len(testc))
        print 'A:', format(100*acc,'.2f')
        print 'A (top ' + str(top) + "): " + format(100*top_correct / float(len(testc)), '.2f')
        perf[k][0] = acc
        
        # Precision and recall for each class for this fold
        foldp = []
        foldr = []
        foldf1 = []
        for c in class_p:
            
            # Precision: Correct classified for c / total classified for c
            p = 1.0
            if class_classified[c] > 0:
                p = correct[c] / float(class_classified[c])
            class_p[c][k] = p
            foldp.append(p)
        
            # Recall: Correct classified for c / actual classes for c
            r = 1.0    
            if actual[c] > 0:
                r = correct[c] / float(actual[c])
            class_r[c][k] = r
            foldr.append(r)
            
            # F1: Harmonic mean of precision and recall
            f1 = 0.0
            rp_sum = p + r
            if rp_sum != 0:
                f1 = (2*p*r) / float(r+p)
            class_f1[c][k] = f1
            foldf1.append(f1)
            
        # Average precision, recall and f1 for fold
        #print foldp, foldr, foldf1
        avgfoldp = sum(foldp) / float(len(foldp))
        avgfoldr = sum(foldr) / float(len(foldr))
        avgfoldf1 = sum(foldf1) / float(len(foldf1))
        print 'Avg. P:', format(100*avgfoldp,'.2f')
        print 'Avg. R:', format(100*avgfoldr,'.2f')
        print 'Avg. F1:', format(100*avgfoldf1,'.2f')
        perf[k][1] = avgfoldp
        perf[k][2] = avgfoldr
        perf[k][3] = avgfoldf1
    
    # Average class precision, recall and f1 for each class
    for i in range(len(class_p)):
        c = class_p.keys()[i]
        avgcp = sum(class_p[c]) / float(len(class_p[c]))
        avgcr = sum(class_r[c]) / float(len(class_r[c]))
        perf[i][4] = avgcp
        perf[i][5] = avgcr
        avgcf1 = 0.0
        if avgcp != 0 and avgcr != 0:
            avgcf1 = (2*avgcp*avgcr) / float(avgcp+avgcr)
        perf[i][6] = avgcf1 
    
    # ----- Write performance measures to file ----- #
    pf = open(PERFORMANCE_FILE,'w')
    w = csv.writer(pf)
    for row in perf:
        w.writerow(row)
    pf.close()
    
    end = time.time()
    print "Time: {0}".format(end-start)
        
        