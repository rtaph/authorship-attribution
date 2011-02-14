tic;

RUN_PYTHON = false;

if RUN_PYTHON
    %params = '-c 3 300 -w 3 300';
    %params = '-c 3 300 -w 3 300 -r /Users/epb/Documents/uni/kandidat/speciale/data/PersonaeCorpus_onlineVersion/set2';
    %params = '-f -c 3 200';
    %params = '-w -c';
    %params = '-f -c 3 200 -w 2 50 -r /Users/epb/Documents/uni/kandidat/speciale/data/fed_papers/set5';
    params = '-c 3 200 -r /Users/epb/Documents/uni/kandidat/speciale/data/PersonaeCorpus_onlineVersion/set2';

    fprintf(strcat(['Calling Python script with arguments: ', params, '\n']));
    [status, pythonOut] = system(strcat(['python ../python/corpus_analysis.py ', params]));
    fprintf(pythonOut);
    %files = regexp(pythonOut,'\n','split');
    %fprintf(strcat(['Feature-file: ', char(files(1)), '\n']));
    %data = load(char(files(1)));
    % Read possible classes, must be integers starting at 1
    %fprintf(strcat(['Class-file: ', char(files(2)), '\n']));
    %classes = load(char(files(2)));
end

data = load('/Users/epb/Documents/uni/kandidat/speciale/code/out.txt');
classes = load( '/Users/epb/Documents/uni/kandidat/speciale/code/cat.txt');
nClasses = max(classes);

k = 5;
accuracies = zeros(1,k);
classPrecisions = zeros(nClasses,k); % precision per class
classRecalls = zeros(nClasses,k); % recall per class
foldIndices = crossvalind('Kfold',classes,k);
for i=1:k
    
    %fprintf(strcat(['CV-iteration ', int2str(i), '\n']));

    % votes for a text belonging to a class
    %votes = zeros(size(data,1),nClasses);
    
    % find indices of data/classes that will be used for training/test
    testIndices = (foldIndices == i);
    trainIndices = ~testIndices;
    testClasses = classes(testIndices);
    
    % TODO: Should be possible to use SVM with different parameters from
    % here
    % TODO: We use "don't knows' in ava so this should be mentioned
    
    % Classification
    %classified = classifyava(data,classes,testIndices,trainIndices);
    classified = classifyova(data,classes,testIndices,trainIndices);
    
    % ----------- Performance measures -----------------
    
    correctClassified = classified == testClasses;
    
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

toc;

fprintf('\n------------------------- Done -------------------------\n\n');