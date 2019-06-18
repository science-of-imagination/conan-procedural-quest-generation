begin_version
3
end_version
begin_metric
1
end_metric
27
begin_variable
var0
-1
3
Atom at(aladdin, castle)
Atom at(aladdin, lamp)
Atom at(aladdin, mountain)
end_variable
begin_variable
var1
-1
3
Atom at(jafar, castle)
Atom at(jafar, lamp)
Atom at(jafar, mountain)
end_variable
begin_variable
var2
-1
3
Atom at(jasmine, castle)
Atom at(jasmine, lamp)
Atom at(jasmine, mountain)
end_variable
begin_variable
var3
-1
3
Atom at(you, castle)
Atom at(you, lamp)
Atom at(you, mountain)
end_variable
begin_variable
var4
-1
2
Atom captive(you, aladdin)
NegatedAtom captive(you, aladdin)
end_variable
begin_variable
var5
-1
2
Atom captive(you, jafar)
NegatedAtom captive(you, jafar)
end_variable
begin_variable
var6
-1
2
Atom captive(you, jasmine)
NegatedAtom captive(you, jasmine)
end_variable
begin_variable
var7
-1
2
Atom cooperative(aladdin)
NegatedAtom cooperative(aladdin)
end_variable
begin_variable
var8
-1
2
Atom cooperative(jafar)
NegatedAtom cooperative(jafar)
end_variable
begin_variable
var9
-1
2
Atom cooperative(jasmine)
NegatedAtom cooperative(jasmine)
end_variable
begin_variable
var10
-1
2
Atom defended(aladdin)
NegatedAtom defended(aladdin)
end_variable
begin_variable
var11
-1
2
Atom defended(jafar)
NegatedAtom defended(jafar)
end_variable
begin_variable
var12
-1
2
Atom defended(jasmine)
NegatedAtom defended(jasmine)
end_variable
begin_variable
var13
-1
2
Atom experimented(lamp)
NegatedAtom experimented(lamp)
end_variable
begin_variable
var14
-1
2
Atom explored(castle)
NegatedAtom explored(castle)
end_variable
begin_variable
var15
-1
2
Atom explored(lamp)
NegatedAtom explored(lamp)
end_variable
begin_variable
var16
-1
2
Atom explored(mountain)
NegatedAtom explored(mountain)
end_variable
begin_variable
var17
-1
2
Atom has(aladdin, lamp)
NegatedAtom has(aladdin, lamp)
end_variable
begin_variable
var18
-1
2
Atom has(aladdin, secret)
NegatedAtom has(aladdin, secret)
end_variable
begin_variable
var19
-1
2
Atom has(dragon, lamp)
NegatedAtom has(dragon, lamp)
end_variable
begin_variable
var20
-1
2
Atom has(jafar, lamp)
NegatedAtom has(jafar, lamp)
end_variable
begin_variable
var21
-1
2
Atom has(jasmine, lamp)
NegatedAtom has(jasmine, lamp)
end_variable
begin_variable
var22
-1
2
Atom has(jasmine, secret)
NegatedAtom has(jasmine, secret)
end_variable
begin_variable
var23
-1
2
Atom has(you, lamp)
NegatedAtom has(you, lamp)
end_variable
begin_variable
var24
-1
2
Atom has(you, secret)
NegatedAtom has(you, secret)
end_variable
begin_variable
var25
-1
2
Atom sneaky(you)
NegatedAtom sneaky(you)
end_variable
begin_variable
var26
-1
2
Atom used(lamp)
NegatedAtom used(lamp)
end_variable
4
begin_mutex_group
3
0 0
0 1
0 2
end_mutex_group
begin_mutex_group
3
1 0
1 1
1 2
end_mutex_group
begin_mutex_group
3
2 0
2 1
2 2
end_mutex_group
begin_mutex_group
3
3 0
3 1
3 2
end_mutex_group
begin_state
0
0
0
0
1
1
1
1
1
1
1
1
1
1
1
1
1
1
1
0
1
1
1
1
1
1
1
end_state
begin_goal
0
end_goal
106
begin_operator
capture you aladdin castle
2
0 0
3 0
1
0 4 -1 0
2
end_operator
begin_operator
capture you aladdin lamp
2
0 1
3 1
1
0 4 -1 0
2
end_operator
begin_operator
capture you aladdin mountain
2
0 2
3 2
1
0 4 -1 0
2
end_operator
begin_operator
capture you jafar castle
2
1 0
3 0
1
0 5 -1 0
2
end_operator
begin_operator
capture you jafar lamp
2
1 1
3 1
1
0 5 -1 0
2
end_operator
begin_operator
capture you jafar mountain
2
1 2
3 2
1
0 5 -1 0
2
end_operator
begin_operator
capture you jasmine castle
2
2 0
3 0
1
0 6 -1 0
2
end_operator
begin_operator
capture you jasmine lamp
2
2 1
3 1
1
0 6 -1 0
2
end_operator
begin_operator
capture you jasmine mountain
2
2 2
3 2
1
0 6 -1 0
2
end_operator
begin_operator
defend you aladdin castle
2
0 0
3 0
1
0 10 -1 0
1
end_operator
begin_operator
defend you aladdin lamp
2
0 1
3 1
1
0 10 -1 0
1
end_operator
begin_operator
defend you aladdin mountain
2
0 2
3 2
1
0 10 -1 0
1
end_operator
begin_operator
defend you jafar castle
2
1 0
3 0
1
0 11 -1 0
1
end_operator
begin_operator
defend you jafar lamp
2
1 1
3 1
1
0 11 -1 0
1
end_operator
begin_operator
defend you jafar mountain
2
1 2
3 2
1
0 11 -1 0
1
end_operator
begin_operator
defend you jasmine castle
2
2 0
3 0
1
0 12 -1 0
1
end_operator
begin_operator
defend you jasmine lamp
2
2 1
3 1
1
0 12 -1 0
1
end_operator
begin_operator
defend you jasmine mountain
2
2 2
3 2
1
0 12 -1 0
1
end_operator
begin_operator
escort you aladdin castle lamp
1
7 0
2
0 0 0 1
0 3 0 1
3
end_operator
begin_operator
escort you aladdin castle mountain
1
7 0
2
0 0 0 2
0 3 0 2
3
end_operator
begin_operator
escort you aladdin lamp castle
1
7 0
2
0 0 1 0
0 3 1 0
3
end_operator
begin_operator
escort you aladdin lamp mountain
1
7 0
2
0 0 1 2
0 3 1 2
3
end_operator
begin_operator
escort you aladdin mountain castle
1
7 0
2
0 0 2 0
0 3 2 0
3
end_operator
begin_operator
escort you aladdin mountain lamp
1
7 0
2
0 0 2 1
0 3 2 1
3
end_operator
begin_operator
escort you jafar castle lamp
1
8 0
2
0 1 0 1
0 3 0 1
3
end_operator
begin_operator
escort you jafar castle mountain
1
8 0
2
0 1 0 2
0 3 0 2
3
end_operator
begin_operator
escort you jafar lamp castle
1
8 0
2
0 1 1 0
0 3 1 0
3
end_operator
begin_operator
escort you jafar lamp mountain
1
8 0
2
0 1 1 2
0 3 1 2
3
end_operator
begin_operator
escort you jafar mountain castle
1
8 0
2
0 1 2 0
0 3 2 0
3
end_operator
begin_operator
escort you jafar mountain lamp
1
8 0
2
0 1 2 1
0 3 2 1
3
end_operator
begin_operator
escort you jasmine castle lamp
1
9 0
2
0 2 0 1
0 3 0 1
3
end_operator
begin_operator
escort you jasmine castle mountain
1
9 0
2
0 2 0 2
0 3 0 2
3
end_operator
begin_operator
escort you jasmine lamp castle
1
9 0
2
0 2 1 0
0 3 1 0
3
end_operator
begin_operator
escort you jasmine lamp mountain
1
9 0
2
0 2 1 2
0 3 1 2
3
end_operator
begin_operator
escort you jasmine mountain castle
1
9 0
2
0 2 2 0
0 3 2 0
3
end_operator
begin_operator
escort you jasmine mountain lamp
1
9 0
2
0 2 2 1
0 3 2 1
3
end_operator
begin_operator
experiment you lamp
1
23 0
1
0 13 -1 0
2
end_operator
begin_operator
explore you castle castle
1
3 0
1
0 14 -1 0
3
end_operator
begin_operator
explore you castle lamp
0
2
0 3 0 1
0 15 -1 0
3
end_operator
begin_operator
explore you castle mountain
0
2
0 3 0 2
0 16 -1 0
3
end_operator
begin_operator
explore you lamp castle
0
2
0 3 1 0
0 14 -1 0
3
end_operator
begin_operator
explore you lamp lamp
1
3 1
1
0 15 -1 0
3
end_operator
begin_operator
explore you lamp mountain
0
2
0 3 1 2
0 16 -1 0
3
end_operator
begin_operator
explore you mountain castle
0
2
0 3 2 0
0 14 -1 0
3
end_operator
begin_operator
explore you mountain lamp
0
2
0 3 2 1
0 15 -1 0
3
end_operator
begin_operator
explore you mountain mountain
1
3 2
1
0 16 -1 0
3
end_operator
begin_operator
giveto you aladdin lamp castle
2
0 0
3 0
3
0 7 -1 0
0 17 -1 0
0 23 0 1
2
end_operator
begin_operator
giveto you aladdin lamp lamp
2
0 1
3 1
3
0 7 -1 0
0 17 -1 0
0 23 0 1
2
end_operator
begin_operator
giveto you aladdin lamp mountain
2
0 2
3 2
3
0 7 -1 0
0 17 -1 0
0 23 0 1
2
end_operator
begin_operator
giveto you jafar lamp castle
2
1 0
3 0
3
0 8 -1 0
0 20 -1 0
0 23 0 1
2
end_operator
begin_operator
giveto you jafar lamp lamp
2
1 1
3 1
3
0 8 -1 0
0 20 -1 0
0 23 0 1
2
end_operator
begin_operator
giveto you jafar lamp mountain
2
1 2
3 2
3
0 8 -1 0
0 20 -1 0
0 23 0 1
2
end_operator
begin_operator
giveto you jasmine lamp castle
2
2 0
3 0
3
0 9 -1 0
0 21 -1 0
0 23 0 1
2
end_operator
begin_operator
giveto you jasmine lamp lamp
2
2 1
3 1
3
0 9 -1 0
0 21 -1 0
0 23 0 1
2
end_operator
begin_operator
giveto you jasmine lamp mountain
2
2 2
3 2
3
0 9 -1 0
0 21 -1 0
0 23 0 1
2
end_operator
begin_operator
listen you aladdin castle secret
3
0 0
3 0
18 0
1
0 24 -1 0
2
end_operator
begin_operator
listen you aladdin lamp secret
3
0 1
3 1
18 0
1
0 24 -1 0
2
end_operator
begin_operator
listen you aladdin mountain secret
3
0 2
3 2
18 0
1
0 24 -1 0
2
end_operator
begin_operator
listen you jafar castle secret
2
1 0
3 0
1
0 24 -1 0
2
end_operator
begin_operator
listen you jafar lamp secret
2
1 1
3 1
1
0 24 -1 0
2
end_operator
begin_operator
listen you jafar mountain secret
2
1 2
3 2
1
0 24 -1 0
2
end_operator
begin_operator
listen you jasmine castle secret
3
2 0
3 0
22 0
1
0 24 -1 0
2
end_operator
begin_operator
listen you jasmine lamp secret
3
2 1
3 1
22 0
1
0 24 -1 0
2
end_operator
begin_operator
listen you jasmine mountain secret
3
2 2
3 2
22 0
1
0 24 -1 0
2
end_operator
begin_operator
move you castle lamp
0
1
0 3 1 0
2
end_operator
begin_operator
move you castle mountain
0
1
0 3 2 0
2
end_operator
begin_operator
move you lamp castle
0
1
0 3 0 1
2
end_operator
begin_operator
move you lamp mountain
0
1
0 3 2 1
2
end_operator
begin_operator
move you mountain castle
0
1
0 3 0 2
2
end_operator
begin_operator
move you mountain lamp
0
1
0 3 1 2
2
end_operator
begin_operator
report you aladdin secret castle
3
0 0
3 0
24 0
1
0 18 -1 0
2
end_operator
begin_operator
report you aladdin secret lamp
3
0 1
3 1
24 0
1
0 18 -1 0
2
end_operator
begin_operator
report you aladdin secret mountain
3
0 2
3 2
24 0
1
0 18 -1 0
2
end_operator
begin_operator
report you jasmine secret castle
3
2 0
3 0
24 0
1
0 22 -1 0
2
end_operator
begin_operator
report you jasmine secret lamp
3
2 1
3 1
24 0
1
0 22 -1 0
2
end_operator
begin_operator
report you jasmine secret mountain
3
2 2
3 2
24 0
1
0 22 -1 0
2
end_operator
begin_operator
spy you aladdin castle secret
4
0 0
3 0
18 0
25 0
1
0 24 -1 0
2
end_operator
begin_operator
spy you aladdin lamp secret
4
0 1
3 1
18 0
25 0
1
0 24 -1 0
2
end_operator
begin_operator
spy you aladdin mountain secret
4
0 2
3 2
18 0
25 0
1
0 24 -1 0
2
end_operator
begin_operator
spy you jafar castle secret
3
1 0
3 0
25 0
1
0 24 -1 0
2
end_operator
begin_operator
spy you jafar lamp secret
3
1 1
3 1
25 0
1
0 24 -1 0
2
end_operator
begin_operator
spy you jafar mountain secret
3
1 2
3 2
25 0
1
0 24 -1 0
2
end_operator
begin_operator
spy you jasmine castle secret
4
2 0
3 0
22 0
25 0
1
0 24 -1 0
2
end_operator
begin_operator
spy you jasmine lamp secret
4
2 1
3 1
22 0
25 0
1
0 24 -1 0
2
end_operator
begin_operator
spy you jasmine mountain secret
4
2 2
3 2
22 0
25 0
1
0 24 -1 0
2
end_operator
begin_operator
stealth you
0
1
0 25 -1 0
2
end_operator
begin_operator
take you aladdin lamp castle
3
0 0
3 0
7 0
2
0 17 0 1
0 23 -1 0
2
end_operator
begin_operator
take you aladdin lamp castle
3
0 0
3 0
25 0
2
0 17 0 1
0 23 -1 0
2
end_operator
begin_operator
take you aladdin lamp lamp
3
0 1
3 1
7 0
2
0 17 0 1
0 23 -1 0
2
end_operator
begin_operator
take you aladdin lamp lamp
3
0 1
3 1
25 0
2
0 17 0 1
0 23 -1 0
2
end_operator
begin_operator
take you aladdin lamp mountain
3
0 2
3 2
7 0
2
0 17 0 1
0 23 -1 0
2
end_operator
begin_operator
take you aladdin lamp mountain
3
0 2
3 2
25 0
2
0 17 0 1
0 23 -1 0
2
end_operator
begin_operator
take you dragon lamp mountain
2
3 2
25 0
2
0 19 0 1
0 23 -1 0
2
end_operator
begin_operator
take you jafar lamp castle
3
1 0
3 0
8 0
2
0 20 0 1
0 23 -1 0
2
end_operator
begin_operator
take you jafar lamp castle
3
1 0
3 0
25 0
2
0 20 0 1
0 23 -1 0
2
end_operator
begin_operator
take you jafar lamp lamp
3
1 1
3 1
8 0
2
0 20 0 1
0 23 -1 0
2
end_operator
begin_operator
take you jafar lamp lamp
3
1 1
3 1
25 0
2
0 20 0 1
0 23 -1 0
2
end_operator
begin_operator
take you jafar lamp mountain
3
1 2
3 2
8 0
2
0 20 0 1
0 23 -1 0
2
end_operator
begin_operator
take you jafar lamp mountain
3
1 2
3 2
25 0
2
0 20 0 1
0 23 -1 0
2
end_operator
begin_operator
take you jasmine lamp castle
3
2 0
3 0
9 0
2
0 21 0 1
0 23 -1 0
2
end_operator
begin_operator
take you jasmine lamp castle
3
2 0
3 0
25 0
2
0 21 0 1
0 23 -1 0
2
end_operator
begin_operator
take you jasmine lamp lamp
3
2 1
3 1
9 0
2
0 21 0 1
0 23 -1 0
2
end_operator
begin_operator
take you jasmine lamp lamp
3
2 1
3 1
25 0
2
0 21 0 1
0 23 -1 0
2
end_operator
begin_operator
take you jasmine lamp mountain
3
2 2
3 2
9 0
2
0 21 0 1
0 23 -1 0
2
end_operator
begin_operator
take you jasmine lamp mountain
3
2 2
3 2
25 0
2
0 21 0 1
0 23 -1 0
2
end_operator
begin_operator
use you lamp
1
23 0
1
0 26 -1 0
2
end_operator
0
