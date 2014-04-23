import functools

import endpoints
from google.appengine.api import namespace_manager
from protorpc import message_types, messages, remote

from messages import GameMessage, MoveMessage
from models import Game, Squares


CLIENT_IDS = ['74921937461.apps.googleusercontent.com',
              endpoints.API_EXPLORER_CLIENT_ID]


def require_user(endpoints_method):

    @functools.wraps(endpoints_method)
    def wrapped(*args, **kw):
        user = endpoints.get_current_user()
        if user is None:
            raise endpoints.UnauthorizedException('Invalid token.')
        namespace_manager.set_namespace(user.user_id())
        return endpoints_method(*args, **kw)

    return wrapped


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
    @require_user
    def start(self, unused_request):
        game = Game.query().get()
        if not game:
            game = Game()
            game.put()
        return game.to_message()

    @endpoints.method(_move_resource, GameMessage,
                      path='move/{id}', http_method='PUT')
    @require_user
    def move(self, request):
        game = Game.get_by_id(request.id)
        square = request.square

        if not game:
            raise endpoints.NotFoundException
        if game.outcome is not None:
            raise endpoints.BadRequestException
        if square not in Squares.ALL:
            raise endpoints.BadRequestException
        if not game.is_empty_square(square):
            raise endpoints.BadRequestException

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
    @require_user
    def replay(self, request):
        game = Game.get_by_id(request.id)
        if not game:
            raise endpoints.NotFoundException
        game.reset()
        game.put()
        return game.to_message()


application = endpoints.api_server([TicTacToeApi])
