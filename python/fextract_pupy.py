from mpi import MPI
from nltk.corpus import PlaintextCorpusReader
from nltk.probability import FreqDist
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
nworkers = workers.size()-1
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
   
# Using master
if char_ngrams:
        
    if rank == 0:
        s1 = time.time()
        #print rank, 'Finding n-grams'
        all_ngs = fextract_helper.get_cngs(texts,corpus_root,char_ngram_size)
        e1 = time.time()
        print rank, 'Finding took', e1-s1, 'seconds'
        #print rank, 'Calculating most frequent n-grams'
        print len(all_ngs)
        s1 = time.time()
        all_ngs_freqs = FreqDist(all_ngs)
        tot_cngs = min([n_char_ngrams, all_ngs_freqs.B()])
        mostfreq_ngs = all_ngs_freqs.keys()[:tot_cngs]
        e1 = time.time()
        print rank, 'Calc took', e1-s1, 'seconds'
        #print rank, 'Sending most-frequent ngrams'
        s1 = time.time()
        workers.bcast(mostfreq_ngs,0)
        e1 = time.time()
        #print rank, 'Bcast took', e1-s1, 'seconds'
        f = []
    else:
        #print rank, 'Finding n-grams'
        s1 = time.time()
        t = fextract_helper.get_text_cngs(text_tasks[rank-1],corpus_root,char_ngram_size)
        e1 = time.time()
        print rank, 'Finding took', e1-s1, 'seconds'
        #print rank, 'Receiving most-frequent ngrams'
        s1 = time.time()
        mostfreq_ngs = workers.bcast(root=0)
        e1 = time.time()
        #print rank, 'Bcast took', e1-s1, 'seconds'
        #print rank, 'Creating features'
        s1 = time.time()
        f = fextract_helper.create_ngram_feats(mostfreq_ngs, t)
        e1 = time.time()
        print rank, 'Creating took', e1-s1, 'seconds' 
    
    #print rank, 'Gathering features'
    s1 = time.time()
    r2 = workers.gather(f,0)
    e1 = time.time()
    #print rank, 'Gather took', e1-s1, 'seconds'
    if rank == 0:    
        charngram_features = []
        for r in r2:
            charngram_features.extend(r)
            
if wrd_ngrams:
        
    print rank, 'Finding word n-grams'
    all_ngs = []
    a, t = fextract_helper.wrd_ngram_stats(text_tasks[rank], corpus, n_wrd_ngrams, wrd_ngram_size)
    print rank, 'Sending n-grams'
    r1 = workers.allgather(a)
    for r in r1:
        all_ngs.extend(r)
    print rank, 'Calculating most frequent word n-grams'
    all_ngs_freqs = FreqDist(all_ngs)
    tot_wngs = min([n_wrd_ngrams, all_ngs_freqs.B()])
    mostfreq_ngs = all_ngs_freqs.keys()[:tot_wngs]
    print rank, 'Creating features for word n-grams'
    f = fextract_helper.create_ngram_feats(mostfreq_ngs, t)
    print rank, 'Sending features'  
    r2 = workers.gather(f,0)
    if rank == 0:    
        wrdngram_features = []
        for r in r2:
            wrdngram_features.extend(r) 

## Using allgather
#if char_ngrams:
#        
#    print rank, 'Finding n-grams'
#    all_ngs = []
#    a, t = fextract_helper.char_ngram_stats(text_tasks[rank], corpus, n_char_ngrams, char_ngram_size)
#    print rank, 'Sending n-grams'
#    r1 = workers.allgather(a)
#    for r in r1:
#        all_ngs.extend(r)
#    print rank, 'Calculating most frequent n-grams'
#    all_ngs_freqs = FreqDist(all_ngs)
#    tot_cngs = min([n_char_ngrams, all_ngs_freqs.B()])
#    mostfreq_ngs = all_ngs_freqs.keys()[:tot_cngs]
#    print rank, 'Creating features'
#    f = fextract_helper.create_ngram_feats(mostfreq_ngs, t)  
#    print rank, 'Sending features'
#    r2 = workers.gather(f,0)
#    if rank == 0:    
#        charngram_features = []
#        for r in r2:
#            charngram_features.extend(r)
#            
#if wrd_ngrams:
#        
#    print rank, 'Finding word n-grams'
#    all_ngs = []
#    a, t = fextract_helper.wrd_ngram_stats(text_tasks[rank], corpus, n_wrd_ngrams, wrd_ngram_size)
#    print rank, 'Sending n-grams'
#    r1 = workers.allgather(a)
#    for r in r1:
#        all_ngs.extend(r)
#    print rank, 'Calculating most frequent word n-grams'
#    all_ngs_freqs = FreqDist(all_ngs)
#    tot_wngs = min([n_wrd_ngrams, all_ngs_freqs.B()])
#    mostfreq_ngs = all_ngs_freqs.keys()[:tot_wngs]
#    print rank, 'Creating features for word n-grams'
#    f = fextract_helper.create_ngram_feats(mostfreq_ngs, t)
#    print rank, 'Sending features'  
#    r2 = workers.gather(f,0)
#    if rank == 0:    
#        wrdngram_features = []
#        for r in r2:
#            wrdngram_features.extend(r)
        
    
#    # Find n-grams in provided texts
#    #a, t = fextract_helper.char_ngram_stats(text_tasks[rank],corpus,n_char_ngrams,char_ngram_size)
#    # Master finds most occurring n-grams across all texts
#    if rank == 0:
#        print 'Master finding all char n-grams'
#        ngs = fextract_helper.get_cngs(texts,corpus,char_ngram_size)
#        freqs = FreqDist(ngs)
#        tot_ngrams = min([n_char_ngrams, freqs.B()])
#        mostfreq_ngs = freqs.keys()[:tot_ngrams]
#        print 'Master found', len(mostfreq_ngs), 'most-occurring char n-grams'
#        workers.bcast(mostfreq_ngs,0)
#        cng_feat = [] # Master does not create features
#    # Other processes find n-grams per text
#    else: 
#        text_ngs = fextract_helper.get_text_cngs(text_tasks[rank-1],corpus,char_ngram_size)
#        mostfreq_ngs = workers.bcast(root=0)
#        cng_feat = fextract_helper.create_ngram_feats(mostfreq_ngs,text_ngs)
#        
#    # Send features to master
#    features = workers.gather(cng_feat,0)
#    
#    # Master creates final feature matrix
#    if rank == 0:
#        charngram_features = []
#        for f in features:
#            charngram_features.extend(f)
    
        
    # Send found n-grams to master
    #ngrams = workers.gather(a,0)
    
    # Master collects all n-grams in one structure
    # and broadcasts this structure to all processes
    #if rank == 0:
    #    all_ngrams = []
    #    for g in ngrams:
    #        all_ngrams.extend(g)
    #    workers.bcast(all_ngrams,0)
    #else:
        #workers.bcast(root=0)
    
    #print rank, ': Got', len(all_ngrams), 'ngrams in total'
    
    # All processes create features for their texts
    #my_features = fextract_helper.create_char_ngrams(n_char_ngrams,all_ngrams, t)
    #my_features = [range(n_char_ngrams) for i in range(len(t))]
    #print rank, ': My features:', my_features
    
    # Send features to master
    #features = workers.gather(my_features,0)
    
    # Master creates final feature matrix
    #if rank == 0:
    #    charngram_features = []
    #    for f in features:
    #        charngram_features.extend(f)
    
    
    
#    # Split up texts and process find char n-grams in subset of texts in each process
#    #all_char_ngrams = []
##    #text_char_ngrams = []
#    if rank != 0:
#        a, t = fextract_helper.char_ngram_stats(text_tasks[rank], corpus, n_char_ngrams, char_ngram_size)
#        workers.(a, 0)
#        all_char_ngrams = workers.recv(0, ALL_NGRAMS_TAG)
#        f = fextract_helper.create_char_ngrams(n_char_ngrams, all_char_ngrams, t)
#        workers.igather(f,0)
#    if rank == 0:
#        
#        all_char_ngrams = []
#        for r in r1:
#            all_char_ngrams.extend(r)
#        workers.
#        fhandle = workers.igather(f,0)
        
#    s1 = time.time()
#    r1 = workers.allgather(a)
#    e1 = time.time()
#    print os.getpid(), ': Waited for', e1-s1, 'seconds (1)'
#    for r in r1:
#        all_char_ngrams.extend(r)
#    #s2 = time.time()
#    #r2 = workers.allgather(t)
#    #e2 = time.time()
#    #print os.getpid(), ': Waited for', e2-s2, 'seconds (2)'
#    #for r in r2:
#    #    text_char_ngrams.extend(r)
#    
#    # Each process creates features for a subset of texts
#    #cng_tasks = splitup_tasks(text_char_ngrams, nworkers, tasks_per_worker)
#    #f = fextract_helper.create_char_ngrams(n_char_ngrams, all_char_ngrams, cng_tasks[rank])
#    f = fextract_helper.create_char_ngrams(n_char_ngrams, all_char_ngrams, text_char_ngrams)
##    s3 = time.time()
##    r3 = workers.allgather(f)
##    e3 = time.time()
##    print os.getpid(), ': Waited for', e3-s3, 'seconds (3)'
#    if rank == 0:
#        charngram_features = []
#        for r in r3:
#            charngram_features.extend(r)
#        
## Features: word n-grams
#if wrd_ngrams:
#    # Split up texts and process find word n-grams in subset of texts in each process
#    all_wrd_ngrams = []
#    #text_wrd_ngrams = []
#    a, text_wrd_ngrams = fextract_helper.wrd_ngram_stats(text_tasks[rank], corpus, n_wrd_ngrams, wrd_ngram_size)
#    s1 = time.time()
#    r1 = workers.allgather(a)
#    e1 = time.time()
#    print os.getpid(), ': Waited for', e1-s1, 'seconds (4)'
#    for r in r1:
#        all_wrd_ngrams.extend(r)
#    #s2 = time.time()
#    #r2 = workers.allgather(t)
#    #e2 = time.time()
#    #print os.getpid(), ': Waited for', e2-s2, 'seconds (5)'
#    #for r in r2:
#    #    text_wrd_ngrams.extend(r)
#    
#    # Each process creates features for a subset of texts
#    #wng_tasks = splitup_tasks(text_wrd_ngrams, nworkers, tasks_per_worker)
#    #f = fextract_helper.create_wrd_ngrams(n_wrd_ngrams, all_wrd_ngrams, wng_tasks[rank])
#    f = fextract_helper.create_wrd_ngrams(n_wrd_ngrams, all_wrd_ngrams, text_wrd_ngrams)
#    s3 = time.time()
#    r3 = workers.allgather(f)
#    e3 = time.time()
#    print os.getpid(), ': Waited for', e3-s3, 'seconds (6)'
#    if rank == 0:
#        wrdngram_features = []
#        for r in r3:
#            wrdngram_features.extend(r)
#        
## TODO: Features: function words
#if function_words:
#    text_fws = []
#    f, t = fextract_helper.extract_fws(text_tasks[rank], corpus, cur_dir + "/" + FUNC_FOLDER)
#    r1 = worker.allgather(t)
#    for r in r1:
#        text_fws.extend(r)
#    # Create features
#    fw_tasks = splitup_tasks(text_fws, nworkers, tasks_per_worker)
#    fm = fextract_helper.create_fw_features(f, fw_tasks[rank])
#    r2 = workers.allgather(fm)
#    if rank == 0:
#        fw_features = []
#        for r in r2:
#            fw_features.extend(r)
        
# 0 wraps it all up by creating the feature matrix
# and saving output to files
if rank == 0:
    # Create feature matrix with all features
    feature_matrix = [[] for i in range(n_texts)]
    for f in range(len(feature_matrix)):
#        pass
        if char_ngrams:
            feature_matrix[f].extend(charngram_features[f])
        if wrd_ngrams:
            feature_matrix[f].extend(wrdngram_features[f])
#        if function_words:
#            feature_matrix[f].extend(fw_features[f])
    print 'Features:', len(feature_matrix), "x", len(feature_matrix[0])
            
    # Save features to files
    fextract_helper.save_features(os.path.join(cur_dir,FEATURE_FILE), feature_matrix, \
                                  os.path.join(cur_dir,CATEGORY_FILE), text_classes)
    

# 0 stops timer and displays results
if rank == 0:
    endtime = time.time()
    n_features = len(feature_matrix[0])
    print "Total time elapsed analysing {0} texts: {1} sec. No. of features: {2}".format(n_texts,endtime-starttime,n_features)
    
# Clean-up: close filehandles, logs and sockets
mpi.finalize()
