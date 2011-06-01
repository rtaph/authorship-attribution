function test_suite = testEvalVote
initTestSuite;

function test1
v = [0,0,0];
c = evalvote(v);
assertEqual(c,[0]);

function test2
v = [1,0,0];
c = evalvote(v);
assertEqual(c,[1]);

function test3
v = [1,2,0];
c = evalvote(v);
assertEqual(c,[2]);

function test4
v = [1,2,2];
c = evalvote(v);
assertEqual(c,[0]);

function test5
v = [0,0,0;0,0,0];
c = evalvote(v);
assertEqual(c,[0;0]);

function test6
v = [1,0,0;0,0,1];
c = evalvote(v);
assertEqual(c,[1;3]);

function test7
v = [1,2,0;0,2,1];
c = evalvote(v);
assertEqual(c,[2;2]);

function test8
s = [1,2,3;4,5,6];
v = [0,0,0,0,0,0];
c = evalvote(v, s);
assertEqual(c,[0]);

function test9
s = [1,2,3;4,5,6];
v = [0,0,1,0,0,0];
c = evalvote(v, s);
assertEqual(c,[1]);

function test10
s = [1,2,3;4,5,6];
v = [0,0,1,0,2,0];
c = evalvote(v, s);
assertEqual(c,[2]);

function test11
s = [1,2,3;4,5,6];
v = [4,0,1,0,1,0;1,2,3,3,2,3];
c = evalvote(v, s);
assertEqual(c,[1;0]);

function test12
s = [1,2,3;4,5,6];
v = [4,0,1,0,1,0;1,2,4,0,2,3];
c = evalvote(v, s);
assertEqual(c,[1;1]);
