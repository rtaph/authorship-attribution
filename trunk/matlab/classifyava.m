function classified = classifyava(trainData, trainClasses, testData, nClasses, kernel, realClasses, multi)
% SVM multiclass classification using All vs. All.

% Max. no. of iterations
iters = 1000;

% votes for a text of the test set belonging to a class
votes = zeros(size(testData,1),nClasses);

if multi
    
    parfor c=1:nClasses
        fprintf(strcat(['c: ', int2str(c), '\n']));
        for d=(c+1):nClasses
            cIndices = trainClasses == c;
            dIndices = trainClasses == d;
            cdIndices = logical(cIndices + dIndices);
            cdTrainData = trainData(cdIndices,:);
            cdTrainClasses = trainClasses(cdIndices,:);
            try
                options = optimset('maxiter',iters);
                svmStruct = svmtrain(cdTrainData,cdTrainClasses,'Kernel_Function',kernel,'quadprog_opts',options);
            catch exception
                fprintf('Exception!!\n');
                size(cdTrainData)
                size(cdTrainClasses)
                continue
            end
            cdClassified = svmclassify(svmStruct,testData);
            myVotes = zeros(size(testData,1),nClasses);
            for l=1:size(testData,1)
                myVotes(l,cdClassified(l)) = myVotes(l,cdClassified(l)) + 1;
            end
            votes = votes + myVotes;
        end
    end
    
    
else % Sequential version
    
    
    for c=1:nClasses
        fprintf(strcat(['c: ', int2str(c), '\n']));
        for d=(c+1):nClasses
            cIndices = trainClasses == c;
            dIndices = trainClasses == d;
            cdIndices = logical(cIndices + dIndices);
            
            cdTrainData = trainData(cdIndices,:);
            cdTrainClasses = trainClasses(cdIndices,:);

            try
                options = optimset('maxiter',iters);
                svmStruct = svmtrain(cdTrainData,cdTrainClasses,'Kernel_Function',kernel,'quadprog_opts',options);

            catch exception
                fprintf('Exception!!\n');
                c
                d
                size(cdTrainData)
                size(cdTrainClasses)
                continue
            end
            
            % Test classifier
            cdClassified = svmclassify(svmStruct,testData);

            % Place vote for one of the two classes, c or d
            myVotes = zeros(size(testData,1),nClasses);
            for l=1:size(testData,1)
                myVotes(l,cdClassified(l)) = myVotes(l,cdClassified(l)) + 1;
            end
            votes = votes + myVotes;
        end
    end
end

if isempty(realClasses)
    fprintf('Normal voting..\n');
    classified = evalvote(votes);
else
    fprintf('Voting for real classes..\n');
    classified = evalvote(votes, realClasses);
end
