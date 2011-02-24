function classified = evalvote (votes, testIndices, subClasses)
% Evaluate vote. The highest vote to achieve is nClasses-1, as this
% is the number of pairs each class participates in.
% 
% subClasses: A matrix of size r x s, where each of the r rows represent a
% real class and the s values in a row determine which sub-classes this
% real class contains.

votes = votes(testIndices,:);
classified = zeros(sum(testIndices),1);
for v=1:size(votes,1)
    
    
    %if nargin > 2 % sum of votes for subclasses
    
%     if nargin > 2 % The subclass with highest vote gives the win to real class
%         
%         sums = zeros(1,size(subClasses,1));
%         for n=1:size(subClasses,1)
%             
%             n;
%             s = 0;
%             sc = subClasses(n,:);
%             for r=1:size(sc,2)
%                 s = s + votes(v,sc(r));
%             end
%             sums(n) = s;
%         end
%         
%         %votes(v,:)
%         voteRow = sums;
%         
%         
%     else % normal vote
        
        voteRow = votes(v,:);
        
%     end
    
    [high, class] = max(voteRow);
    
    % Make sure we only have _one_ winner
    if sum(ismember(voteRow,high)) == 1
        
        % If the subClasses argument is given, the sub-class that wins the
        % vote, will give its victory to its parent
        if nargin > 2
            for n=1:size(subClasses,1)
                sc = subClasses(n,:);
                if sum(ismember(sc,class)) == 1
                    classified(v) = n;
                end
            end
        else
            classified(v) = class; % normal vote
        end
        
    end
end