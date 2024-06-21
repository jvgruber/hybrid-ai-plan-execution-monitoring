
boy(dewey; louie; huey).
color(yellow; green; white).
design(panda; camel; giraffe).
age(4; 5; 6).

% --> BOY WEARS COLOR <--
wears_color(B, C) : color(C) :- boy(B).
:- wears_color(B1, C), wears_color(B2, C), B1 != B2.

% --> BOY WEARS DESIGN <--
wears_design(B, D) : design(D) :- boy(B).
:- wears_design(B1, D), wears_design(B2, D), B1 != B2.
 
% --> EACH BOY HAS DISTINCT AGE <--
is(B, A) : age(A) :- boy(B).
:- is(B1, A) , is(B2, A), B1 != B2.

% --> YOUNGER
younger(B1, B2) :- is(B1, A1), is(B2, A2), A1 < A2.
not younger(B2, B1) :- younger(B1, B2).

% Axiom 1
younger(huey, B) :- wears_color(B, C), C = green.

% Axiom 2
is(B,A) :- wears_design(B, D), D = camel, A = 5.
 
% Axiom 3
wears_color(dewey, yellow).

% Axiom 4
wears_design(louie, giraffe).

% Axiom 5
:- wears_color(B, C) , wears_design(B, D), C = white, D = panda. 

#show wears_color/2.
#show wears_design/2.
#show is/2.
#show younger/2.
