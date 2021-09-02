# Overview of the Game

This is an implementation of the game "Omok" (as known in Korean) or "Gomoku" (as known in Japanese) or "connect-5" or "5-in-a-row" as known in English.
It is played on a Go board, not exactly on the 19 by 19 classic Go board, but on a smaller 15 by 15 go board.
<br/><br/>
Black goes first by putting a black stone on the board. White goes next, putting a white stone on a place where there are no stones.
If a position on the board is occupied, new stones cannot be placed on the position. No stones will be moved off the board until the game ends.
Black and white take turns placing stones on the board. The objective of the game is to place 5 stones in a row before the opponent.
<br/><br/>
There are variants of Gomoku. The most basic variant is when there are no illegal moves for white and black.
This means that if a position is not occupied, a player can put their stone there without any restrictions, and even more than 5 stones in a row is counted as a winning move.
This basic variant is proven to be unwinnable for white if black plays even moderately well (because black has the advantage of going first), 
so an alternate set of rules was made: the renju rule.
### The renju rule
In the renju rule, the basic gameplay is the same as the basic rules, but restrictions are placed on black's moves.
In a nutshell, "double threes", "double fours", and "overlines" (more than five in a row) are considered illegal moves for black.
Black cannot place stones if a position is an illegal position, and white can take advantage of this fact too.
White has no restrictions, and double threes, double fours, and overlines are all legal attacking moves for white.
For more details on the renju rule, the following guide might be helpful:  
https://renju.nu/renju-rules/

# Implementation of the Game
This implementation of Gomoku is based on the renju rule (described above), but without the opening rules.
The restrictions for black are implemnented, but the opening rules are not implemented. See the link above for more details on the renju rule.
<br/><br/>
To start the program, both python 3.9 and pygame must be installed.  
Running main.py will start the game.  
A timer is implemented, but running out of time does not end the game.  
Information about every possible move for black and white can be viewed using the "potential display options". When "Black" is selected, information about
black's moves are displayed. When "White" is selected, information about white's moves are displayed. The potentials are displayed on each position as follows:
the top right 2-letter code (ex: "o2") is information about the type of attack the move would be in the vertical direction. The top left code is the type of attack
in the top-left-to-bottom-right diagonal direction. The bottom right code is the type of attack in the horizontal direction. The bottom left code is the type of
attack in the bottom-left-to-top-right diagonal direction.  
These codes are used to determine which moves are illegal for black. (ex: if a position has two out of the four directions that is an "o3", then the move is a
double three and is illegal) They might also be used by an AI later to help determine the optimal move to make.
