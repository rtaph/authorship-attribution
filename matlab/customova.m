function classified = customova(trainClasses, trainData, testData, nClasses, kernel, kerneloption)

c = 1;

trainClasses
allIndices = trainClasses ~= c;
ovaClasses = allIndices + 1 % c will be class 1, all will be class 2

size(ovaClasses)
options = optimset('maxiter',1000);
svmStruct = svmtrain(trainData,ovaClasses,'Kernel_Function',kernel,'quadprog_opts',options)
%svmStruct.KernelFunction
%svmStruct.SupportVectorIndices
%bsxfun(@svmStruct.KernelFunction, cdTrainData(1,:),testData(1,:))
%pause
%svmStruct.Alpha


% sum K(xi,x)*(alphai.*yi)
% firstPart = sum(bsxfun(@svmStruct.KernelFunction, testData,...
% svmStruct.SupportVectors(1,:)).*(svmStruct.Alpha(1)*-1), 2;
bla = bsxfun(@svmStruct.KernelFunction, testData(1,:), trainData(1,:))
blu = svmStruct.Alpha



% sum K(xi,s)*(alphai.*yi)

% Calculate distance
dNeg = firstPartNeg - 0.5*secondPart

% for c=1:nClasses
%     for d=(c+1):nClasses
%         %fprintf(strcat(['c,d: ', int2str(c), ',', int2str(d), '\n']));
%         %cIndices = classes == c;
%         %dIndices = classes == d;
%         cIndices = trainClasses == c;
%         dIndices = trainClasses == d;
%         cdIndices = logical(cIndices + dIndices);
%         %pause
%
%
%         %cdTestIndices = logical(testIndices .* cdIndices);
%         %cdTrainIndices = logical(trainIndices .* cdIndices);
%
%         %if c == 13 && d == 15
%         %    cdTestIndices(1:30,:)
%         %    cdTrainIndices(1:30,:)
%         %end
%
%         %fprintf(strcat(['Training on indexes ', int2str(find(cdTrainIndices')), '\n']));
%         %fprintf(strcat(['Testing  on indexes ', int2str(find(cdTestIndices')), '\n']));
%
%         %testData = data(cdTestIndices,:);
%         %testData = data(testIndices,:);
%         %trainData = data(cdTrainIndices,:);
%         cdTrainData = trainData(cdIndices,:);
%         cdTrainClasses = trainClasses(cdIndices,:);