import os
from lxml import etree

#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/blogs_utf8"
#corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/small"
corpus_root = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/blogs"

output_folder = "/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/data_formatted"

total_posts = 0
nonempty_posts = 0

ONLY_AUTHORSID_PREFIX = ""

for f in os.listdir(corpus_root):
    p = os.path.join(corpus_root, f)
    if os.path.isfile(p) and f.endswith(".xml"):
        name = f.rpartition(".xml")[0]
        author_id = f.partition(".")[0]
        
        if len(ONLY_AUTHORSID_PREFIX) == 0 or str(author_id)[0] == ONLY_AUTHORSID_PREFIX:
            print f
            xml_file = open(p, 'r').read()
            parser = etree.XMLParser(recover=True,remove_blank_text=True,encoding='latin1')
            root = etree.fromstring(xml_file,parser)
            post_no = 1
            for child in root:
                if child.tag == "post":
                    total_posts = total_posts + 1         
                    if child.text:
                        post = child.text.strip()
                        if len(post) > 0:
                            folder = output_folder + str(author_id)[0]
                            new_file = name + "_post" + str(post_no) + "_" + author_id + ".txt"
                                
                            nf = open(os.path.join(folder, new_file), "w")
                            nf.write(post.encode("utf-8"))
                            nf.flush()
                            
                            nonempty_posts = nonempty_posts + 1
                            post_no = post_no + 1
                    
print "Total posts:", total_posts
print "Non-empty posts:", nonempty_posts