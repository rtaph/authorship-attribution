function classified = classifyava(data, classes, testIndices, trainIndices, kernel)
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
% classified: A vector of length sum(testIndices), with a the class of each
% text in the test-set.

nClasses = max(classes);

% votes for a text belonging to a class
votes = zeros(size(data,1),nClasses);

for c=1:nClasses
    for d=(c+1):nClasses
        fprintf(strcat(['c,d: ', int2str(c), ',', int2str(d), '\n']));
        cIndices = classes == c;
        dIndices = classes == d;
        cdIndices = cIndices + dIndices;
        
        cdTestIndices = logical(testIndices .* cdIndices)
        cdTrainIndices = logical(trainIndices .* cdIndices);
        
        testData = data(cdTestIndices,:);
        trainData = data(cdTrainIndices,:);
        
        %testClasses = classes(cdTestIndices);
        trainClasses = classes(cdTrainIndices);
        
        % Train classifier
        %svmStruct = svmtrain(trainData,trainClasses,'Kernel_Function','rbf');
        %svmStruct = svmtrain(trainData,trainClasses,'Kernel_Function','quadratic');
        %kernel
        % TODO: mlp sometimes throw exception
        
        try
            svmStruct = svmtrain(trainData,trainClasses,'Kernel_Function',kernel);
        catch
            %fprintf('Error\n');
            continue
        end
        % Test classifier
        cdClassified = svmclassify(svmStruct,testData)
        %pause
        
        % Place vote for one of the two classes, c and d
        nClassified = size(cdClassified,1);
        myVote = zeros(nClassified,nClasses);
        for l=1:nClassified
            myVote(l,cdClassified(l)) = 1;
        end
        %myVote
        votes(cdTestIndices,:) = votes(cdTestIndices,:) + myVote;
        %votes(testIndices,:)
        
        
    end
end

classified = evalvote(votes, testIndices);
