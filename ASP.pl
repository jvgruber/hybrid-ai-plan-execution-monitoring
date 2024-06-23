% executes, packets, locations
% move(t, location, location) - adjacent(t, location, location)
% load(t, packet, location)  - at(t, packet, location)
% release(t, packet, location) - carry(t, packet, location)
% maximum one packet at same time
% 
% problems if not something then holds
% if llm says the sequence is inconsistent because of step x then
% run asp but delete all steps of the plan after llm predicted failure
% output should be an explaination to the observations

% Define time steps
time(0..10).

% INIT
at(0,a).
ploc(0, one, b).
ploc(0, two, e).

% GOAL
ploc(10, one, e).
ploc(10, two, b).

% Define locations
location(a; b; c).

% Define packets
packet(none; one; two; three).

% Define actions
action(move(X)) :- location(X).
action(load(X)) :- packet(X).

% Not more than one execution at a time.
1 { execute(T, A) : action(A) } 1 :- time(T).
:- execute(T, X), execute(T, Y), X!=Y.

% Definition: robot at location
1 { at(T, A) : location(A) } 1 :- time(T).
:- at(T, A), at(T, B), A!=B.

% Definition: packet at location
1 { ploc(T, A, X) : location(X) } 1 :- time(T), packet(A), A!=none.
:- ploc(T, A, X), ploc(T, A, Y), X!=Y, A!=none.
ploc(T, none, X) :- time(T), location(X).

% Definition: execute move action
execute(T, move(B)) :- time(T), location(A), location(B), at(T, A), at(T+1, B), A!=B.
at(T+1, B) :- time(T), location(A), location(B), execute(T, move(B)).
A!=B :- time(T), location(A), location(B), at(T, A), execute(T, move(B)).

% Definition: packet carry
1 { carry(T, A) : packet(A) } 1 :- time(T).
:- carry(T, A), carry(T, B), A!=B.
ploc(T, A, X) :- carry(T, A), at(T, X).

% Definition: execute load
execute(T, load(A)) :- time(T), packet(A), carry(T, none), carry(T+1, A).
carry(T, none) :- execute(T, load(A)).
carry(T+1, A) :- execute(T, load(A)).
:- load(none).
ploc(T, A, X) :- location(X), execute(T, load(A)), at(T, X).
at(T, X) :- location(X), execute(T, load(A)), ploc(T, A, X).

% Definition: execute release
execute(T, release(A)) :- time(T), packet(A), carry(T+1, none), carry(T, A).
carry(T, A) :- execute(T, release(A)).
carry(T+1, none) :- execute(T, release(A)).
:- release(none).


% Minimize faults
% :~ fault(T). [1@T, T]


#show execute/2.
#show at/2.
#show carry/2.
#show ploc/3.

