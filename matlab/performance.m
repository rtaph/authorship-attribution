function [accuracy, classPrecisions, classRecalls, classF1s] = performance (classified, testClasses,nClasses)

correctClassified = classified == testClasses;

% accuracy
accuracy = (sum(correctClassified))/size(classified,1);
%accuracies(i) = a;

% precision and recall
classPrecisions = zeros(nClasses,1); % precision per class
classRecalls = zeros(nClasses,1); % recall per class

for c=1:nClasses
    totalClassifiedForC = classified == c;
    actualClassesForC = testClasses == c;
    correctClassifiedForC = correctClassified(totalClassifiedForC);
    
    precision = NaN;
    if sum(totalClassifiedForC) > 0
        precision = sum(correctClassifiedForC) / sum(totalClassifiedForC);
    %elseif sum(actualClassesForC) == 0
        % We cannot calculate precision if there are no instances of a
        % given class in the test set and none was assigned.
    %    precision = NaN;
    end
    classPrecisions(c) = precision;
    
    % We cannot calculate recall if there are no instances of a given
    % class in the test set.
    recall = NaN;
    if sum(actualClassesForC) > 0
        recall = sum(correctClassifiedForC) / sum(actualClassesForC);
    end
    classRecalls(c) = recall;
    
end

classF1s = (2*classPrecisions.*classRecalls) ./ (classPrecisions + classRecalls);
%classF1s = zeros(nClasses,1);
%classF1s = (2*classPrecisions*classRecalls) / (classPrecisions + classRecalls);