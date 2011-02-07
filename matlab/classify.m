
% --- Use this when changing the parameters in the python script ---

% -c: character ngrams, ngram size, ngrams used
params = '-c 3 5';

fprintf(strcat(['Calling Python script with arguments: ', params, '\n']));
[status, fileStr] = system(strcat(['python ../python/nltk_test.py ', params]));
files = regexp(fileStr,'\n','split')
fprintf(strcat('File containing character n-gram freqs: ', char(files(1)), '\n'));
data = load(char(files(1)));
% Read possible classes, must be integers starting at 1
fprintf(strcat('File containing categories: ', char(files(2)), '\n'));
classes = load(char(files(2)));

%data = load('/Users/epb/Documents/uni/kandidat/speciale/code/python/out.txt');
%classes = load( '/Users/epb/Documents/uni/kandidat/speciale/code/python/cat.txt');

nClasses = max(classes);

% TODO: Support for more than two classes (OvA or AvA?)

% TODO: Cross-validation stratified?

% ----------------------------------------------
% ----------- Cross-validation -----------------
% ----------------------------------------------
accuracies = [];
k = 10;
classPrecisions = zeros(nClasses,k);
classRecalls = zeros(nClasses,k);
foldIndices = crossvalind('Kfold',classes,k);
for i=1:k
    
    fprintf(strcat(['CV, ', int2str(i), '. iteration\n']));
    
    % find indices of data/classes that will be used for training/test
    testIndices = (foldIndices == i);
    trainIndices = ~testIndices;
    
    % pick training/test data 
    testData = data(testIndices,:)
    trainingData = data(trainIndices,:)
    % pick training/test classes
    trainClasses = classes(trainIndices,:);
    testClasses = classes(testIndices,:);
    
    % train
    svmStruct = svmtrain(trainingData,trainClasses);
    
    % test
    classified = svmclassify(svmStruct,testData);
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
        
        precision = sum(correctClassifiedForC) / sum(totalClassifiedForC);
        classPrecisions(c,i) = precision;
        
        recall = sum(correctClassifiedForC) / sum(actualClassesForC);
        classRecalls(c,i) = recall;
    end
    
    %classperf(testClasses, classified);
    %cp
    %pause
end

avgAccuracy = mean(accuracies)
avgClassPrecisions = mean(classPrecisions,2)
avgClassRecalls = mean(classRecalls,2)



fprintf('\nDone!\n')