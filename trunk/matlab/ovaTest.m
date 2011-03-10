fprintf('\n\n******************* NEW OVA TEST *********************\n');
fprintf('******************* NEW OVA TEST *********************\n');
fprintf('******************* NEW OVA TEST *********************\n\n');

fprintf('OVA, poly\n');
a = [];
%a(1) = aa_classify(true,'OVA','poly',3,'/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/set30_10_1/');
a(1) = aa_classify(false,false,'OVA','poly',3);
a(2) = aa_classify(false,false,'OVA','poly',3);
a(3) = aa_classify(false,false,'OVA','poly',3);
a(4) = aa_classify(false,false,'OVA','poly',3);
a(5) = aa_classify(false,false,'OVA','poly',3);
avg = mean(a)
stDev = std(a)

fprintf('OVA, polyhomog\n');
a = [];
a(1) = aa_classify(false,false,'OVA','polyhomog',3);
a(2) = aa_classify(false,false,'OVA','polyhomog',3);
a(3) = aa_classify(false,false,'OVA','polyhomog',3);
a(4) = aa_classify(false,false,'OVA','polyhomog',3);
a(5) = aa_classify(false,false,'OVA','polyhomog',3);
avg = mean(a)
stDev = std(a)

fprintf('OVA, gaussian\n');
a = [];
a(1) = aa_classify(false,false,'OVA','gaussian',2);
a(2) = aa_classify(false,false,'OVA','gaussian',2);
a(3) = aa_classify(false,false,'OVA','gaussian',2);
a(4) = aa_classify(false,false,'OVA','gaussian',2);
a(5) = aa_classify(false,false,'OVA','gaussian',2);
avg = mean(a)
stDev = std(a)

fprintf('OVA, htrbf\n');
a = [];
a(1) = aa_classify(false,false,'OVA','htrbf',[1,-1]);
a(2) = aa_classify(false,false,'OVA','htrbf',[1,-1]);
a(3) = aa_classify(false,false,'OVA','htrbf',[1,-1]);
a(4) = aa_classify(false,false,'OVA','htrbf',[1,-1]);
a(5) = aa_classify(false,false,'OVA','htrbf',[1,-1]);
avg = mean(a)
stDev = std(a)

% NOT WORKING AS INPUT DESCRIPTIONS NOT GIVEN!

%fprintf('OVA, wavelet\n');
%a = [];
%a(1) = aa_classify(false,false,'OVA','wavelet');
% a(2) = aa_classify(false,false,'OVA','wavelet');
% a(3) = aa_classify(false,false,'OVA','wavelet');
% a(4) = aa_classify(false,false,'OVA','wavelet');
% a(5) = aa_classify(false,false,'OVA','wavelet');
% avg = mean(a)
% stDev = std(a)

%fprintf('OVA, frame\n');
%a = [];
%a(1) = aa_classify(false,false,'OVA','frame','sin');
% a(2) = aa_classify(false,false,'OVA','wavelet');
% a(3) = aa_classify(false,false,'OVA','wavelet');
% a(4) = aa_classify(false,false,'OVA','wavelet');
% a(5) = aa_classify(false,false,'OVA','wavelet');
% avg = mean(a)
% stDev = std(a)