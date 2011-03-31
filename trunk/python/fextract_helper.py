from nltk.util import ngrams
from nltk.probability import FreqDist
import os

def find_classes(texts):
    text_classes = []
    for text in texts:
        found_category = text.partition(".")[0]
        text_classes.append(found_category)
    return text_classes

def load_wrds(dir, cmt="//"):
    '''
    Load a list of a words from some text files found in a given dir.
    Each line is considered a word if it is not a comment.
    @param dir: Where the files are found
    @param cmt: Comment-line indicator
    '''
    wrds = []
    for e in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, e)):
            f = open(os.path.join(dir,e))
            for l in f:
                if not l.startswith(cmt):
                    wrds.append(l.rstrip())
            f.close()
    return wrds

def char_ngram_stats(texts, corpus, n_char_ngrams, char_ngram_size):
    
    n_texts = len(texts)
    
    all_char_ngrams = [] # All n-grams found in entire corpus
    text_char_ngrams = [] # The frequency of char n-grams found in each text
    
    for text in texts:
        
        if not text.endswith(".txt"):
            continue
        #print text
        
        wrd_tokens = corpus.words(text)
        empty = len(corpus.raw(text)) == 0 
    
        if not empty:
            text_str = corpus.raw(text).replace('\r','').replace('\n', ' ')
            char_ng = ngrams(text_str, char_ngram_size)
            #print len(char_ng)
            #print FreqDist(char_ng)
            #print len(text_char_ngrams)
            #text_char_ngrams.append(FreqDist(char_ng))
            text_char_ngrams.append(char_ng)
            #print 'e'
            all_char_ngrams.extend(char_ng)
        else:
            #text_char_ngrams.append(FreqDist())
            text_char_ngrams.append([])
            
    #print 'Returning'
    return all_char_ngrams, text_char_ngrams

def create_char_ngrams(n_char_ngrams, all_char_ngrams, text_char_ngrams):
    print os.getpid(), ": Attaching char n-grams to list of features"
    n_texts = len(text_char_ngrams)
    #print os.getpid(), n_texts
    feature_matrix = [[] for i in range(n_texts)]
    
    # Frequency of all possible n-grams across corpus
    all_char_ngrams_freqs = FreqDist(all_char_ngrams)
    # we can't look for more n-grams than we have
    tot_ngrams = min([n_char_ngrams, all_char_ngrams_freqs.B()])
    
    # Select char n-gram features
    for t in range(n_texts):
        #print 'Text', t
        #freqs = text_char_ngrams[t]
        freqs = FreqDist(text_char_ngrams[t])
        #print freqs.items()[:5]
        # TODO: Correct to calculate delta here from text-only?
        delta = freqs.Nr(1) / float(freqs.Nr(1) + 2*freqs.Nr(2))
        #print delta
            
        # Step through X most frequent n-grams across corpus, the feature is the
        # relative frequency for each n-gram in each text
        for r in range(tot_ngrams):
            ngram = all_char_ngrams_freqs.keys()[r]
            freq = freqs.freq(ngram)
            #print freq
            feature_matrix[t].append(freq)
    
    return feature_matrix

def wrd_ngram_stats(texts, corpus, n_wrd_ngrams, wrd_ngram_size):
    n_texts = len(texts)
    feature_matrix = [[] for i in range(n_texts)]
    
    all_wd_ngrams = []
    text_wrd_ngrams = []
    
    for text in texts:
        
        if not text.endswith(".txt"):
            continue
        #print text
        
        wrd_tokens = corpus.words(text)
        empty = len(corpus.raw(text)) == 0

        if not empty:
            lower_wrds = [w.lower() for w in wrd_tokens if w.isalnum()]
            wrd_ng = ngrams(lower_wrds, wrd_ngram_size)
            #text_wrd_ngrams.append(FreqDist(wrd_ng))
            text_wrd_ngrams.append(wrd_ng)
            all_wd_ngrams.extend(wrd_ng)
        else:
            #text_wrd_ngrams.append(FreqDist())
            text_wrd_ngrams.append([])
            
    return all_wd_ngrams, text_wrd_ngrams

def create_wrd_ngrams(n_wrd_ngrams, all_wd_ngrams, text_wrd_ngrams):
    print os.getpid(), ": Attaching word n-grams to list of features"
    n_texts = len(text_wrd_ngrams)
    feature_matrix = [[] for i in range(n_texts)]
    all_wrd_ngrams_freqs = FreqDist(all_wd_ngrams)
        
    # we can't look for more n-grams than we have
    tot_ngrams = min([n_wrd_ngrams, all_wrd_ngrams_freqs.B()])
        
    # Select word n-gram features
    for t in range(n_texts):
        #print 'Text', t
        #freqs = text_wrd_ngrams[t]
        freqs = FreqDist(text_wrd_ngrams[t])
            
        # Step through X most frequent n-grams across corpus, the feature is the
        # relative frequency for each n-gram in each text
        for r in range(tot_ngrams):
            ngram = all_wrd_ngrams_freqs.keys()[r]
            freq = freqs.freq(ngram)
            feature_matrix[t].append(freq)
            
    return feature_matrix    

def extract_fws(texts, corpus, fw_root):
    n_texts = len(texts)
    feature_matrix = [[] for i in range(n_texts)]
    
    func_wrds = load_wrds(fw_root)
    text_fws = []
    
    for text in texts:
        
        if not text.endswith(".txt"):
            continue
        #print text
        
        wrd_tokens = corpus.words(text)
        empty = len(corpus.raw(text)) == 0
        
        if not empty:
            lower_wrds = [w.lower() for w in wrd_tokens if w.isalnum()]
            my_func_wrds = [w for w in lower_wrds if func_wrds.count(w) > 0]
            #text_fws.append(FreqDist(my_func_wrds))
            text_fws.append(my_func_wrds)
        else:
            #text_fws.append(FreqDist())
            text_fws.append([])
            
    return func_wrds, text_fws

def create_fw_features(func_words, text_fws):
    print "Attaching function words to list of features"
    n_texts = len(text_fws)
    feature_matrix = [[] for i in range(n_texts)]
    for t in range(n_texts):
        print 'Text', t
        #freqs = text_funcwrd_freqs[t]
        freqs = FreqDist(text_fws[t])
        for f in func_words:
            freq = freqs.freq(f)
            feature_matrix[t].append(freq)
            
    return feature_matrix
    
def save_features(feature_file, feature_matrix, class_file, text_classes):
    
    print "Outputting features to", feature_file
    ff = open(feature_file,'w')
    for feat in feature_matrix:
        strlist = [str(i) for i in feat]
        ff.write(" ".join(strlist) + "\n")
    ff.flush()
    
    # TODO: Output real classes + subclasses to real_cat
    
    print "Outputting classes to", class_file
    distinct_classes = list(set(text_classes))
    cf = open(class_file,'w')
    for c in text_classes:
        i = distinct_classes.index(c) + 1
        cf.write(str(i) + "\n")
    cf.flush()
    