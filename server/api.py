import endpoints
from protorpc import message_types, messages, remote

from messages import GameMessage, MoveMessage
from models import Game


CLIENT_IDS = [endpoints.API_EXPLORER_CLIENT_ID]


@endpoints.api(allowed_client_ids=CLIENT_IDS,
               description='Tic Tac Toe API',
               name='tictactoe',
               version='v1')
class TicTacToeApi(remote.Service):
    """TicTacToe API."""

    _id_resource = endpoints.ResourceContainer(
        message_types.VoidMessage, id=messages.IntegerField(1))

    _move_resource = endpoints.ResourceContainer(
        MoveMessage, id=messages.IntegerField(1))

    @endpoints.method(message_types.VoidMessage, GameMessage,
                      path='start', http_method='POST')
    def start(self, unused_request):
        game = Game.query().get()
        if not game:
            game = Game()
            game.put()
        return game.to_message()

    @endpoints.method(_move_resource, GameMessage,
                      path='move/{id}', http_method='PUT')
    def move(self, request):
        game = Game.get_by_id(request.id)
        square = request.square

        setattr(game, square, 'X')
        if game.is_won('X'):
            game.outcome = Game.WON
        elif game.is_full():
            game.outcome = Game.TIED
        else:
            setattr(game, game.get_best_square(), 'O')
            if game.is_won('O'):
                game.outcome = Game.LOST

        game.put()
        return game.to_message()

    @endpoints.method(_id_resource, GameMessage,
                      path='replay/{id}', http_method='PUT')
    def replay(self, request):
        game = Game.get_by_id(request.id)
        if not game:
            raise endpoints.NotFoundException
        game.reset()
        game.put()
        return game.to_message()


application = endpoints.api_server([TicTacToeApi])
