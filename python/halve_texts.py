import os
from lxml import etree
from nltk.corpus import PlaintextCorpusReader

#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/a2_4_8"
#output_folder = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/a2_4_16"
corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/test/test1_32"
output_folder = "/Users/epb/Documents/uni/kandidat/speciale/data/test/test1_64"    

ONLY_FIRST_HALF = False

for f in os.listdir(corpus_root):
    p = os.path.join(corpus_root, f)
    if os.path.isfile(p) and f.endswith(".txt"):
        name = f.rpartition(".txt")[0]
        print f
        txt_file = open(p, 'r')
        txt = txt_file.read()
        txt_file.close()
        
        wrds = len(txt.split())
        chars = len(txt)
        
        if wrds > 1:
            i = 0        
            if wrds == 2:
                i = txt.find(" ")
            else:
                i = chars / 2
                try: # try going forward to find a space where to split..
                    while not txt[i].isspace():
                        i = i + 1
                except IndexError, e: # .. it didn't work so we try to go backwards
                    i = chars / 2
                    while not txt[i].isspace():
                        i = i - 1
                    
            #if f == "9289.male.23.Marketing.Taurus_post5_9289_1.txt":
            #    print i
            first_half = txt[:i]
            second_half = txt[i:]
            
            new_name1 = name + "_1.txt"
            nf1 = open(os.path.join(output_folder, new_name1), "w")
            nf1.write(first_half)
            nf1.flush()
                       
            if not ONLY_FIRST_HALF:     
                new_name2 = name + "_2.txt"
                nf2 = open(os.path.join(output_folder, new_name2), "w")
                nf2.write(second_half)
                nf2.flush()
            
        else: # not enough text for two files
            
            new_name = name + ".txt"
            nf = open(os.path.join(output_folder, new_name), "w")
            nf.write(txt)
            nf.flush()
