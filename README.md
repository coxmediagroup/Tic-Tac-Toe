Tic-Tac-Toe
===========

Tic-Tac-Toe is an externally monitored project. This version is made in java
with the constraint that a machine never lose. I have self imposed constraints,
like finishing the project in 24 hours and having it be playable on windows, linux,
and android, on top of having at least some versions have a variable span game
board.

A plan to do a version in pytohn/django is in place and will likely happen shortly
after this java version is complete, albeit with different constraints. Code is best
edited in Fedora 19 eclipse with egit plugin.

A balance is chosen between lean code and extensibility, and was the target of
much thought. I will add some of the more relevant musings below in a thought
log type format, showing first context of the thought, then content, reverse
sorted by date.

Entry 3
-------

### Context
Writing first chunk of the artificial agent, some 1.75 hours in. Extracted from 
ArtificialAgentSimple.java

### Content
Oh so many options here... A day or two ago I thought of what a person
evaluating this product would want, and I thought it may be helpful to 
add difficulty modifiers. What could a difficulty modifier be, though?

Different spans/board sizes was the msot obvious, where the computer
could simply do tree/table lookups, whereas the human would have to
scheme given the rulesets of the board. Maybe you could have a 10 width
board but only need 4 slots (connect 4). Some of these could not be 
solved, and if so, how to solve in generic ways.

I leaned toward making a tree. After implementing the easy generic tree
in java, one may see the root's children as all permutations of the next 
move. Upon making the move, that part of the tree would be pruned. 
If the computer sees a branch which is undesirable (e.g. leading to 
certain doom) it would avoid it.

If this was not a solved game, 3x3, then I would weight trees according
to favorability - if you were guaranteed not to lose, a higher score,
guaranteed to win, higher yet. Difficulty could then be based on how many
plys, or levels, the a.i. would look ahead to see where it would move,
similar if I remember correctly to chess a.i.

I was in a group in college that made 3d Minesweeper. It was an interesting
project, and made me muse about 3d tictactoe and an a.i. for it. The tree
model could handle this quite easily. But, since this is such a small
project, I'll instead just ramble on for paragraphs about what I think
at certain stages rather than code it, and instead code a simplistic
model which does the job for 3x3.

Entry 2
-------

### Context
When first writing the terminal based human vs human game client, some 1.5 hours in.
Extracted from HumanVsHuman (near the bottom)

### Content
I thought of a lot of dumb fancy programming stuff here for some reason. The plague
of design patterns struck me, where I thought of adding an interface for agents
which listen to mark events, then sends events (which the board would listen for),
check the win state, and invoke another listener here if there is a win state. For this
particular problem, I feel it over-engineers the issue, but perhaps in the python
implementation I'll indulge myself in some lambda function handlers for this kind of thing.

What's the gang-of-four reference here - a monitor pattern I believe, or at least listener.
There are always a few patterns that apply. So do I express this in code, have folks see
I too verbosely and theoretically approach a simple problem? Do I stay agile/light and
wait to implement functionality to avoid code bloat? I tend toward the latter now, but
would express how I could go either way management directs me. Man was created to tend toward
laziness/comfort, no? That's why I'm here Friday night at 11:12 after all, heh.

Feels kinda like answering a question that isn't there. Should I implement a design pattern
where there's no one asking for a complex solution? Should I mock this unit test for
an eventuality I know I'll never interact with? Could I make a plugin infrastructure using
JSPF (like GDXworld on narfman0's github) to offer other listeners that could handle/render
the information differently? Notification system... in tic-tac-toe?

These things I entertained, but the sooo heavy burden of programming struck me. Life is soooo hard
(he said sarcastically). I suspect I'm more reverse engineering cox media group's intentions
and what they'd want rather than engineering the project. A quandary they
put me in, and here I lie rambling on Friday night whilst musing about this stuff.
I suppose if I want to twist it to some other positive, that CMG as customer, I care to that degree
to get the job done the way they want - props to me. 

Entry 1
-------

### Context
Written some 0.5 hours in, when first predicting how in depth I should go with the project.
This is extracted from Board.java.

### Content
Board class for tic-tac-toe. Initially I was thinking easymode array, but upon
reflection, I wondered how extensible we could want this. I considered a.i. implications
as a result of making it variable width, a la 4 width tic tac toe, or variable width
and different win conditions, a la connect four.

For a brief while I considered my potential enjoyment of making a connect four a.i.,
with a decision tree built on startup and continuous pruning each turn. This could work 
for tic-tac-toe, variable width, and variable iwn conditions. I don't know
what cox is going for here yet, as this is the first twenty minutes or so, but seeing as 
how this is a (I don't want to say trivial) easier exercise, they are probably looking
for thought process, in which case I should turn this out before they reject me with
"noob array java (ab)user" before I do my python/django implementation.

First step: make the board class, test it, verify I know if an agent (ai/human) wins or not.
For now I'll go easy as I'm probably over-thinking. I've been balancing how agile I should
show this and that I don't add needlessly complex code on the one hand, vs extensible 
design that could work for variable width tic tac toe, or connect four/connect five/
connect infinity. Dat psychological warfare...
