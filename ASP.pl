package(1; 2; 3).

location(a; b; c; d; e; f; g; h; i).

% Original adjacency pairs
adjacent(a,b; b,c; c,e; e,d; a,d; d,f; f,h; h,g; h,i).

% Package locations
at_location(1, b).
at_location(2, e).
at_location(3, f).

% Symmetric adjacency pairs
adjacent(Y,X) :- adjacent(X,Y), location(X), location(Y).

