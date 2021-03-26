% FROZEN LAKE
% A slippery lake to cross.


% PROBLEM-SPECIFIC DOMAIN (UNINTERPRETED FUNCTIONS) ****************************

%	VARIABLES:
%	L			... describes a location `L`, currently between 0-15
%   TODO: Größe variable machen
%       ___________
%      |0  1  2  3 |
%      |4  5  6  7 |
%      |8  9  10 11|
%      |12 13 14 15|
%      |___________|

% 	STATE FUNCTIONS S(...):
%	position(L)	... describes each position
%   currentPosition(L) ... describes the location `L` of the agent
%	frozen(L)	... describes whether the location `L` is frozen
%   leftEdge(L) ... describes whether the location `L` is on the left edge on the lake
%   rightEdge(L) ... describes whether the location `L` is on the right edge on the lake
%   upperEdge(L) ... describes whether the location `L` is on the upper edge on the lake
%   lowerEdge(L) ... describes whether the location `L` is on the lower edge on the lake


%	ACTION FUNCTIONS A(...):
%	move(L)		...	the agent moves to location `L`

%	STATIC STATE (ATOMS):
%   TODO: parametrisieren
%   #const length ... the horizontal length of the lake
%   #const goal ... the goal state to be reached, must be >0

% KNOWLEDGE ********************************************************************

% Describe which actions are executable in a given state
% 	INPUT:		tic(S(...), T)
% 	INPUT:		terminal(T)
% 	OUTPUT: 	executable(A(...), T)

% TODO: dynamisch:
#const length = 4.
#const goal = 15.
position(0..15).
frozen(0..4). frozen(6). frozen(8..10). frozen(13..15).
leftEdge(0). leftEdge(4). leftEdge(8). leftEdge(12).
rightEdge(3). rightEdge(7). rightEdge(11). rightEdge(15).
upperEdge(0..3).
lowerEdge(12..15).


executable(move(left), T) :- tic(currentPosition(L), T), frozen(L-1), not leftEdge(L), not terminal(T).
executable(move(right), T) :- tic(currentPosition(L), T), frozen(L+1), not rightEdge(L), not terminal(T).
executable(move(up), T) :- tic(currentPosition(L), T), frozen(L-length), not upperEdge(L), not terminal(T).
executable(move(down), T) :- tic(currentPosition(L), T), frozen(L+length), not lowerEdge(L), not terminal(T).

% Describe the effects of state transitions
%	INPUT:		tic(S(...), T)
%	INPUT: 		act(A(...), T)
%	INPUT: 		time(T)
%	OUTPUT:		tic(S(...), T+1)

tic(currentPosition(L), T+1) :- tic(currentPosition(L), T), not act(move(_), T), time(T).
tic(currentPosition(L-1), T+1) :- act(move(left), T), tic(currentPosition(L), T), time(T).
tic(currentPosition(L+1), T+1) :- act(move(right), T), tic(currentPosition(L), T), time(T).
tic(currentPosition(L-length), T+1) :- act(move(up), T), tic(currentPosition(L), T), time(T).
tic(currentPosition(L+length), T+1) :- act(move(down), T), tic(currentPosition(L), T), time(T).
-tic(currentPosition(L),T+1) :- tic(currentPosition(L),T), act(move(_),T).


% Describe the rewards for each state
%	INPUT: 		tic(S(...), T)
%	OUTPUT: 	partialReward(R, T)

goalState(T) :- tic(currentPosition(goal), T), time(T).
partialReward(100,T) :- goalState(T), not goalState(T-1).
partialReward(-1,T)  :- act(_,T-1).


% Describe terminal states
%	INPUT: 		tic(S(...), T)
%	OUTPUT: 	terminal(T)

terminal(T) :- goalState(T).