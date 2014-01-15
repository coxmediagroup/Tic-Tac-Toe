from twisted.web import server, resource
from twisted.internet import reactor
from src.tic_tac_toe import game_server
import json

class ApiRoot(resource.Resource):
    def render_GET(self, request):
        return "There are %d active games." % len(game_server.games)


class CreateGameResource(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        """Create new game and communicate game_id to client for subsequent 
        requests."""
        game = game_server.createGame()
        data = {'gameId': str(game.id), 'board': game.board,}
        return json.dumps(data)


class PlayTurnResource(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        content = request.content.getvalue()
        turn_info = json.loads(content)

        gameId = turn_info['gameId']
        turnNum = turn_info['turn']
        squareNum = int(turn_info['square'])

        game = game_server.getGame(gameId)
        status = game.do_turn(turnNum, squareNum)

        data = {
            'gameId': str(game.id), 
            'gameState': status,
            'board': game.board,
            'winningSquares': game.winning_squares,
        }
        return json.dumps(data)


root = resource.Resource()

tttApiRoot = ApiRoot()
tttApiRoot.putChild('create-game', CreateGameResource())
tttApiRoot.putChild('play-turn', PlayTurnResource())

root.putChild('TTT_API', tttApiRoot)

site = server.Site(root)
reactor.listenTCP(8080, site)
reactor.run()

