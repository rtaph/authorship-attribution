function means = meanwithnan(samples)
% Calculate row-wise mean of a matrix, taking into account that some values
% in matrix may be NaN.

[n, k] = size(samples);

if sum(sum(isnan(samples))) == 0
    means = mean(samples,2);
else
    means = zeros(n,1);
    for i=1:n
        c = 0;
        s = 0;
        for j=1:k
            if ~isnan(samples(i,j))
                c = c + 1;
                s = s + samples(i,j);
            end
        end
        means(i) = s / c;
    end
end