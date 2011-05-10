'''
Inspired by Peter Norvig. http://norvig.com/spell-correct.html
'''
import re, collections, codecs

class SpellCorrector:
    
    def __init__(self, alphabet):
        self.alphabet = alphabet
    
    def train(self, features):
        #print 'Training spell-corrector'
        if not hasattr(self, 'word_db'):
            self.word_db = collections.defaultdict(lambda: 1)
        for f in features:
            self.word_db[f] += 1
    
    def correct(self, word):
        candidates = self._known([word]) or self._known(self._edits1(word)) or \
        self._known_edits2(word) or [word]
        return max(candidates, key=self.word_db.get)
    
    def load_from_file(self, f):
        print 'Loading from', f
        lf = codecs.open(f,'r','utf-8')
        l = eval(lf.read())
        lf.close()
        self.word_db = collections.defaultdict(lambda: 1)
        for k, v in l:
            self.word_db[k] = v
        #print self.word_db
    
    def save_to_file(self, f):
        print 'Saving to', f
        #print self.word_db
        sf = codecs.open(f,'w','utf-8')
        #for w in self.word_db:
        #    sf.write(str(w) + "," + str(self.word_db) + "\n")
        sf.write(str(self.word_db.items()))
        sf.close()
    
    def _known(self, words): return set(w for w in words if w in self.word_db)
    
    def _edits1(self, word):
        splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes    = [a + b[1:] for a, b in splits if b]
        transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
        replaces   = [a + c + b[1:] for a, b in splits for c in self.alphabet if b]
        inserts    = [a + c + b     for a, b in splits for c in self.alphabet]
        return set(deletes + transposes + replaces + inserts)

    def _known_edits2(self, word):
        return set(e2 for e1 in self._edits1(word) for e2 in self._edits1(e1) if e2 in self.word_db)

def words(text): return re.findall('[a-z]+', text.lower()) 

if __name__ == '__main__':
    
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    sc = SpellCorrector(alphabet)
    
    #sc.train(words(file('/Users/epb/Documents/uni/kandidat/speciale/big.txt').read()))
    #print sc.correct('havvi')