function votes = classifyava(data, classes, testIndices, trainIndices)
% SVM multiclass classification using All vs. All.
%
% Input
% -----
% data: A matrix (n x m) of data. The n rows each represent a text and the
% m columns represent the features of each text.
% classes: A vector (n x 1) that determines which of q classes (integers
% starting at 1) each text of the data set belongs to.
% testIndices: A vector (n x 1) of logical indices of the classes used for
% test.
% trainIndices: A vector (n x 1) of logical indices of the classes used for
% training.
%
% Output
% ------
% votes: A matrix (n x q) of votes of which class each text of the data
% belongs to. Each row corresponds to a text, each column, i contains the
% no. of votes for the text belonging to class i. Only texts used for test
% will have votes larger than 0.

nClasses = max(classes);

% votes for a text belonging to a class
votes = zeros(size(data,1),nClasses);
    
for c=1:nClasses
    for d=(c+1):nClasses
        
        cIndices = classes == c;
        dIndices = classes == d;
        cdIndices = cIndices + dIndices;
        
        cdTestIndices = logical(testIndices .* cdIndices);
        cdTrainIndices = logical(trainIndices .* cdIndices);
        
        testData = data(cdTestIndices,:);
        trainData = data(cdTrainIndices,:);
        
        %testClasses = classes(cdTestIndices);
        trainClasses = classes(cdTrainIndices);
        
        % Train classifier
        svmStruct = svmtrain(trainData,trainClasses);
        
        % Test classifier
        cdClassified = svmclassify(svmStruct,testData);
        
        % Place vote for one of the two classes, c and d
        nClassified = size(cdClassified,1);
        myVote = zeros(nClassified,nClasses);
        for l=1:nClassified
            myVote(l,cdClassified(l)) = 1;
        end
        votes(cdTestIndices,:) = votes(cdTestIndices,:) + myVote;
        
    end
end