from mpi import MPI
from nltk.corpus import PlaintextCorpusReader
import fextract_helper
import subprocess
import os
import sys
import time

wrd_ngrams = False
wrd_ngram_size = 3
n_wrd_ngrams = 10

char_ngrams = False
char_ngram_size = 3
n_char_ngrams = 10

function_words = False

#FEATURE_FILE = "/Users/epb/Documents/uni/kandidat/speciale/code/out.txt"
#CATEGORY_FILE = "/Users/epb/Documents/uni/kandidat/speciale/code/cat.txt"
FEATURE_FILE = "out.txt"
CATEGORY_FILE = "cat.txt"
FUNC_FOLDER = "/Users/epb/Documents/uni/kandidat/speciale/data/func_words_eng_zlch06"

#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/a1_005_10"
corpus_root = "nobackup/blogs/a1_005_10"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/test/a1"

def splitup_tasks(all_tasks, workers, tasks_per_worker):
    tasks = []
    # Calculate portion sizes
    missing = len(all_tasks) % workers
    portion_sizes = []
    for i in range(workers):
        w = tasks_per_worker + 1 if missing else tasks_per_worker
        portion_sizes.append(w)
        missing = missing - 1 if missing else 0
    
    # Split-up tasks in portions
    start = 0
    end = 0
    for w in portion_sizes:
        end = start + w
        t = all_tasks[start:end]
        tasks.append(t)
        start = end
    return tasks

# Init MPI system
mpi = MPI()
workers = mpi.MPI_COMM_WORLD
nworkers = workers.size()
rank = workers.rank() # The rank of the current process

# Read arguments from command line
a = 2
while a < len(sys.argv):
    arg = sys.argv[a]
    i = 1
        
    # Character n-grams, with n-gram size and no. of n-grams
    if arg == "-cng":
        char_ngrams = True
        if a+1 < len(sys.argv) and not sys.argv[a+1].startswith("-"):
            char_ngram_size = int(sys.argv[a+1])
            i = i + 1
            if a+2 < len(sys.argv) and not sys.argv[a+2].startswith("-"):
                n_char_ngrams = int(sys.argv[a+2])
                i = i + 1
        if rank == 0:
            print "Using the", n_char_ngrams, "most frequent char n-grams of size", char_ngram_size
            
    # Function words
    elif arg == "-fw":
        function_words = True
        if rank == 0:
            print "Using function words"
            
    # Word n-grams
    elif arg == "-wng":
        wrd_ngrams = True
        if a+1 < len(sys.argv) and not sys.argv[a+1].startswith("-"):
            wrd_ngram_size = int(sys.argv[a+1])
            i = i + 1
            if a+2 < len(sys.argv) and not sys.argv[a+2].startswith("-"):
                n_wrd_ngrams = int(sys.argv[a+2])
                i = i + 1
        if rank == 0:
            print "Using the", n_wrd_ngrams, "most frequent word n-grams of size", wrd_ngram_size
           
    # Corpus
    elif arg == "-cor":
        if a+1 < len(sys.argv) and not sys.argv[a+1].startswith("-"):
            corpus_root = sys.argv[a+1]
            i = i + 1
            if rank == 0:
                print 'Corpus set by user:', corpus_root

    a = a + i
    
if rank == 0:
    starttime = time.time() 
    
# First argument is expected to be dir where the job is running (from pwd)
cur_dir = sys.argv[1]
corpus_root = os.path.join(cur_dir,corpus_root) 
if rank == 0:
    print 'Corpus root:', corpus_root

corpus = PlaintextCorpusReader(corpus_root, '.*txt', encoding='UTF-8')
texts = corpus.fileids()

n_texts = len(texts)
tasks_per_worker = n_texts / nworkers
text_tasks = splitup_tasks(texts, nworkers, tasks_per_worker)
if rank == 0:
    print 'Workers:', nworkers
    print 'Texts:', n_texts
    print 'Tasks per worker:', tasks_per_worker
    
if rank == 0:
    text_classes = fextract_helper.find_classes(texts)
    

# Features: char n-grams
if char_ngrams:
    # Split up texts and process find char n-grams in subset of texts in each process
    all_char_ngrams = []
    text_char_ngrams = []
    a, t = fextract_helper.char_ngram_stats(text_tasks[rank], corpus, n_char_ngrams, char_ngram_size)
    r1 = workers.allgather(a)
    for r in r1:
        all_char_ngrams.extend(r)
    r2 = workers.allgather(t)
    for r in r2:
        text_char_ngrams.extend(r)
    
    # Each process creates features for a subset of texts
    cng_tasks = splitup_tasks(text_char_ngrams, nworkers, tasks_per_worker)
    f = fextract_helper.create_char_ngrams(n_char_ngrams, all_char_ngrams, cng_tasks[rank])
    r3 = workers.allgather(f)
    if rank == 0:
        charngram_features = []
        for r in r3:
            charngram_features.extend(r)
        
# Features: word n-grams
if wrd_ngrams:
    # Split up texts and process find word n-grams in subset of texts in each process
    all_wrd_ngrams = []
    text_wrd_ngrams = []
    a, t = fextract_helper.wrd_ngram_stats(text_tasks[rank], corpus, n_wrd_ngrams, wrd_ngram_size)
    r1 = workers.allgather(a)
    for r in r1:
        all_wrd_ngrams.extend(r)
    r2 = workers.allgather(t)
    for r in r2:
        text_wrd_ngrams.extend(r)
    
    # Each process creates features for a subset of texts
    wng_tasks = splitup_tasks(text_wrd_ngrams, nworkers, tasks_per_worker)
    f = fextract_helper.create_wrd_ngrams(n_wrd_ngrams, all_wrd_ngrams, wng_tasks[rank])
    r3 = workers.allgather(f)
    if rank == 0:
        wrdngram_features = []
        for r in r3:
            wrdngram_features.extend(r)
        
# TODO: Features: function words
if function_words:
    text_fws = []
    f, t = fextract_helper.extract_fws(text_tasks[rank], corpus, cur_dir + "/" + FUNC_FOLDER)
    r1 = worker.allgather(t)
    for r in r1:
        text_fws.extend(r)
    # Create features
    fw_tasks = splitup_tasks(text_fws, nworkers, tasks_per_worker)
    fm = fextract_helper.create_fw_features(f, fw_tasks[rank])
    r2 = workers.allgather(fm)
    if rank == 0:
        fw_features = []
        for r in r2:
            fw_features.extend(r)
        
# Process with rank 0 wraps it all up by creating the feature matrix
# and saving output to files
if rank == 0:
    # Create feature matrix with all features
    feature_matrix = [[] for i in range(n_texts)]
    for f in range(len(feature_matrix)):
        if char_ngrams:
            feature_matrix[f].extend(charngram_features[f])
        if wrd_ngrams:
            feature_matrix[f].extend(wrdngram_features[f])
        if function_words:
            feature_matrix[f].extend(fw_features[f])
    print 'Features:', len(feature_matrix), "x", len(feature_matrix[0])
            
    # Save features to files
    fextract_helper.save_features(os.path.join(cur_dir,FEATURE_FILE), feature_matrix, \
                                  os.path.join(cur_dir,CATEGORY_FILE), text_classes)
    

# Rank 0 stops timer and displays results
if rank == 0:
    endtime = time.time()
    n_features = len(feature_matrix[0])
    print "Total time elapsed analysing {0} texts: {1} sec. No. of features: {2}".format(n_texts,endtime-starttime,n_features)
    
# Clean-up: close filehandles, logs and sockets
mpi.finalize()
