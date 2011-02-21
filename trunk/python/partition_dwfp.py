import os

#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/dark_web_forum_portal/almedad/almedad_all.txt"
corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/dark_web_forum_portal/ansar1/ansar1_all.txt"

output_folder = "/Users/epb/Documents/uni/kandidat/speciale/data/dark_web_forum_portal/ansar1/all/"
#output_folder = "/Users/epb/Documents/uni/kandidat/speciale/data/dark_web_forum_portal/almedad/all/"

f = open(corpus_root,'r')
print f.readline() # header line

for li in f:
    l = li.split('\t')
    k = len(l)
    if k > 0:
        msgid = l[0]
        if k > 1:
            tid = l[1]
            if k > 3:
                memid = l[3].replace(" ", "")
                if len(memid) > 20:
                    memid = memid[:20]
                if len(l) > 5:
                    msg = l[5]
                    msg = msg.strip()
                    if len(msg) > 0:
                        
                        
                        #filename = ".".join(["m"+memid,msgid,tid]) + "_" + memid + ".txt"
                        filename = ".".join(["m"+memid,msgid,tid]) + ".txt"
                        print filename
                        nf = open(os.path.join(output_folder,filename),"w")
                        nf.write(msg)
                        nf.flush()        

f.close()