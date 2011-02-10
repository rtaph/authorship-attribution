
% --- Use this when changing the parameters in the python script ---

% -c: character ngrams, ngram size, ngrams used
%params = '-c 3 200';
%params = '-f -c 3 200';
%params = '-w 2 5';
params = '-c 3 5 -r /Users/epb/Documents/uni/kandidat/speciale/data/fed_papers/set4';

fprintf(strcat(['Calling Python script with arguments: ', params, '\n']));
[status, fileStr] = system(strcat(['python ../python/corpus_analysis.py ', params]));
files = regexp(fileStr,'\n','split');
fprintf(strcat(['Feature-file: ', char(files(1)), '\n']));
data = load(char(files(1)));
% Read possible classes, must be integers starting at 1
fprintf(strcat(['Class-file: ', char(files(2)), '\n']));
classes = load(char(files(2)))

% data = load('/Users/epb/Documents/uni/kandidat/speciale/code/out.txt');
% classes = load( '/Users/epb/Documents/uni/kandidat/speciale/code/cat.txt');

nClasses = max(classes)


% Multi-class learning
%svmStructs = [];
k = 2;
classPrecisions = zeros(nClasses,k); % precision per class
classRecalls = zeros(nClasses,k); % recall per class
for c=1:nClasses
    

    oneVsAllClasses = int16(classes == c)
    %oneClasses = classes(oneClassIndices)
    %allClasses = classes(~oneClassIndices)
    
    % TODO: Cross-validation stratified?

    % ----------------------------------------------
    % ----------- Cross-validation -----------------
    % ----------------------------------------------
    
    % The reason for doing CV as an inner loop is that we will get
    % equal size partitions of the two classes ("one" and "all")
    
    %k = 10;
    accuracies = zeros(1,k);
    %classPrecisions = zeros(nClasses,k); % precision per class
    %classRecalls = zeros(nClasses,k); % recall per class
    %foldIndices = crossvalind('Kfold',classes,k);
    foldIndices = crossvalind('Kfold',oneVsAllClasses,k)
    for i=1:k

        fprintf(strcat(['CV, ', int2str(i), '. iteration\n']));

        % find indices of data/classes that will be used for training/test
        testIndices = (foldIndices == i)
        trainIndices = ~testIndices

        % pick training/test data 
        testData = data(testIndices,:)
        trainingData = data(trainIndices,:)
        % pick training/test classes
        %trainClasses = classes(trainIndices,:)
        %testClasses = classes(testIndices,:)
        testClasses = oneVsAllClasses(testIndices,:)
        trainClasses = oneVsAllClasses(trainIndices,:)
        

        % train
         svmStruct = svmtrain(trainingData,trainClasses);
        %svmStructs(c) = svmtrain(trainingData,trainClasses)

        % test
        classified = svmclassify(svmStruct,testData)
        %classified = svmclassify(svmStructs(c),testData);
        correctClassified = classified == testClasses;

        % ----------- Performance measures -----------------

        % accuracy
        a = (sum(correctClassified))/size(classified,1);
        accuracies(i) = a;

        % TODO: remove inner loop when using multi-class
        % precision and recall
        for c=1:nClasses
            totalClassifiedForC = classified == c;
            actualClassesForC = testClasses == c;
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

        %classperf(testClasses, classified);
        %cp
        %pause
    end

end

avgAccuracy = mean(accuracies)
classPrecisions
avgClassPrecisions = mean(classPrecisions,2)
avgClassRecalls = mean(classRecalls,2)



fprintf('\nDone!\n')