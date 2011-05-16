import math, collections

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
        print 'Training boosted classifier with', no_of_texts, 'texts'
        weights = [1/float(no_of_texts) for n in range(no_of_texts)]
        self.classifiers = classifiers
        no_of_classifiers = len(self.classifiers)
        self.M = M
        self.alphas = [0 for x in range(self.M)]
        self.selected_classifiers = [None for x in range(self.M)]
        
        # Do classification for each of the classifiers
        classified = []
        for c in range(no_of_classifiers):
            myclassified = self.classifiers[c].classify(features[c])
                
            # NB classifier returns, for each text, a list of the X most probable
            # classes. The first element of this list is the most probable class
            # and the first element of this element is the class name
            classified.append([x[0][0] for x in myclassified])
        
        for m in range(self.M):
            
            print 'Weights', weights[:10]
            all_errors = []
            weight_sum = sum(weights)
            
            # Try classifying with all classifiers
            for c in range(no_of_classifiers):
                
                # Register the error for this classifier
                a_sum = 0
                err_sum = 0
                for t in range(no_of_texts):
                    if classified[c][t] != classes[t]:
                        err_sum = err_sum + weights[t]
                    else:
                        a_sum = a_sum + 1
                all_errors.append(err_sum/float(weight_sum))
            
                print 'Real accuracy', a_sum / float(no_of_texts)
            
            # Minimum error across all classifiers
            print 'Errors', all_errors
            min_error = min(all_errors)
            
            # No more boosting if accuracy is lower than 1/K
            if min_error <= 0 or min_error >= (1-(1/float(K))):
            #if min_error <= 0 or (1-min_error <= 1/float(K)):
                print min_error
                break
            
            # Select classifier with lowest error
            for c in range(no_of_classifiers):
                if min_error == all_errors[c]:
                    print 'Selected classifier', c
                    self.selected_classifiers[m] = c
                    break
            
            # Alpha
            self.alphas[m] = math.log((1-min_error)/min_error)+math.log(K-1)
            
            # Weight per text (normalized)
            for i in range(no_of_texts):
                if classified[self.selected_classifiers[m]][i] != classes[i]:
                    weights[i] = weights[i] * math.exp(self.alphas[m]) # new weight
                    #print weights[i] 
            
            weight_sum = sum(weights)
            for i in range(no_of_texts):
                #weights[i] = nw / float(no_of_texts) # normalized
                weights[i] = weights[i] / weight_sum # normalized 
        
        print 'Alphas', self.alphas
             
    
    def classify(self, data):
        
        # Classify with all weak classifiers
        all_classified = []
        for c in range(len(self.classifiers)):
            classifier = self.classifiers[c]
            all_classified.append(classifier.classify(data[c]))
        
        # Order classification results according to the M selected classifiers
        wclassified = []
        for m in range(self.M):
            c = self.selected_classifiers[m]
            if c is not None:
                wclassified.append(all_classified[c])
          
        # Calculate combined guess  
        classified = []
        for i in range(len(wclassified[0])):
            c = collections.defaultdict(lambda: 0)
            for m in range(self.M):
                if self.alphas[m] > 0:
                    guess = wclassified[m][i][0][0]
                    c[guess] = c[guess] + self.alphas[m]
            best_guess = max(c.values())
            #print 'Guesses:', c.values(), '- best:', best_guess
            
            for x in c:
                if c[x] == best_guess:
                    classified.append(x)
                    break 
        
        return classified