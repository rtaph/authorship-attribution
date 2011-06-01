function test_suite = testPerformanceFunc
initTestSuite;

function test1
c = [1;1;1;1;2;2;2;2];
tc = [1;1;1;1;2;2;2;2];
[a, cp, cr, cf] = performance(c,tc,2);
assertEqual(a,1);
assertEqual(cp,[1;1]);
assertEqual(cr,[1;1]);
assertEqual(cf,[1;1]);

function test2
c = [1;2;1;2;1;2;1;2];
tc = [1;2;1;2;1;2;1;2];
[a, cp, cr, cf] = performance(c,tc,2);
assertEqual(a,1);
assertEqual(cp,[1;1]);
assertEqual(cr,[1;1]);
assertEqual(cf,[1;1]);

function test3
c = [1;1;1;2;2;2;3;3;3];
tc = [1;1;1;2;2;2;3;3;3];
[a, cp, cr, cf] = performance(c,tc,3);
assertEqual(a,1);
assertEqual(cp,[1;1;1]);
assertEqual(cr,[1;1;1]);
assertEqual(cf,[1;1;1]);

function test4
c = [1;2;3;1;2;3;1;2;3];
tc = [1;2;3;1;2;3;1;2;3];
[a, cp, cr, cf] = performance(c,tc,3);
assertEqual(a,1);
assertEqual(cp,[1;1;1]);
assertEqual(cr,[1;1;1]);
assertEqual(cf,[1;1;1]);

function test5
c = [0;1;0;2;0;2;0;3;0];
tc = [1;1;1;2;2;2;3;3;3];
[a, cp, cr, cf] = performance(c,tc,3);
assertEqual(a,4.0/9);
assertEqual(cp,[1;1;1]);
assertEqual(cr,[1.0/3;2.0/3;1.0/3]);
assertEqual(cf,[(2*1*1.0/3)/(1+(1.0/3));(2*1*2.0/3)/(1+(2.0/3));(2*1*1.0/3)/(1+(1.0/3))]);

function test6
c = [0;0;0;0;0;0;0;0;0];
tc = [1;1;1;2;2;2;3;3;3];
[a, cp, cr, cf] = performance(c,tc,3);
assertEqual(a,0);
assertEqual(cp,[1;1;1]);
assertEqual(cr,[0;0;0]);
assertEqual(cf,[0;0;0]);

function test7
c = [1;1;1;1;1;1;1;1;1];
tc = [1;1;1;2;2;2;3;3;3];
[a, cp, cr, cf] = performance(c,tc,3);
assertEqual(a,3.0/9);
assertEqual(cp,[3.0/9;1;1]);
assertEqual(cr,[1;0;0]);
assertEqual(cf,[(2*(3.0/9)*1)/((3.0/9)+1);0;0]);

function test8
c = [1;1;1;1;2;2;2;2;2];
tc = [1;1;1;2;2;2;2;2;2];
[a, cp, cr, cf] = performance(c,tc,3);
assertEqual(a,8.0/9);
assertEqual(cp,[3.0/4;1;1]);
assertEqual(cr,[1;5.0/6;1]);
assertEqual(cf,[(2*(3.0/4)*1)/((3.0/4)+1);(2*(5.0/6)*1)/((5.0/6)+1);1]);

function test9
c = [1;2;1;1;1;1;3;1;3];
tc = [1;1;1;2;2;2;2;2;2];
[a, cp, cr, cf] = performance(c,tc,3);
assertEqual(a,2.0/9);
assertEqual(cp,[2.0/6;0;0]);
assertEqual(cr,[2.0/3;0;1]);
assertEqual(cf,[(2*(2.0/6)*(2.0/3))/((2.0/6)+(2.0/3));0;0]);
