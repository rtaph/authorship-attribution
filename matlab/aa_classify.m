function avgAccuracy = aa_classify (runPython, method, kernel, kerneloption, corpus)

%RUN_PYTHON = false;
%METHOD = 'AVA'; % AVA or OVA

if nargin < 4
    kerneloption = 2;
end

if runPython
    
    if nargin < 5
        corpus = '/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/set3_10_2/';
    end
    featureParams = '-c 3 150 -w 3 150';
    params = strcat([featureParams, ' -r ', corpus]); 

    fprintf(strcat(['Calling Python script, args: ', params, '\n']));
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
classes = load( '/Users/epb/Documents/uni/kandidat/speciale/code/cat.txt')
nClasses = max(classes)

tic;
k = 4;
accuracies = zeros(1,k);
classPrecisions = zeros(nClasses,k); % precision per class
classRecalls = zeros(nClasses,k); % recall per class
classF1s = zeros(nClasses,k); % F1-measure per class

foldIndices = crossvalind('Kfold',classes,k);
for i=1:k
    
    %fprintf(strcat(['CV-iteration ', int2str(i), '\n']));
    
    % find indices of data/classes that will be used for training/test
    testIndices = (foldIndices == i);
    trainIndices = ~testIndices;
    testClasses = classes(testIndices);
    
    % TODO: We use "don't knows' in ava so this should be mentioned
    
    % Classification
    if strcmp(method,'AVA')
        classified = classifyava(data,classes,testIndices,trainIndices,kernel);
    elseif strcmp(method,'OVA')
        classified = classifyova(data,classes,testIndices,trainIndices,kernel, kerneloption);
    end
    classified;
    testClasses;
    
    % ----------- Performance measures -----------------
    
    [a, cp, cr, cf] = performance(classified, testClasses,nClasses);
    accuracies(i) = a;
    classPrecisions(:,i) = cp;
    classRecalls(:,i) = cr;
    classF1s(:,i) = cf;

end

% TODO: Alarm if some precision/recall is low

% Catch NaNs in precisions and recalls if necessary
avgAccuracy = mean(accuracies);
accuracies
classPrecisions;
avgClassPrecisions = meanwithnan(classPrecisions);
classRecalls;
avgClassRecalls = meanwithnan(classRecalls);
classF1s;
avgClassF1s = meanwithnan(classF1s);

toc;

fprintf('\n------------------------- Done -------------------------\n\n');