
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
        
        
    def getComputerMove( self, game_state ):
        move = 0
        for i in range(len(game_state)):
            if game_state[i] == 0:
                move = i
                break
        return move
