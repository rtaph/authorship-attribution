RUN_PYTHON = false;

if RUN_PYTHON
    %params = '-c 3 200';
    %params = '-f -c 3 200';
    %params = '-w 2 5';
    %params = '-f -c 3 200 -w 2 50 -r /Users/epb/Documents/uni/kandidat/speciale/data/fed_papers/set5';
    params = '-f -w 2 50 -r /Users/epb/Documents/uni/kandidat/speciale/data/fed_papers/set6';

    fprintf(strcat(['Calling Python script with arguments: ', params, '\n']));
    [status, fileStr] = system(strcat(['python ../python/corpus_analysis.py ', params]));
    files = regexp(fileStr,'\n','split');
    fprintf(strcat(['Feature-file: ', char(files(1)), '\n']));
    data = load(char(files(1)));
    % Read possible classes, must be integers starting at 1
    fprintf(strcat(['Class-file: ', char(files(2)), '\n']));
    classes = load(char(files(2)));
else
    data = load('/Users/epb/Documents/uni/kandidat/speciale/code/out.txt');
    classes = load( '/Users/epb/Documents/uni/kandidat/speciale/code/cat.txt');
end

nClasses = max(classes);

k = 5;
accuracies = zeros(1,k);
classPrecisions = zeros(nClasses,k); % precision per class
classRecalls = zeros(nClasses,k); % recall per class
foldIndices = crossvalind('Kfold',classes,k);
for i=1:k

    % votes for a text belonging to a class
    %votes = zeros(size(data,1),nClasses);
    
    % find indices of data/classes that will be used for training/test
    testIndices = (foldIndices == i);
    trainIndices = ~testIndices;
    testClasses = classes(testIndices);
    
    % TODO: Should be possible to use SVM with different parameters from
    % here
    
    % Classification
    votes = classifyava(data,classes,testIndices,trainIndices);
    
    % TODO: We use "don't knows' in ava so this should be mentioned
    
    % Evaluate vote. The highest vote to achieve is nClasses-1, as this
    % is the number of pairs each class participates in.
    votes = votes(testIndices,:);
    classified = zeros(size(testClasses,1),1);
    for v=1:size(votes,1)
        [high, class] = max(votes(v,:));
        
        % Make sure we only have _one_ winner
        if sum(ismember(votes(v,:),high)) == 1
            classified(v) = class;
        end
    end
    %classified
    correctClassified = classified == testClasses;
    
    % ----------- Performance measures -----------------
    
    % accuracy
    a = (sum(correctClassified))/size(classified,1);
    accuracies(i) = a;
    
    % precision and recall
    for c=1:nClasses
        totalClassifiedForC = classified == c;
        actualClassesForC = testClasses == c;
        correctClassifiedForC = correctClassified(totalClassifiedForC);
        
        precision = 0.0;
        if sum(totalClassifiedForC) > 0
            precision = sum(correctClassifiedForC) / sum(totalClassifiedForC);
        elseif sum(actualClassesForC) == 0
            % We cannot calculate precision if there are no instances of a
            % given class in the test set and none was assigned.
            precision = NaN;
        end
        classPrecisions(c,i) = precision;
        
        % We cannot calculate recall if there are no instances of a given
        % class in the test set.
        recall = NaN;
        if sum(actualClassesForC) > 0
            recall = sum(correctClassifiedForC) / sum(actualClassesForC);
        end
        classRecalls(c,i) = recall;
    end

end

% Catch NaNs in precisions and recalls if necessary
avgAccuracy = mean(accuracies)
%classPrecisions
avgClassPrecisions = meanwithnan(classPrecisions)
%classRecalls
avgClassRecalls = meanwithnan(classRecalls)

fprintf('\n------------------------- Done -------------------------\n\n');