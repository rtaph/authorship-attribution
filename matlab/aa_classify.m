function avgAccuracy = aa_classify (runPython, voteReal, method, kernel, kerneloption, corpus)
% runPython: Run the python script prior to classification
% method: AvA or OvA
% kernel: For AvA: . For OvA:
% kerneloption: ?
% corpus: Path to text-corpus
% voteReal: Whether to vote for real (over-)classes in AvA

autoCluster = false;

if nargin < 5
    kerneloption = 2;
end

if runPython
    
    if nargin < 6
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

%data = load('/Users/epb/Documents/uni/kandidat/speciale/code/out.txt');
%classes = load('/Users/epb/Documents/uni/kandidat/speciale/code/cat.txt')
%data = load('/Users/epb/Documents/uni/kandidat/speciale/output/almedad/150_3char_150_3wrd/a1_3_40_multi.out.txt');
%classes = load('/Users/epb/Documents/uni/kandidat/speciale/output/almedad/150_3char_150_3wrd/a1_3_40_multi.cat.txt');
data = load('/Users/epb/Documents/uni/kandidat/speciale/output/blogs/150_3char_150_3wrd/set30_10_1.out.txt');
classes = load('/Users/epb/Documents/uni/kandidat/speciale/output/blogs/150_3char_150_3wrd/set30_10_1.cat.txt');
%data = load('/Users/epb/Documents/uni/kandidat/speciale/output/fed/150_3char_150_3wrd/all_single_quat_multi.out.txt');
%classes = load('/Users/epb/Documents/uni/kandidat/speciale/output/fed/150_3char_150_3wrd/all_single_quat_multi.cat.txt');

%data = data(:,1:3)
%classes(1:30,:)
%data(1:30,1:10)
%y = pdist(data);
%z = linkage(y);
%[H,T] = dendrogram(z,'colorthreshold','default');
%pause;

%plot(data(classes==1,1),data(classes==1,2),'r.','MarkerSize',12)
%hold on
%plot(data(classes==2,1),data(classes==2,2),'b.','MarkerSize',12)
%plot(ctrs(:,1),ctrs(:,2),'kx',...
%    'MarkerSize',12,'LineWidth',2)
%plot(ctrs(:,1),ctrs(:,2),'ko',...
%    'MarkerSize',12,'LineWidth',2)
%legend('Cluster 1','Cluster 2','Centroids',...
%      'Location','NW')
%pause

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
k = 4;
accuracies = zeros(1,k);
classPrecisions = zeros(nRealClasses,k); % precision per class
classRecalls = zeros(nRealClasses,k); % recall per class
classF1s = zeros(nRealClasses,k); % F1-measure per class

foldIndices = crossvalind('Kfold',classes,k);
for i=1:k
    
    %fprintf(strcat(['CV-iteration ', int2str(i), '\n']));
    
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
    %pause
    
    % TODO: We use "don't knows' in ava so this should be mentioned
    % Classification
    if strcmp(method,'AVA')
        if voteReal || autoCluster
            classified = classifyava(trainData,trainClasses,testData,nClasses,kernel,realClasses);
            %classified = classifyava(data,classes,testData,trainIndices,kernel,realClasses);
        else
            classified = classifyava(trainData,trainClasses,testData,nClasses,kernel);
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
    classF1s(:,i) = cf;

end

% Alarm
alarmTrigger = 0.3;

% Catch NaNs in precisions and recalls if necessary
avgAccuracy = mean(accuracies);
accuracies;
classPrecisions;
avgClassPrecisions = meanwithnan(classPrecisions);

% Alarm if low precision found
if sum(isnan(avgClassPrecisions)) > 0 || sum(avgClassPrecisions<=alarmTrigger) > 0
    fprintf('!!!!!!!!!!!!!!!! WARNING !!!!!!!!!!!!!');
    avgClassPrecisions
end
avgPrecision = meanwithnan(avgClassPrecisions')
classRecalls;
avgClassRecalls = meanwithnan(classRecalls);

% Alarm if low recall found
if sum(isnan(avgClassRecalls)) > 0 || sum(avgClassRecalls<=alarmTrigger) > 0
    fprintf('!!!!!!!!!!!!!!!! WARNING !!!!!!!!!!!!!');
    avgClassRecalls
end
avgRecall = meanwithnan(avgClassRecalls')
classF1s;
avgClassF1s = meanwithnan(classF1s);
avgF1 = meanwithnan(avgClassF1s')

toc;

fprintf('\n------------------------- Done -------------------------\n\n');