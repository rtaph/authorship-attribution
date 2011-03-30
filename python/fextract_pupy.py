from mpi import MPI
from nltk.corpus import PlaintextCorpusReader
import fextract_helper
import subprocess
import os
import sys

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
rank = workers.rank()

# First argument is dir where the job is running (from pwd)
args =  sys.argv[1].split(" ")
print rank, args
cur_dir = args[0]
root = cur_dir + "/" + corpus_root

a = 1
while a < len(args):
    arg = args[a]
    print rank, arg
    i = 1
        
    # Character n-grams, with n-gram size and no. of n-grams
    if arg == "-c":
        char_ngrams = True
        if a+1 < len(args) and not args[a+1].startswith("-"):
            char_ngram_size = int(args[a+1])
            i = i + 1
            if a+2 < len(args) and not args[a+2].startswith("-"):
                n_char_ngrams = int(args[a+2])
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
        if a+1 < len(args) and not args[a+1].startswith("-"):
            wrd_ngram_size = int(args[a+1])
            i = i + 1
            if a+2 < len(args) and not args[a+2].startswith("-"):
                n_wrd_ngrams = int(args[a+2])
                i = i + 1
        print "Using the", n_wrd_ngrams, "most frequent word n-grams of size", wrd_ngram_size 
        #st_file.write("Using the " + str(n_wrd_ngrams) +  " most frequent word n-grams of size " + str(wrd_ngram_size) + "\n")
           
    # Corpus
    elif arg == "-r":
        if a+1 < len(args) and not args[a+1].startswith("-"):
            corpus_root = args[a+1]
            i = i + 1
                            
    a = a + i 
    
#print cur_dir
#d = subprocess.call('pwd')
#root = os.path.join(cur_dir, corpus_root)
#print rank, ": Root:", root

corpus = PlaintextCorpusReader(root, '.*txt', encoding='UTF-8')

if rank == 0:
    text_classes = fextract_helper.find_classes(texts)

texts = corpus.fileids()
#print rank, ': Workers:', nworkers
n_texts = len(texts)
#print rank, ': Texts:', n_texts
tasks_per_worker = n_texts / nworkers
#print rank, ': Tasks per worker:', tasks_per_worker
text_tasks = splitup_tasks(texts, nworkers, tasks_per_worker)

if char_ngrams:
    all_char_ngrams = []
    text_char_ngrams = []
    a, t = fextract_helper.char_ngram_stats(text_tasks[rank], corpus, n_char_ngrams, char_ngram_size)
    r1 = workers.allgather(a)
    for r in r1:
        all_char_ngrams.extend(r)
    #print rank, 'All char ngrams:', len(all_char_ngrams)
    r2 = workers.allgather(t)
    for r in r2:
        text_char_ngrams.extend(r)
    #print rank, 'Text char ngrams:', len(text_char_ngrams)
    
    cng_tasks = splitup_tasks(text_char_ngrams, nworkers, tasks_per_worker)
    f = fextract_helper.create_char_ngrams(n_char_ngrams, all_char_ngrams, cng_tasks[rank])
    r3 = workers.allgather(f)
    if rank == 0:
        charngram_features = []
        for r in r3:
            charngram_features.extend(r)
        print 'Feat1:' + str(len(charngram_features))
        print 'Feat2:' + str(len(charngram_features[0]))
        
if wrd_ngrams:
    all_wrd_ngrams = []
    text_wrd_ngrams = []
    a, t = fextract_helper.wrd_ngram_stats(text_tasks[rank], corpus, n_wrd_ngrams, wrd_ngram_size)
    r1 = workers.allgather(a)
    for r in r1:
        all_wrd_ngrams.extend(r)
    #print rank, 'All char ngrams:', len(all_char_ngrams)
    r2 = workers.allgather(t)
    for r in r2:
        text_wrd_ngrams.extend(r)
    #print rank, 'Text char ngrams:', len(text_char_ngrams)
    
    wng_tasks = splitup_tasks(text_wrd_ngrams, nworkers, tasks_per_worker)
    f = fextract_helper.create_wrd_ngrams(n_wrd_ngrams, all_wrd_ngrams, wng_tasks[rank])
    r3 = workers.allgather(f)
    if rank == 0:
        wrdngram_features = []
        for r in r3:
            wrdngram_features.extend(r)
        print 'Feat3:' + str(len(wrdngram_features))
        print 'Feat4:' + str(len(wrdngram_features[0]))
        
if function_words:
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
        
if rank == 0:
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
            
    # Save features to files
    fextract_helper.save_features(cur_dir + "/" + FEATURE_FILE, feature_matrix, \
                                  cur_dir + "/" + CATEGORY_FILE, text_classes)
    
#if mpi.MPI_COMM_WORLD.rank() == 0:
#    mpi.MPI_COMM_WORLD.send("Hello World!", 1)
#elif mpi.MPI_COMM_WORLD.rank() == 1:
#    message = mpi.MPI_COMM_WORLD.recv(0)
#    print message
#else:
#    print 'I am more than 1'

# Clean-up: close filehandles, logs and sockets
mpi.finalize()