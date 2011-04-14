%function classified = classifyava(data, classes, testData, trainIndices, kernel, realClasses)
function classified = classifyava(trainData, trainClasses, testData, nClasses, kernel, realClasses)
% SVM multiclass classification using All vs. All.
%
% Input
% -----
% data: A matrix (n x m) of data. The n rows each represent a text and the
% m columns represent the features of each text.
% classes: A vector (n x 1) that determines which of q classes (integers
% starting at 1) each text of the data set belongs to.
% testData: 
% trainIndices: A vector (n x 1) of logical indices of the classes used for
% training.
%
% Output
% ------
% classified: A vector of length sum(testIndices), with a the class of each
% text in the test-set.


% testIndices: A vector (n x 1) of logical indices of the classes used for
% test.

%nClasses = max(classes);

% votes for a text of the test set belonging to a class
%votes = zeros(size(data,1),nClasses);
votes = zeros(size(testData,1),nClasses);

%testIndices(1:4,:)
%testClasses = classes(testIndices);

for c=1:nClasses
    for d=(c+1):nClasses
        %fprintf(strcat(['c,d: ', int2str(c), ',', int2str(d), '\n']));
        %cIndices = classes == c;
        %dIndices = classes == d;
        cIndices = trainClasses == c;
        dIndices = trainClasses == d;
        cdIndices = logical(cIndices + dIndices);
        %pause
        
        
        %cdTestIndices = logical(testIndices .* cdIndices);
        %cdTrainIndices = logical(trainIndices .* cdIndices);
        
        %if c == 13 && d == 15
        %    cdTestIndices(1:30,:)
        %    cdTrainIndices(1:30,:)
        %end
        
        %fprintf(strcat(['Training on indexes ', int2str(find(cdTrainIndices')), '\n']));
        %fprintf(strcat(['Testing  on indexes ', int2str(find(cdTestIndices')), '\n']));
        
        %testData = data(cdTestIndices,:);
        %testData = data(testIndices,:);
        %trainData = data(cdTrainIndices,:);
        cdTrainData = trainData(cdIndices,:);
        cdTrainClasses = trainClasses(cdIndices,:);
        %size(cdTrainData)
        %size(cdTrainClasses)
        %pause
        %if c == 13 && d == 15
        %    testData(:,1:10)
        %    trainData(:,1:10)
        %end
        
        %testClasses = classes(cdTestIndices);
        %trainClasses = classes(cdTrainIndices);
        
        % Train classifier
        %svmStruct = svmtrain(trainData,trainClasses,'Kernel_Function','rbf');
        %svmStruct = svmtrain(trainData,trainClasses,'Kernel_Function','quadratic');
        %kernel
        % TODO: mlp sometimes throw exception
        
        
        try
            %options = optimset('maxiter',1000,'display','iter');
            options = optimset('maxiter',1000);
            %tic;
            %svmStruct = svmtrain(trainData,trainClasses,'Kernel_Function',kernel,'quadprog_opts',options);
            svmStruct = svmtrain(cdTrainData,cdTrainClasses,'Kernel_Function',kernel,'quadprog_opts',options);
            %toc;
            %svmStruct = svmtrain(trainData,trainClasses,'Kernel_Function',kernel,'quadprog_opts',options,'showplot',true);
            %pause;
            %svmStruct.KernelFunction
            %svmStruct.SupportVectorIndices
            %bsxfun(@svmStruct.KernelFunction, cdTrainData(1,:),testData(1,:))
            %pause
            
        catch exception
            fprintf('Exception!!\n');
            size(cdTrainData)
            size(cdTrainClasses)
            %toc;
            %cdTrainData
            %cdTrainClasses
            %throw(exception);
            continue
        end
        % Test classifier
        %cdClassified = svmclassify(svmStruct,testData,'showplot',true);
        cdClassified = svmclassify(svmStruct,testData);
        %fprintf(strcat(['                    ',int2str(cdClassified'),'\n']));
        %pause
        %if c == 1
        %cdClassified
        %end
        
        % Place vote for one of the two classes, c or d
        %nClassified = size(cdClassified,1);
        %myVote = zeros(nClassified,nClasses);
        %myVote = zeros(size(votes));
        %for l=1:nClassified
        for l=1:size(testData,1)
            %myVote(l,cdClassified(l)) = 1;
            votes(l,cdClassified(l)) = votes(l,cdClassified(l)) + 1;
        end
        %myVote
        %votes(cdTestIndices,:) = votes(cdTestIndices,:) + myVote;
        %votes(testIndices,:) = votes(testIndices,:) + myVote;
        %votes(testIndices,:)
        %votes = votes + myVote
        %votes
        %if c == 1
        %votes(1:4,:)
        %end
        %pause
    end
end
%votes(1:30,:)
%votes(testIndices,:)
%pause

%fprintf('Voting...');
if nargin < 6
    %classified = evalvote(votes, testIndices);
    classified = evalvote(votes);
else
    %classified = evalvote(votes, testIndices, realClasses);
    classified = evalvote(votes, realClasses);
end
