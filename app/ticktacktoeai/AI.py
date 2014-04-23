import random

class TickTackToeAI():
    """
    Tick Tac Toe is a class for a Tick Tac Toe AI.
    
    Key:
    0 = unclaimed square
    1 = user claimed
    -1 = computer claimed.
    
    The game_state array is arranged much like you may expect:
    [1, 2, 3,
     4, 4, 5,
     6, 7, 8]
    """
    
    wins_list = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
    ]
    
    def didPlayerWin( self, game_state, isuser ):
        """
            Call with isuser=False to check for computer. 
            
            This function should be called after every move.
        """
        for win in self.wins_list:
            match = 0
            for w in win:
                i = 0
                for position in game_state:
                    if i == w and position == 1 and isuser == True:
                        match += 1
                    elif i == w and position == -1 and isuser == False:
                        match += 1
                    i += 1
            if match >= 3:
                #print "Winner: ", win
                return win
        return None
    
    
    def getSingleMoveWinner( self, game_state ):
        """
            Either returns a winning move or
            None, if not possible.
        """
        for win in self.wins_list:
            counter = 0
            blocked = False
            empty = -1
            for w in win:
                if game_state[ w ] == -1:
                    counter += 1
                if game_state[ w ] == 1:
                    blocked = True
                if game_state[ w ] == 0:
                    empty = w
            if counter == 2 and blocked == False:
                return empty
        return None
        
    def getStopUserMove( self, game_state ):
        """
            Either returns a blocking move or
            None, if not possible.
        """
        for win in self.wins_list:
            counter = 0
            unrequired = False
            empty = -1
            for w in win:
                if game_state[ w ] == 1:
                    counter += 1
                if game_state[ w ] == -1:
                    unrequired = True
                if game_state[ w ] == 0:
                    empty = w
            if counter == 2 and unrequired == False:
                return empty
        return None
        
    def getOtherMoves(self, game_state ):
        """
            Either returns a blocking move or
            None, if not possible.
        """
        i = 0
        for s in game_state:
            # try for center
            if i == 4 and s == 0:
                return i
            i += 1
        i = 0
        for s in game_state:
            if i in [0,2,6,8] and s == 0:
                return i
            i += 1
        i = 0
        for s in game_state:
            if i in [1,3,7,5] and s == 0:
                return i
            i += 1
        return None
            
        
    def getComputerMove( self, game_state ):
        """
            A.i.
                a) First see if we can win in one move, take it.
                b) See if we can block a 2 streak from the user.
                c) Corner pieces
                d) Check if center is free
                e) move outside-middle pieces
        
        """
        move = 0
        #a
        res1 = self.getSingleMoveWinner( game_state ) 
        if res1 != None:
            #print "Wining move: ", res1
            return res1
        #b
        res2 = self.getStopUserMove( game_state ) 
        if res2 != None:
            #print "Blocking move: ", res2
            return res2
        # cde
        res3 = self.getOtherMoves( game_state )
        if res3 != None:
            #print "Other move: ", res3
            return res3
        # backup
        i = 0
        for s in game_state:
            if s == 0:
                move = i
        return move
        
        
    def gameTest(self, game_state):
        cp_wins = 0
        user_wins = 0
        ties = 0
        game_on = True
        while game_on:
            if 0 not in game_state:
                game_on = False
                ties += 1
                break
                
            picking_user_move = True
            user_move = -1
            while picking_user_move and 0 in game_state:
                test = random.randrange(0,9)
                if game_state[ test ] == 0:
                    user_move = test
                    picking_user_move = False
            
            game_state[ user_move ] = 1
            user_win = self.didPlayerWin( game_state, True )
            if user_win != None:
                game_on = False
                user_wins += 1
                break
            
            cp_move = self.getComputerMove( game_state )
            game_state[ cp_move ] = -1        
            cp_win = self.didPlayerWin( game_state, False )
            if cp_win != None:
                game_on = False
                cp_wins += 1
                break
                
        winsdict = {}
        winsdict["cp_wins"] = cp_wins
        winsdict["user_wins"] = user_wins
        winsdict["ties"] = ties
        
        return winsdict
