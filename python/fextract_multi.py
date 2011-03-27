import multiprocessing
from multiprocessing import Pool
import time
import sys
from nltk.corpus import PlaintextCorpusReader
import fextract_helper

wrd_ngrams = False
wrd_ngram_size = 3
n_wrd_ngrams = 10

char_ngrams = False
char_ngram_size = 3
n_char_ngrams = 10

function_words = False

FEATURE_FILE = "/Users/epb/Documents/uni/kandidat/speciale/code/out.txt"
CATEGORY_FILE = "/Users/epb/Documents/uni/kandidat/speciale/code/cat.txt"
FUNC_FOLDER = "/Users/epb/Documents/uni/kandidat/speciale/data/func_words_eng_zlch06"

corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/a1_050_10"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/test/a1"

corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding='UTF-8')

def cng_stats_worker(texts):
    # Depends on some variables to be global
    return fextract_helper.char_ngram_stats(texts, corpus, \
                                            n_char_ngrams, char_ngram_size)

def cng_create_worker(text_char_ngrams):
    # Depends on some variables to be global
    return fextract_helper.create_char_ngrams(n_char_ngrams, all_char_ngrams, text_char_ngrams)
    
def wng_stats_worker(texts):
    # Depends on some variables to be global
    return fextract_helper.wrd_ngram_stats(texts, corpus, \
                                           n_wrd_ngrams, wrd_ngram_size)

def wng_create_worker(text_wrd_ngrams):
    # Depends on some variables to be global
    return fextract_helper.create_wrd_ngrams(n_wrd_ngrams, all_wrd_ngrams, text_wrd_ngrams)
    
def fw_stats_worker(texts):
    # Depends on some variables to be global
    return fextract_helper.extract_fws(texts, corpus, FUNC_FOLDER)

def fw_create_worker(text_fws):
    # Depends on some variables to be global
    return fextract_helper.create_fw_features(func_wrds, text_fws)
    
def splitup_tasks(all_tasks, workers, tasks_per_worker):
    text_tasks = []
    # Calculate portion sizes
    missing = len(all_tasks) % workers
    portion_sizes = []
    for i in range(workers):
        w = tasks_per_worker + 1 if missing else tasks_per_worker
        portion_sizes.append(w)
        missing = missing - 1 if missing else 0
    #print portion_sizes
    
    # Split-up tasks in portions
    #print missing
    #if missing > 0:
    #    tasks_per_worker = tasks_per_worker + 1
    #m = 0
    start = 0
    end = 0
    #end = tasks_per_worker
    #for i in range(workers):
    for w in portion_sizes:
        end = start + w
        #print 'Start', start
        #print 'End', end
        t = all_tasks[start:end]
        text_tasks.append(t)
        #m = m + 1
        start = end
        #if m >= missing:
        #    end = end + tasks_per_worker - 1
        #else:
        #    end = end + tasks_per_worker
    return text_tasks

if __name__ == '__main__':
    
    # Get options from command line
    a = 0
    while a < len(sys.argv):
        arg = sys.argv[a]
        i = 1
        
        # Character n-grams, with n-gram size and no. of n-grams
        if arg == "-c":
            char_ngrams = True
            if a+1 < len(sys.argv) and not sys.argv[a+1].startswith("-"):
                char_ngram_size = int(sys.argv[a+1])
                i = i + 1
                if a+2 < len(sys.argv) and not sys.argv[a+2].startswith("-"):
                    n_char_ngrams = int(sys.argv[a+2])
                    i = i + 1
            print "Using the", n_char_ngrams, "most frequent char n-grams of size", char_ngram_size
            #st_file.write("Using the " + str(n_char_ngrams) + " most frequent char n-grams of size " + str(char_ngram_size) + "\n")
            
        # Function words
        elif arg == "-f":
            function_words = True
            print "Using function words"
            #st_file.write("Using function words\n")
            
        # Word n-grams
        elif arg == "-w":
            wrd_ngrams = True
            if a+1 < len(sys.argv) and not sys.argv[a+1].startswith("-"):
                wrd_ngram_size = int(sys.argv[a+1])
                i = i + 1
                if a+2 < len(sys.argv) and not sys.argv[a+2].startswith("-"):
                    n_wrd_ngrams = int(sys.argv[a+2])
                    i = i + 1
            print "Using the", n_wrd_ngrams, "most frequent word n-grams of size", wrd_ngram_size 
            #st_file.write("Using the " + str(n_wrd_ngrams) +  " most frequent word n-grams of size " + str(wrd_ngram_size) + "\n")
            
        # Corpus
        elif arg == "-r":
            if a+1 < len(sys.argv) and not sys.argv[a+1].startswith("-"):
                corpus_root = sys.argv[a+1]
                i = i + 1
                            
        a = a + i
        
    # Load corpus
    #corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding='UTF-8')
    
    starttime = time.time()
    #print 'Start', starttime
    
    cpus = multiprocessing.cpu_count()
    #cpus = 1
    #texts = ['a.txt','b.txt','c.txt','d.txt', \
    #         'e.txt','f.txt','g.txt','h.txt','i.txt','j.txt']#'k','l','m','n','o','p','q','r','s','t','u']
    texts = corpus.fileids()
    print 'CPUs:', cpus
    n_texts = len(texts)
    print 'Texts:', n_texts
    tasks_per_worker = n_texts / cpus
    
    print 'Tasks per worker:', tasks_per_worker
    text_tasks = splitup_tasks(texts, cpus, tasks_per_worker)
    
    text_classes= fextract_helper.find_classes(texts)
    #print text_classes
    
    if char_ngrams:
        # Find n-grams in texts
        global all_char_ngrams
        all_char_ngrams = []
        text_char_ngrams = []
        charngram_workers = Pool(cpus)
        #for bla in text_tasks:
        #    print 'Bla:', len(bla)
        results = charngram_workers.map(cng_stats_worker, text_tasks)
        for r in results:
            all_char_ngrams.extend(r[0])
            text_char_ngrams.extend(r[1])
        charngram_workers.terminate()
        #print 'List of n-grams:', len(text_char_ngrams)
        # Create features
        cng_tasks = splitup_tasks(text_char_ngrams, cpus, tasks_per_worker)
        #for bla in cng_tasks:
        #    print 'Bla:', len(bla)
        charngram_features = []
        charngram_workers = Pool(cpus)
        results = charngram_workers.map(cng_create_worker, cng_tasks)
        for r in results:
            #print 'Result:', len(r)
            charngram_features.extend(r)
        charngram_workers.terminate()
        print 'Char ngram features:', len(charngram_features)
    
    if wrd_ngrams:
        # Find n-grams in texts
        global all_wrd_ngrams
        all_wrd_ngrams = []
        text_wrd_ngrams = []
        wrdngram_workers = Pool(cpus)
        results = wrdngram_workers.map(wng_stats_worker, text_tasks)
        for r in results:
            all_wrd_ngrams.extend(r[0])
            text_wrd_ngrams.extend(r[1])
        wrdngram_workers.terminate()
        # Create features
        wng_tasks = splitup_tasks(text_wrd_ngrams, cpus, tasks_per_worker)
        wrdngram_features = []
        wrdngram_workers = Pool(cpus)
        results = wrdngram_workers.map(wng_create_worker, wng_tasks)
        for r in results:
            wrdngram_features.extend(r)
        wrdngram_workers.terminate()
        print 'Wrd ngram features:', len(wrdngram_features)
    
    if function_words:
        # Find function words in texts
        global func_wrds
        text_fws = []
        fw_workers = Pool(cpus)
        results = fw_workers.map(fw_stats_worker, text_tasks)
        func_wrds = results[0][0]
        for r in results:
            text_fws.extend(r[1])
        fw_workers.terminate()
        # Create features
        fw_tasks = splitup_tasks(text_fws, cpus, tasks_per_worker)
        fw_features = []
        fw_workers = Pool(cpus)
        results = fw_workers.map(fw_create_worker, fw_tasks)
        for r in results:
            fw_features.extend(r)
        fw_workers.terminate()

    # Create feature matrix with all features
    feature_matrix = [[] for i in range(n_texts)]
    print 'Features:', len(feature_matrix)
    for f in range(len(feature_matrix)):
        if char_ngrams:
            feature_matrix[f].extend(charngram_features[f])
        if wrd_ngrams:
            feature_matrix[f].extend(wrdngram_features[f])
        if function_words:
            feature_matrix[f].extend(fw_features[f])
        
    #print 'Classes', text_classes
    #print 'Features:'
    #print feature_matrix
    
    # Save features to files
    fextract_helper.save_features(FEATURE_FILE, feature_matrix, CATEGORY_FILE, text_classes)
    
    # Stop timer and display results
    endtime = time.time()
    #print 'End', endtime
    n_texts = len(corpus.fileids())
    n_features = len(feature_matrix[0])
    print "Total time elapsed analysing {0} texts: {1} sec. No. of features: {2}".format(n_texts,endtime-starttime,n_features)