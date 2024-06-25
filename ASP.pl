#const max_time = 10. % Default value

% Define time steps
time(0..max_time).

% INIT
robot_at(0,a).
packet_at(0, one, b).
packet_at(0, two, e).
% packet_at(0, three, f).
carry(0, empty).
% packet_at(0, two, e).

% GOAL
packet_at(max_time, one, e).
robot_at(max_time, a).
% carry(1, one).
% carry(6, two).

% PLAN
% execute(0,load(one)).
% execute(1,move(b)).
% execute(2,release(one)).
% execute(3,move(c)).
% execute(6,wait).

% Define locations
location(a; b; c; d; e; f; g; h; i).

% Original adjacency pairs
adjacent(a,b; b,c; c,e; e,d; a,d; d,f; f,h; h,g; h,i).

% Define packets
packet(empty; one; two).

% Define actions
action(move(X)) :- location(X).
action(load(X)) :- packet(X).
action(release(X)) :- packet(X).
action(wait).

% Not more than one execution at a time.
1 { execute(T, A) : action(A) } 1 :- time(T).
:- execute(T, X), execute(T, Y), X!=Y.

% Definition: robot at location
1 { robot_at(T, A) : location(A) } 1 :- time(T).
:- robot_at(T, A), robot_at(T, B), A!=B.

% Definition: packet at location
1 { packet_at(T, A, X) : location(X) } 1 :- time(T), packet(A), A!=empty.
:- packet_at(T, A, X), packet_at(T, A, Y), X!=Y, A!=empty.
% packet_at(T, empty, X) :- time(T), location(X).
:- packet_at(T, empty, X).

% Definition: Adjacent Locations
adjacent(Y,X) :- adjacent(X,Y), location(X), location(Y).

% Definition: execute move action
execute(T, move(B)) :- time(T), location(A), location(B), robot_at(T, A), robot_at(T+1, B), A!=B.
robot_at(T+1, B) :- execute(T, move(B)).
A!=B :- robot_at(T, A), execute(T, move(B)).
:- execute(T, move(B)), robot_at(T, A), not adjacent(A, B).

% Definition: packet carry
1 { carry(T, A) : packet(A) } 1 :- time(T).
:- carry(T, A), carry(T, B), A!=B.
packet_at(T, A, X) :- carry(T, A), robot_at(T, X), A!=empty.

% %%%%%% make sure that a package cannot switch while carried.
:- carry(T, A), carry(T+1, B), B!=A, A!=empty, not execute(T, release(A)).
:- carry(T, A), carry(T+1, B), A!=B, B!=empty, not execute(T, load(B)).


% If a packet moves it must be carried
carry(T, A) :- packet_at(T, A, X), packet_at(T+1, A, Y), X!=Y, A!=empty.

% If no packet is carried all packets stay put (Implied by line 70)
% packet_at(T+1, A, X) :- packet_at(T, A, X), carry(T, empty), A!=empty.

% Definition: execute load
execute(T, load(A)) :- time(T), packet(A), carry(T, empty), carry(T+1, A), A!=empty.
:- execute(T, load(emtpy)).
carry(T, empty) :- execute(T, load(A)).
carry(T+1, A) :- execute(T, load(A)).

% If the robot loads a packet it must be at the robots location (Implied by line 70)
% packet_at(T, A, X) :- location(X), execute(T, load(A)), robot_at(T, X).
% robot_at(T, X) :- location(X), execute(T, load(A)), packet_at(T, A, X).

% Definition: execute release
execute(T, release(A)) :- time(T), packet(A), carry(T+1, empty), carry(T, A), A!=empty.
:- execute(T, release(emtpy)).
carry(T, A) :- execute(T, release(A)).
carry(T+1, empty) :- execute(T, release(A)).

% If the robot releases the packet it remains at the location of the robot.
packet_at(T+1, A, X) :- location(X), execute(T, release(A)), robot_at(T, X).
% robot_at(T, X) :- location(X), execute(T, release(A)), packet_at(T+1, A, X).

% Minimize actions
:~ execute(T, A), A != wait. [T@1, T, A]

% Minimize faults
% :~ fault(T). [1@T, T]

#show execute/2.
% #show robot_at/2.
% #show carry/2.
% #show packet_at/3.
