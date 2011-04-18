function means = meanwithnan(samples,dim)
% Calculate row-wise or column-wise mean of a matrix,
% taking into account that some values in matrix may be NaN.

[n, k] = size(samples);

if sum(sum(isnan(samples))) == 0
    means = mean(samples,dim); % no NaNs
end

if dim == 1
    means = zeros(1,k);
    for i=1:k
        c = 0;
        s = 0;
        for j=1:n
            if ~isnan(samples(j,i))
                c = c + 1;
                s = s + samples(j,i);
            end
        end
        means(1,i) = s / c;
    end
elseif dim == 2
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