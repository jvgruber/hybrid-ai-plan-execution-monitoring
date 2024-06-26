%#const max_time = 10. % Default value

% Define time steps
time(0..max_time).

% INITIAL CONDITIONS
robot_at(0,a).
carry(0, empty).
packet_at(0, one, b).
packet_at(0, two, e).
packet_at(0, three, f).

% INTENDED PLAN SEQUENCE (get this from python)
% fault(0) :- not execute(0,move(b)).
% fault(1) :- not execute(1,load(one)).
% fault(2) :- not execute(2,move(d)).
% fault(3) :- not execute(3,move(f)).
% fault(4) :- not execute(4,move(h)).
% fault(5) :- not execute(5,release(one)).
% fault(6) :- not execute(6,move(f)).
% fault(7) :- not execute(7,load(three)).
% fault(8) :- not execute(8,move(d)).
% fault(9) :- not execute(9,release(three)).

% OBSERVATION SEQUENCE (get this from python)
% saw_packet_at(1, one).
% :- saw_packet_at(3, P).
% saw_packet_at(4, three).
% :- saw_packet_at(5, P).
% saw_packet_at(7, three).
% :- saw_packet_at(9, P).


% Define locations
location(a; b; c; d; e; f; g; h; i).

% Original adjacency pairs
adjacent(a,b; a,d; b,c; b,d; c,e; e,d; d,f; f,h; h,g; h,i).

% Define packets
packet(empty; one; two; three).

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

% Make sure that a package cannot switch while carried.
:- carry(T, A), carry(T+1, B), B!=A, A!=empty, not execute(T, release(A)).
:- carry(T, A), carry(T+1, B), A!=B, B!=empty, not execute(T, load(B)).

% If a packet moves it must be carried
carry(T, A) :- packet_at(T, A, X), packet_at(T+1, A, Y), X!=Y, A!=empty.

% Definition: execute load
execute(T, load(A)) :- time(T), packet(A), carry(T, empty), carry(T+1, A), A!=empty.
:- execute(T, load(emtpy)).
carry(T, empty) :- execute(T, load(A)).
carry(T+1, A) :- execute(T, load(A)).

% Definition: execute release
execute(T, release(A)) :- time(T), packet(A), carry(T+1, empty), carry(T, A), A!=empty.
:- execute(T, release(emtpy)).
carry(T, A) :- execute(T, release(A)).
carry(T+1, empty) :- execute(T, release(A)).

% If the robot releases the packet it remains at the location of the robot.
packet_at(T+1, A, X) :- location(X), execute(T, release(A)), robot_at(T, X).

% Define observation 
saw_packet_at(T,P) :- robot_at(T,L), packet_at(T,P,L), P!=emtpy, not carry(T,P).
A=B :- saw_packet_at(T,P), robot_at(T,A), packet_at(T,P,B), P!=emtpy.

% Does not observe a packet at a location while carrying it.
:- saw_packet_at(T,P), carry(T,P), P!=emtpy.

% Observations only happens when entering a location. (does not work)
% :- saw_packet_at(T+1,P), robot_at(T,L), packet_at(T,P,L), P!=emtpy.

% Minimize actions and penalize delayed execution
:~ execute(T, A), A != wait. [T@1, T, A]

% Minimize faults
:~ fault(T). [(2*max_time)@1, T]

#show execute/2.
% #show robot_at/2.
% #show carry/2.
% #show packet_at/3.
% #show saw_packet_at/2.
% #show fault/1.
