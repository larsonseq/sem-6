% facts

male(anthony).
male(gilbert).
male(glanson).
male(richard).
male(rolwin).
male(nicholas).
male(andrew).
male(anish).
male(ajith).
male(cyril).
male(praveen).
male(allwyn).
male(norbert).
male(dennis).
male(pravin).
male(vincent).
male(naveen).
male(pravin).
male(larson).
male(lawrence).

female(paulineD).
female(joyce).
female(glenisha).
female(laveena).
female(rishael).
female(severine).
female(lilly).
female(priya).
female(eva).
female(paulineS).
female(violet).
female(mabel).
female(dorris).
female(priona).
female(diana).
female(dolin).
female(cecilia).
female(lavina).
female(cicilia).
female(sharon).

parent(anthony, joyce).
parent(paulineD, joyce).
parent(anthony, laveena).
parent(paulineD, laveena).
parent(joyce, glanson).
parent(joyce, glenisha).
parent(gilbert, glanson).
parent(gilbert, glenisha).
parent(anthony, laveena).
parent(paulineD, laveena).
parent(richard, rolwin).
parent(richard, rishael).
parent(laveena, rolwin).
parent(laveena, rishael).
parent(nicholas, lilly).
parent(severine, lilly).
parent(nicholas, paulineS).
parent(severine, paulineS).
parent(nicholas, dennis).
parent(severine, dennis).
parent(nicholas, cecilia).
parent(severine, cecilia).
parent(andrew, anish).
parent(andrew, priya).
parent(lilly, anish).
parent(lilly, priya).
parent(cyril, praveen).
parent(paulineS, praveen).
parent(cyril, norbert).
parent(paulineS, norbert).
parent(cyril, allwyn).
parent(paulineS, allwyn).
parent(cyril, violet).
parent(paulineS, violet).
parent(dennis, dolin).
parent(dennis, dorris).
parent(dennis, diana).
parent(mabel, dorris).
parent(mabel, diana).
parent(mabel, dolin).
parent(vincent, lavina).
parent(cecilia, lavina).
parent(cecilia, naveen).
parent(vincent, naveen).
parent(anthony, cicilia).
parent(paulineD, cicilia).
parent(nicholas, lawrence).
parent(severine, lawrence).
parent(lawrence, larson).
parent(lawrence, sharon).
parent(cicilia, sharon).
parent(cicilia, larson). 
parent(priya, eva).
parent(ajith, eva).
parent(pravin, priona).
parent(dorris, priona).

% Rules
father(A, B) :- parent(A, B), male(A).
mother(A, B) :- parent(A, B), female(A).

% since parents can father or mother, the tree will have multiple paths, so one node will be printed twice
% mentioning parent as mother or father can fix this (Kind of!).  
% otherwise, use member and set_of functions
sibling(A, B) :- parent(X, A), parent(X, B), A \= B, male(X).

brother(A, B) :- sibling(A, B), male(A).
sister(A, B) :- sibling(A, B), female(A).

grandparent(A, B) :- parent(A, X), parent(X, B).
grandfather(A, B) :- grandparent(A, B), male(A).
grandmother(A, B) :- grandparent(A, B), female(A).

maternalgrandparent(A, B) :- parent(A, X), parent(X, B), female(X).
paternalgrandparent(A, B) :- parent(A, X), parent(X, B), male(X).

uncle(A, B) :- parent(X, B), sibling(A, X), male(A), parent(Y, A), parent(Y, X), male(Y). 
uncle(A, B) :- parent(X, B), sibling(Y, X), parent(Y, Z), parent(A, Z), male(A), Y \= A. 
aunt(A, B) :- parent(X, B), sibling(A, X), female(A), parent(Y, A), parent(Y, X), male(Y).
aunt(A, B) :- parent(X, B), sibling(Y, X), parent(Y, Z), parent(A, Z), female(A), Y \= A.

son(A, B) :- parent(B, A), male(A).
daughter(A, B) :- parent(B, A), female(A).
cousin(A, B) :- parent(X, A), sibling(Y, X), son(B, Y).
cousin(A, B) :- parent(X, A), sibling(Y, X), daughter(B, Y).

% Cousins Children are also cousin
cousin(A, B) :- parent(X, A), parent(Y, B), cousin(X, Y).

wife(A, B) :- parent(B, X), parent(A, X), female(A), A \= B.
husband(A, B) :- parent(B, X), parent(A, X), male(A), A \= B.

collect_cousins(X, Cousin) :- setof(Y, cousin(Y, X), Cousin).

% change_directory('C:/Users/Admin/Desktop/BE/sem 6/AI/Prac3').