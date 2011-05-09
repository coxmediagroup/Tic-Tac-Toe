class Participant(object):
    def __init__(self):
        self.shape = EMPTY
        self.opponent_shape = EMPTY
    
    def setShape(self, shape):
        """ Set the shape we are using """
        self.opponent_shape = 1 if shape == 2 else 2
        self.shape = shape 

class LocalHuman(Participant):
    """ Console player for a game """
    def __init__(self):
        pass

class Ai(Participant):
    def __init__(self):
        pass
