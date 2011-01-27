from random import choice, shuffle

WINNERS = [[0,1,2], [3,4,5], [6,7,8],
           [0,3,6], [1,4,7], [2,5,8],
           [0,4,8], [2,4,6]]

EDGECORNER = {
    1: [6,8],
    3: [2,8],
    5: [0,6],
    7: [0,2]}

CORNERS = [0,2,6,8]
OPPCORNER = {0:8, 2:6, 6:2, 8:0}

class ToeBot:
    

    def __init__(self):
        self.spots = [0,0,0,0,0,0,0,0,0]
        self.their_last_move = None
        self.state = -1

    def reset(self):
        self.spots = [0,0,0,0,0,0,0,0,0]
        self.their_last_move = None
        self.state = -1

    def my_move(self):
        if self.state != -1:
            raise Exception('Game is already over.')
        tmp = self.determine_move()
        if type(tmp) == type([]):
            tmp = choice(tmp)
        self.spots[tmp] = 1
        self.test_state()
        return tmp

    def their_move(self, spot):
        if self.state != -1:
            raise Exception('Game is already over.')
        if self.is_legal_move(spot):
            self.spots[spot] = 2
            self.test_state()
            self.their_last_move = spot
        else:
            raise Exception('Illegal move.')

    def test_state(self):
        avail = 0
        for each in WINNERS:
            me = 0
            them = 0
            for s in each:
                if self.spots[s] == 1:
                    me = me + 1
                elif self.spots[s] == 2:
                    them = them + 1
                else:
                    avail = avail + 1
            if me == 3:
                self.state = 1
                break
            elif them == 3:
                self.state = 2
                break

        if self.state == -1:
            # test for tie
            if avail == 0:
                self.state = 0

    def is_legal_move(self, spot):
        return self.spots[spot] == 0

    def determine_move(self):
        # is the center free?
        if self.spots[4] == 0:
            # grab it!
            return 4

        # if just one more spot is needed to win, then do that
        spam = self.can_i_win()
        if spam:
            return spam

        # if they can win, better block that
        spam = self.can_they_win()
        if (spam):
            return spam

        # if they picked the center, it's their first move.
        # So, grab a corner
        if self.their_last_move == 4:
            return [0,2,6,8]

        # if they got an edge, grab the opposite corner
        if self.their_last_move in EDGECORNER.keys():
            opp = EDGECORNER[self.their_last_move]
            # randomize the opposite corners.
            # find one that's open
            shuffle(opp)
            if self.spots[opp[0]] == 0:
                return opp[0]
            elif self.spots[opp[1]] == 0:
                return opp[1]

            # what if they're both occupied?
            # Then either can_they_win() should have caught it,
            # or they've already won and we shouldn't be here.

        # if they picked a corner...
        if self.their_last_move in CORNERS:
            # get opposite corner
            tmp = OPPCORNER[self.their_last_move]
            # make sure it's open
            if not self.is_legal_move(tmp):
                # pick another corner
                for c in CORNERS:
                    if self.is_legal_move(c):
                        return c

        # all else failed? Just pick one
        avail = []
        for i in range(9):
            if self.spots[i] == 0:
                avail.append(i)
        return avail

    def close_to_winning(self, who):
        r = []
        for each in WINNERS:
            owned = 0
            avail = []
            for s in each:
                if self.spots[s] == who:
                    owned = owned + 1
                elif self.spots[s] == 0:
                    avail.append(s)
            if owned == 2 and len(avail) == 1:
                r.append(avail[0])

        return r

    def can_i_win(self):
        return self.close_to_winning(1)

    def can_they_win(self):
        return self.close_to_winning(2)

def print_board(bot, me, human):
    for i in range(9):
        if i % 3 == 0: print
        val = bot.spots[i]
        if val == 1:
            val = me
        elif val == 2:
            val = human
        else:
            val = str(i)
        print str(val),
    print
    
def play_game(bot, botfirst=False):
    bot.reset()
    if botfirst:
        human = 'O'
        me = 'X'
        print "I pick %i" % bot.my_move()
    else:
        human = 'X'
        me = 'O'

    while bot.state == -1:
        print_board(bot, me, human)        
        
        m = None
        while m == None:
            m = raw_input('Your move, human: ')
            try:
                m = int(m)
            except ValueError:
                m = None
                print "Ack!"
            if m < 0 or m > 8:
                print "Ack!"
                m = None

        bot.their_move(m)
        if bot.state == -1:
            print "I pick %i" % bot.my_move()

    print_board(bot, me, human)
    if bot.state == 1:
        print "HAHAHA! I have crushed you, puny human!"
    elif bot.state == 2:
        print "You... you won? Unpossible!"
    else:
        print "Well... we tied. Drat."
        
if __name__=='__main__':
    botfirst = False
    bot = ToeBot()
    keep_playing = True

    while keep_playing:
        play_game(bot, botfirst)
        
        print
        if raw_input("Play again, human? (y/n) ").lower() == 'y':
            botfirst = not botfirst
            print "\n\n__________"
        else:
            keep_playing = False
        
