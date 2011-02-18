function test_suite = testMeanWithNan
initTestSuite;

function test1
a = [1,1,1;2,2,2;3,3,3];
m = meanwithnan(a);
assertEqual(m,[1;2;3]);

function test2
a = [1,2,3;1,2,3;1,2,3];
m = meanwithnan(a);
assertEqual(m,[2;2;2]);

function test3
a = [1,1,1];
m = meanwithnan(a);
assertEqual(m,[1]);

function test4
a = [1,1,NaN;2,2,2;3,3,3];
m = meanwithnan(a);
assertEqual(m,[1;2;3]);

function test5
a = [1,1,1;2,NaN,5;3,3,3];
m = meanwithnan(a);
assertEqual(m,[1;3.5;3]);

function test6
a = [1,1,1;2,2,2;NaN,44,6];
m = meanwithnan(a);
assertEqual(m,[1;2;25]);