function classified = evalvote (votes, testIndices)
% Evaluate vote. The highest vote to achieve is nClasses-1, as this
% is the number of pairs each class participates in.

votes = votes(testIndices,:);
classified = zeros(sum(testIndices),1);
for v=1:size(votes,1)
    [high, class] = max(votes(v,:));
    
    % Make sure we only have _one_ winner
    if sum(ismember(votes(v,:),high)) == 1
        classified(v) = class;
    end
end