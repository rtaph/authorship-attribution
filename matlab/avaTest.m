fprintf('\n\n******************* NEW AVA TEST *********************\n');
fprintf('******************* NEW AVA TEST *********************\n');
fprintf('******************* NEW AVA TEST *********************\n\n');

voteReal = false;

fprintf('AVA, linear\n');
a = [];
%a(1) = aa_classify(true,'AVA','linear',NaN,'/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/set30_10_1_half');
a(1) = aa_classify(false,voteReal,'AVA','linear');
a(2) = aa_classify(false,voteReal,'AVA','linear');
a(3) = aa_classify(false,voteReal,'AVA','linear');
a(4) = aa_classify(false,voteReal,'AVA','linear');
a(5) = aa_classify(false,voteReal,'AVA','linear');
mean(a)

fprintf('AVA, quadratic\n');
a = [];
a(1) = aa_classify(false,voteReal,'AVA','quadratic');
a(2) = aa_classify(false,voteReal,'AVA','quadratic');
a(3) = aa_classify(false,voteReal,'AVA','quadratic');
a(4) = aa_classify(false,voteReal,'AVA','quadratic');
a(5) = aa_classify(false,voteReal,'AVA','quadratic');
mean(a)

fprintf('AVA, polynomial\n');
a = [];
a(1) = aa_classify(false,voteReal,'AVA','polynomial');
a(2) = aa_classify(false,voteReal,'AVA','polynomial');
a(3) = aa_classify(false,voteReal,'AVA','polynomial');
a(4) = aa_classify(false,voteReal,'AVA','polynomial');
a(5) = aa_classify(false,voteReal,'AVA','polynomial');
mean(a)

fprintf('AVA, rbf\n');
a = [];
a(1) = aa_classify(false,voteReal,'AVA','rbf');
a(2) = aa_classify(false,voteReal,'AVA','rbf');
a(3) = aa_classify(false,voteReal,'AVA','rbf');
a(4) = aa_classify(false,voteReal,'AVA','rbf');
a(5) = aa_classify(false,voteReal,'AVA','rbf');
mean(a)

fprintf('AVA, mlp\n');
a = [];
a(1) = aa_classify(false,voteReal,'AVA','mlp');
a(2) = aa_classify(false,voteReal,'AVA','mlp');
a(3) = aa_classify(false,voteReal,'AVA','mlp');
a(4) = aa_classify(false,voteReal,'AVA','mlp');
a(5) = aa_classify(false,voteReal,'AVA','mlp');
mean(a)