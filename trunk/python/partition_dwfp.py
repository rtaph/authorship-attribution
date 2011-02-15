corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/dark_web_forum_portal/almedad/almedad_all.txt"

output_folder = "/Users/epb/Documents/uni/kandidat/speciale/data/dark_web_forum_portal/almedad"

f = open(corpus_root,'r')
print f.readline()

for li in f:
    l = li.split('\t')
    msg_id = l[0]
    thread_id = l[1]
    thread = l[2]
    member_id = l[3]
    member = l[4]
    msg = l[5]
    year = l[6]
    month = l[7]
    day = l[8]
    date = l[9]
    print date

f.close()