from main import *
from random import choice
from collections import Counter

number_of_trials = 100000
silence()
counter1 = Counter()
counter2 = Counter()


# Choose a random move. The arguments are not used, but are required for syntactical reasons.
# The second return value None tells the calling function not to display any messages.
def random_move(x, y):
    return choice([k for k in range(1, 10) if GRID[k] == BLANK])


# Play lots of games between the expert system 'get_computer_move' and the random mover,
# and tabulate the results.
for _ in xrange(number_of_trials):
    winner1 = play(random_move, get_computer_move)
    winner2 = play(get_computer_move, random_move)
    counter1[winner1] += 1
    counter2[winner2] += 1

print "We simulated %d games between the expert system and a random mover.\n" % (2 * number_of_trials)
print "In the games where the expert system played first"
print "  the expert system won %d games," % counter2[X]
print "  the random mover won %d games," % counter2[O]
print "  and %d games were tied.\n" % counter2[BLANK]
print "In the games where the expert system played second"
print "  the expert system won %d games," % counter1[O]
print "  the random mover won %d games," % counter1[X]
print "  and %d games were tied.\n" % counter1[BLANK]
if counter2[0] == counter1[X] == 0:
    print "The expert system did not lose a single game!"
else:
    print "The expert system lost %d games. Guess it isn't an expert after all." % (counter1[0] + counter2[X])