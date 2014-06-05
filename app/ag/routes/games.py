GET = {"method": ["GET"]}
POST = {"method": ["POST"]}

def configure(router):

    # Tic Tac Toe game page
    router.connect('/games/tictactoe',
                   controller=TicTacToeController,
                   action='index',
                   path='/games/tictactoe.pd')
