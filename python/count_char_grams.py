s = "And so, my fellow Americans. Ask not what your country can do for you. Ask what you can do for your country. My fellow citizens of the world. Ask not what America will do for you, but what together we can do for the Freedom of Man."

print "Chars"

s = s.lower()
#s = s.replace(".","")
#s = s.replace(",","")

oc = {}

for x in range(0,len(s)):
    if x < len(s)-2:
        ngram = s[x] + s[x+1] + s[x+2]
        if oc.has_key(ngram):
            oc[ngram] = oc[ngram] + 1
        else:
            oc[ngram] = 1


import operator
#sorted_oc = sorted(oc.iteritems(), key=operator.itemgetter(1))

for o in oc.iteritems():
    if o[1] == 1:
        print o
        
print len(oc)

print "Words"
s = "And so, my fellow Americans. Ask not what your country can do for you. Ask what you can do for your country. My fellow citizens of the world. Ask not what America will do for you, but what together we can do for the Freedom of Man."

#s = s.lower()
s = s.replace(".","")
s = s.replace(",","")

sl = s.split(" ")

wc = {}

x = 0
for x in range(0,len(sl)):
    if x < len(sl)-2:
        wrds = sl[x] + " " + sl[x+1] + " " + sl[x+2]
        if wc.has_key(wrds):
            wc[wrds] = wc[wrds] + 1
        else:
            wc[wrds] = 1

#print wc
for w in wc.iteritems():
#    if w[1] > 3:
        print w
        
print len(wc)