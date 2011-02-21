fprintf('OVA, poly\n');
a = [];
%a(1) = aa_classify(true,'OVA','poly',3,'/Users/epb/Documents/uni/kandidat/speciale/data/blog_corpus/set30_10_1/');
a(1) = aa_classify(false,'OVA','poly',3);
a(2) = aa_classify(false,'OVA','poly',3);
a(3) = aa_classify(false,'OVA','poly',3);
a(4) = aa_classify(false,'OVA','poly',3);
a(5) = aa_classify(false,'OVA','poly',3);
mean(a)

fprintf('OVA, polyhomog\n');
a = [];
a(1) = aa_classify(false,'OVA','polyhomog',3);
a(2) = aa_classify(false,'OVA','polyhomog',3);
a(3) = aa_classify(false,'OVA','polyhomog',3);
a(4) = aa_classify(false,'OVA','polyhomog',3);
a(5) = aa_classify(false,'OVA','polyhomog',3);
mean(a)

fprintf('OVA, gaussian\n');
a = [];
a(1) = aa_classify(false,'OVA','gaussian',2);
a(2) = aa_classify(false,'OVA','gaussian',2);
a(3) = aa_classify(false,'OVA','gaussian',2);
a(4) = aa_classify(false,'OVA','gaussian',2);
a(5) = aa_classify(false,'OVA','gaussian',2);
mean(a)

fprintf('OVA, htrbf\n');
a = [];
a(1) = aa_classify(false,'OVA','htrbf',[1,-1]);
a(2) = aa_classify(false,'OVA','htrbf',[1,-1]);
a(3) = aa_classify(false,'OVA','htrbf',[1,-1]);
a(4) = aa_classify(false,'OVA','htrbf',[1,-1]);
a(5) = aa_classify(false,'OVA','htrbf',[1,-1]);
mean(a)

% fprintf('OVA, wavelet\n');
% a = [];
% a(1) = aa_classify(false,'OVA','wavelet');
% a(2) = aa_classify(false,'OVA','wavelet');
% a(3) = aa_classify(false,'OVA','wavelet');
% a(4) = aa_classify(false,'OVA','wavelet');
% a(5) = aa_classify(false,'OVA','wavelet');
% mean(a)