from app.ag.controller.tictactoe import TicTacToeController

GET = {"method": ["GET"]}
POST = {"method": ["POST"]}

def configure(router):

    # Tic Tac Toe game page
    router.connect('/games/tictactoe',
                   controller=TicTacToeController,
                   action='index',
                   path='/games/tictactoe.pd')

    router.connect('/games/tictactoe/turn',
                   conditions=POST,
                   controller=TicTacToeController,
                   action='evaluate_board')
