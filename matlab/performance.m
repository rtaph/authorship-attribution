function [accuracy, classPrecisions, classRecalls, classF1s] = performance (classified, testClasses,nClasses)
% Calculate performance measures

correctClassified = classified == testClasses;

% accuracy
accuracy = (sum(correctClassified))/size(classified,1);

% precision and recall per class
classPrecisions = zeros(nClasses,1);
classRecalls = zeros(nClasses,1);

for c=1:nClasses
    totalClassifiedForC = classified == c;
    actualClassesForC = testClasses == c;
    correctClassifiedForC = correctClassified(totalClassifiedForC);
    
    precision = 1;
    % We cannot calculate precision if there are no instances classified
    % to the given class
    if sum(totalClassifiedForC) > 0
        precision = sum(correctClassifiedForC) / sum(totalClassifiedForC);
    end
    classPrecisions(c) = precision;
    
    % We cannot calculate recall if there are no instances of a given
    % class in the test set.
    recall = 1;
    if sum(actualClassesForC) > 0
        recall = sum(correctClassifiedForC) / sum(actualClassesForC);
    end
    classRecalls(c) = recall;
    
end

% We need to calculate F1 in a loop because precision and recall may be
% both 0 for a class and this should give F1=0 not F1=NaN
classF1s = zeros(nClasses,1);
for c=1:nClasses
    p = classPrecisions(c);
    r = classRecalls(c);
    if ~(p == 0 && r == 0)
        classF1s(c) = (2*p*r) / (p+r);
    end
end