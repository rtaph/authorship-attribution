function [newClasses, realClasses] = kmeanscluster (classes, nClasses, data, nClusters)

iterations = 5;

% The new classes for each original class
newClasses = zeros(size(classes));

% One row per real class, each row gives the sub-classes that have the
% class with the row-index as parent
realClasses = zeros(nClasses,nClusters);

for c=1:nClasses
    
    % ----- Usingkmeans function ----- %
    %c
    cIndices = c == classes;
    cData = data(cIndices,:);
    %opts = statset('display','final');
    [idx,ctrs] = kmeans(cData,nClusters,'replicates',iterations);
    %idx
    cNewClasses = (nClusters*c)+(idx-nClusters);
    newClasses(cIndices) = cNewClasses;
    %plot(cData(idx==1,1),cData(idx==1,2),'r.','MarkerSize',12)
    %hold on
    %plot(cData(idx==2,1),cData(idx==2,2),'b.','MarkerSize',12)
    %plot(ctrs(:,1),ctrs(:,2),'kx',...
    %    'MarkerSize',12,'LineWidth',2)
    %plot(ctrs(:,1),ctrs(:,2),'ko',...
    %    'MarkerSize',12,'LineWidth',2)
    %legend('Cluster 1','Cluster 2','Centroids',...
    %      'Location','NW')
    %pause
    
    realClasses(c,:) = unique(cNewClasses)';
    %for i=1:nRealClasses
    %    for j=1:nClusters
    %        realClasses(i,j) = (2*i)+j-2;
    %    end
    %end
    
    
    
end

%newClasses;
%pause