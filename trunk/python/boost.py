import math

class Samme:
    
    def train(self, features, classes, classifiers, K, M):
        '''
        @param features: Features per text
        @param classes: Classes per text
        @param classifiers: List of possible weak classifiers
        @param K: No. of different classes
        @param M: No. of iterations
        '''
        no_of_texts = len(classes)
        weights = [1/float(K) for n in range(no_of_texts)]
        no_of_classifiers = len(classifiers)
        self.alphas = [0 for m in range(M)]
        self.selected_classifiers = [None for m in range(M)]
        for m in M:
            
            # TODO: Fit a classifier
            errors = []
            weight_sum = sum(weights)
            for c in classifiers:
                classified = c.classify(classes, features)
                s = 0
                for t in range(len(classified)):
                    if classified[t] != classes[t]:
                        s = s + (weights[t]*1) # TODO: What to multiply with?
                errors.append(s/float(weight_sum))
            
            # Minimum error
            E = min(errors)
            
            # Selected classifier (the one with lowest error)
            for e in range(no_of_classifiers):
                if E == errors[e]:
                    self.selected_classifiers[m] = classifiers[e]
                    break
            
            # Alpha
            self.alphas[m] = math.log(((1-E)/E)+math.log(K-1))
            
            # Weight per text (normalized)
            for i in range(no_of_texts):
                nw = weights[i] * math.exp((self.alphas[m]*2)-1) # new weight
                weights[i] = nw / float(no_of_texts) # normalized 
             
    
    def classify(self, x):
        s = 0
        for t in range(self.T):
            s = s + (self.alphas[t]*self.selected_classifiers[t])
        return s