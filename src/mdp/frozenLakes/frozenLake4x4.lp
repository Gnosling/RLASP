% The surface is described using a grid like the following
%
%        SFFF   =  0  1  2  3
%        FHFH   =  4  5  6  7
%        FFFH   =  8  9  10 11
%        HFFG   =  12 13 14 15
%
%    S : starting point, safe
%    F : frozen surface, safe
%    H : hole, fall to your doom
%    G : goal, where the frisbee is located

state(0..15).
% currentState(0).
standAble(0..4). standAble(6). standAble(8..10). standAble(13..15).
left :- currentState(X), state(X-1), standAble(X-1), X\4!=0.
right :- currentState(X), state(X+1), standAble(X+1), X\4!=3.
up :- currentState(X), state(X-4), standAble(X-4).
down :- currentState(X), state(X+4), standAble(X+4).