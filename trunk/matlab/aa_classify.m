function avgAccuracy = aa_classify (runPython, voteReal, method, kernel, kerneloption, corpus, multi)
% runPython: Run the python script prior to classification
% method: AvA or OvA
% kernel: For AvA: . For OvA:
% kerneloption: ?
% corpus: Path to text-corpus
% voteReal: Whether to vote for real (over-)classes in AvA

autoCluster = false;


if strcmp(method,'OVA') && nargin < 5
    kerneloption = 2;
end

if nargin < 7
    multi = false;
end
multi

if runPython
    
    if nargin < 6 || isempty(corpus)
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

performanceFile = '/Users/epb/Documents/uni/kandidat/speciale/code/perf_svm.csv'
%performanceFile = '/home/epb/Documents/code/perf.csv'

%outputFolder = '/home/epb/Documents/output/';
outputFolder = '/Users/epb/Documents/uni/kandidat/speciale/output/';

%outFile = 'personae/150_3char/p3.out.txt'
%catFile = 'personae/150_3char/p3.cat.txt'
outFile = 'fed/2000_3char_kn/f2.out.txt'
catFile = 'fed/2000_3char_kn/f2.cat.txt'
%outFile = 'blogs/150_3char_150_3wrd/a1_005_10.out.txt'
%catFile = 'blogs/150_3char_150_3wrd/a1_005_10.cat.txt'
%outFile = '../code/out.txt'
%catFile = '../code/cat.txt'

data = load(strcat(outputFolder,outFile));
classes = load(strcat(outputFolder,catFile));

size(data)
size(classes)

nClasses = max(classes)
nRealClasses = nClasses;
%nTexts = size(data,1)
%nClasses = 3

% TODO: Clean-up in vote for real and autoCluster

if strcmp(method,'AVA') && voteReal
    fprintf('Vote-win goes to parent\n');
    realClasses = load('/Users/epb/Documents/uni/kandidat/speciale/code/real_cat.txt');
    %nClasses = size(realClasses,1);
    nRealClasses = size(realClasses,1);
end
%realClasses = [1:4;5:8;9:12];

if strcmp(method,'AVA') && autoCluster
    fprintf('Using autoclustering..\n');
    nClusters = 4;
    classes
    [classes, realClasses] = kmeanscluster(classes,nClasses,data,nClusters)
    nRealClasses = nClasses
    %realClasses = zeros(nRealClasses,nClusters);
    %for i=1:nRealClasses
    %    for j=1:nClusters
    %        realClasses(i,j) = (2*i)+j-2;
    %    end
    %end
    %realClasses
    nClasses = nClasses*nClusters
    %pause
end
    

tic;

if multi
    matlabpool open local 4
end

k = 10;
accuracies = zeros(1,k);
classPrecisions = zeros(nRealClasses,k); % precision per class
classRecalls = zeros(nRealClasses,k); % recall per class
%classF1s = zeros(nRealClasses,k); % F1-measure per class

foldIndices = crossvalind('Kfold',classes,k);
for i=1:k
    
    fprintf(strcat(['CV-iteration ', int2str(i), '\n']));
    
    % find indices of data/classes that will be used for training/test
    testIndices = (foldIndices == i);
    trainIndices = ~testIndices;
    %if i == 1
    %    testIndices(1:30,:)
    %end
    
    %classes
    trainClasses = classes(trainIndices,:);
    trainData = data(trainIndices,:);
    testData = data(testIndices,:);
    size(trainClasses);
    size(trainData);
    size(testData);
    %pause
    
    % TODO: We use "don't knows' in ava so this should be mentioned
    % Classification
    if strcmp(method,'AVA')
        if voteReal || autoCluster
            classified = classifyava(trainData,trainClasses,testData,nClasses,kernel,realClasses,multi);
            %classified = classifyava(data,classes,testData,trainIndices,kernel,realClasses);
        else
            classified = classifyava(trainData,trainClasses,testData,nClasses,kernel,[],multi);
        end
    elseif strcmp(method,'OVAC')
        classified = customova(trainClasses,trainData,testData,nClasses,kernel, kerneloption);
    elseif strcmp(method,'OVA')
        %classified = classifyova(data,classes,testData,trainIndices,kernel, kerneloption);
        classified = classifyova(trainClasses,trainData,testData,nClasses,kernel, kerneloption);
    end
    %classified = ceil(classified/4)
    
    
    
    %testClasses = ceil(testClasses/4);
    %nClasses = 3
    
    
    % ----------- Performance measures -----------------
    
    % Determine test-classes (possibly some real classes)
    testClasses = classes(testIndices);
    if strcmp(method,'AVA') && (voteReal || autoCluster)
        tc = zeros(size(testClasses));
        for n=1:size(testClasses,1)
            for c=1:nRealClasses
                subClasses = realClasses(c,:);
                if sum(ismember(subClasses,testClasses(n))) == 1
                    tc(n) = c;
                end
            end
        end
        testClasses = tc;
    end
    %classified
    %testClasses
    
            
    [a, cp, cr, cf] = performance(classified, testClasses,nRealClasses);
    accuracies(i) = a;
    classPrecisions(:,i) = cp;
    classRecalls(:,i) = cr;
    %classF1s(:,i) = cf;

end

% Alarm
alarmTrigger = 0.3;

% Catch NaNs in precisions and recalls if necessary
avgAccuracy = mean(accuracies);
accuracies
classPrecisions
avgClassPrecisions = mean(classPrecisions,2)
avgFoldPrecisions = mean(classPrecisions,1)

% Alarm if low precision found
if sum(isnan(avgClassPrecisions)) > 0 || sum(avgClassPrecisions<=alarmTrigger) > 0
    %fprintf('!!!!!!!!!!!!!!!! WARNING !!!!!!!!!!!!!');
    %avgClassPrecisions
end
avgPrecision = mean(avgClassPrecisions',2);
classRecalls
avgClassRecalls = mean(classRecalls,2)
avgFoldRecalls = mean(classRecalls,1)

% Alarm if low recall found
if sum(isnan(avgClassRecalls)) > 0 || sum(avgClassRecalls<=alarmTrigger) > 0
    %fprintf('!!!!!!!!!!!!!!!! WARNING !!!!!!!!!!!!!');
    %avgClassRecalls
end
avgRecall = meanwithnan(avgClassRecalls',2);

% F1 is calculated from the averages of precisions and recalls
%classF1s
%avgClassF1s = meanwithnan(classF1s,2)
avgClassF1s = zeros(nClasses,1);
for i=1:nClasses
    avgClassF1s(i) = f1(avgClassPrecisions(i), avgClassRecalls(i));
end
avgFoldF1s = zeros(1,k);
avgClassF1s
for i=1:k
    avgFoldF1s(i) = f1(avgFoldPrecisions(i),avgFoldRecalls(i));
end
avgFoldF1s
%avgFoldF1s = (2*avgFoldPrecisions.*avgFoldRecalls)./(avgFoldPrecisions+avgFoldRecalls)
%avgF1 = meanwithnan(avgClassF1s',2);

if multi
    matlabpool close
end

toc;

% Write performance measures to file
perf = nan(max(nClasses,k),7);
perf(1:k,1) = accuracies';
perf(1:k,2) = avgFoldPrecisions';
perf(1:k,3) = avgFoldRecalls';
perf(1:k,4) = avgFoldF1s';
perf(1:nClasses,5) = avgClassPrecisions;
perf(1:nClasses,6) = avgClassRecalls;
perf(1:nClasses,7) = avgClassF1s;
csvwrite(performanceFile,perf);

fprintf('\n------------------------- Done -------------------------\n\n');


function f = f1(p,r)
f = 0;
if p != 0 && r != 0
    f = (2*p*r) / (p+r);
end

