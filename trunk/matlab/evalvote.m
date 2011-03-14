function classified = evalvote (votes, subClasses)
% Count votes.
% 
% subClasses: A matrix of size r x s, where each of the r rows represent a
% real class and the s values in a row determine which sub-classes this
% real class contains. If the subClasses argument is given, the sub-class
% that wins the vote, will give its victory to its parent.

classified = zeros(size(votes,1),1);
for v=1:size(votes,1)
        
    voteRow = votes(v,:);

    % Find highest vote
    [high, class] = max(voteRow);
    
    % Make sure we only have _one_ winner
    if sum(ismember(voteRow,high)) == 1
        
        % Give vote to parent class if subClasses argument was given
        if nargin > 1
            for n=1:size(subClasses,1)
                sc = subClasses(n,:);
                if sum(ismember(sc,class)) == 1
                    classified(v) = n;
                end
            end
        % Normal vote
        else
            classified(v) = class;
        end
    end
end