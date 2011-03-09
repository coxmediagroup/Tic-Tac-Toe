'''
tests for invincitron

'''

import random

import invincitron as I

class test_RandomGames(object):
    ''' as a first guess, show that in n games, played with random moves,
    invincitron always wins 
    '''
    def test_random(self):
        for ii in range(20):
            print I.interactive(I.RandomPlayer(),I.RandomPlayer())

       

