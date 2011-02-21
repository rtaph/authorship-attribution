function test_suite = testEvalVote
initTestSuite;

function test1
v = [0,0,0;0,0,0;0,0,0;0,0,0;0,0,0;0,0,0;0,0,0;0,0,0;0,0,0];
t = logical([1;0;1;0;0;0;0;0;0]);
c = evalvote(v, t);
assertEqual(c,[0;0]);

function test2
v = [1,0,0;0,0,0;0,1,0;0,0,0;0,0,0;0,0,0;0,0,0;0,0,0;0,0,0];
t = logical([1;0;1;0;0;0;0;0;0]);
c = evalvote(v, t);
assertEqual(c,[1;2]);

function test3
v = [0,0,0;1,2,0;0,0,0;0,5,0;0,0,5;0,7,0;0,2,0;0,0,0;0,0,0];
t = logical([1;0;1;0;0;0;0;0;0]);
c = evalvote(v, t);
assertEqual(c,[0;0]);

function test4
v = [0,0,2;0,0,0;1,0,1;0,0,0;0,0,0;0,0,0;0,0,0;0,0,0;0,0,0];
t = logical([1;0;1;0;0;0;0;0;0]);
c = evalvote(v, t);
assertEqual(c,[3;0]);

function test5
v = [2,2,2;0,0,0;1,0,1;0,0,0;0,0,0;0,0,0;0,0,0;0,0,0;0,0,0];
t = logical([1;0;1;0;0;0;0;0;0]);
c = evalvote(v, t);
assertEqual(c,[0;0]);

function test6
v = [0,1,2;0,0,0;1,0,1;0,2,0;0,0,0;0,0,0;0,0,0;0,0,0;0,0,0];
t = logical([1;0;1;0;0;0;0;0;0]);
c = evalvote(v, t);
assertEqual(c,[3;0]);