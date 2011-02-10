% -c: character ngrams, ngram size, ngrams used
%params = '-c 3 200';
%params = '-f -c 3 200';
%params = '-w 2 5';
params = '-f -r /Users/epb/Documents/uni/kandidat/speciale/data/fed_papers/set4';

fprintf(strcat(['Calling Python script with arguments: ', params, '\n']));
[status, fileStr] = system(strcat(['python ../python/corpus_analysis.py ', params]));
files = regexp(fileStr,'\n','split');
fprintf(strcat(['Feature-file: ', char(files(1)), '\n']));
data = load(char(files(1)));
% Read possible classes, must be integers starting at 1
fprintf(strcat(['Class-file: ', char(files(2)), '\n']));
classes = load(char(files(2)));

%data = load('/Users/epb/Documents/uni/kandidat/speciale/code/out.txt');
%classes = load( '/Users/epb/Documents/uni/kandidat/speciale/code/cat.txt')

nClasses = max(classes);

k = 3;
accuracies = zeros(1,k);
classPrecisions = zeros(nClasses,k); % precision per class
classRecalls = zeros(nClasses,k); % recall per class
foldIndices = crossvalind('Kfold',classes,k);
for i=1:k

    % votes for a text belonging to a class
    %votes = zeros(size(data,1),nClasses);
    
    % find indices of data/classes that will be used for training/test
    testIndices = (foldIndices == i)
    trainIndices = ~testIndices;
    allTestClasses = classes(testIndices);
    
    % Classification
    votes = classifyava(data,classes,testIndices,trainIndices);
    
    % Evaluate vote. The highest vote to achieve is nClasses-1, as this
    % is the number of pairs each class participates in.
    votes = votes(testIndices,:)
    classified = zeros(size(allTestClasses,1),1);
    for v=1:size(votes,1)
        [high, class] = max(votes(v,:));
        
        % Make sure we only have _one_ winner
        if sum(ismember(votes(v,:),high)) == 1
            classified(v) = class;
        end
    end
    correctClassified = classified == allTestClasses;
    
    % ----------- Performance measures -----------------
    
    % accuracy
    a = (sum(correctClassified))/size(classified,1);
    accuracies(i) = a;
    
    % precision and recall
    for c=1:nClasses
        totalClassifiedForC = classified == c;
        actualClassesForC = allTestClasses == c;
        correctClassifiedForC = correctClassified(totalClassifiedForC);
        
        precision = 0.0;
        if sum(totalClassifiedForC) > 0
            precision = sum(correctClassifiedForC) / sum(totalClassifiedForC);
        end
        classPrecisions(c,i) = precision;
        
        recall = 0.0;
        if sum(actualClassesForC) > 0
            recall = sum(correctClassifiedForC) / sum(actualClassesForC);
        end
        classRecalls(c,i) = recall;
    end

end

avgAccuracy = mean(accuracies)
avgClassPrecisions = mean(classPrecisions,2)
avgClassRecalls = mean(classRecalls,2)

fprintf('\n------------------------- Done -------------------------\n\n');