function classified = classifyova(trainClasses, trainData, testData, nClasses, kernel, kerneloption)
% SVM multiclass classification using One vs. All.
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

%classes
%testIndices
%trainIndices

%nClasses = max(classes);

%classified = zeros(sum(testIndices),1);
classified = zeros(size(testData,1),1);

c = 1000;
lambda = 1e-7;
%kerneloption= 2;
%kernel='gaussian';

%testData = data(testIndices,:);
%trainData = data(trainIndices,:);
%trainClasses = classes(trainIndices);
size(trainData);
size(trainClasses);
nClasses;
[xsup,w,b,nbsv] = svmmulticlassoneagainstall(trainData,trainClasses,nClasses,c,lambda,kernel,kerneloption,false);

for t=1:size(testData,1)
    d = testData(t,:);
    classified(t) = svmmultival(d,xsup,w,b,nbsv,kernel,kerneloption);
end



%bla = [1,2,3;4,5,6;4,5,6;7,7,7;8,8,8;12,1,1]
%blu = [1;2;2;3;3;1]
%[xsup,w,b,nbsv] = svmmulticlassoneagainstall(bla,blu,3,c,lambda,kernel,kerneloption,false)

%svmmultival([4,5,6],xsup,w,b,nbsv,kernel,kerneloption)

%[a,b,c,d] = svmmulticlassoneagainstall(bla,blu,3,c,lambda,kernel,kerneloption,false)
%svmmultival([4,5,6],a,b,c,d,'gaussian',2)