function classified = classifyova(trainClasses, trainData, testData, nClasses, kernel, kerneloption)
% SVM multiclass classification using One vs. All.

classified = zeros(size(testData,1),1);

c = 1000;
lambda = 1e-7;

size(trainData)
size(trainClasses)
[xsup,w,b,nbsv] = svmmulticlassoneagainstall(trainData,trainClasses,nClasses,c,lambda,kernel,kerneloption,false);

for t=1:size(testData,1)
    d = testData(t,:);
    classified(t) = svmmultival(d,xsup,w,b,nbsv,kernel,kerneloption);
end