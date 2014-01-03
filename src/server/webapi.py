from twisted.web import server, resource
from twisted.internet import reactor

class ApiRoot(resource.Resource):
    def render_GET(self, request):
        return "prepath is %s and postpath is %s" % (request.prepath, request.postpath)

class CreateGameResource(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        return "<html>CreateGameResource</html>"


class PlayTurnResource(resource.Resource):
    isLeaf = True
    def render_POST(self, request):
        return "<html>PlayTurnResource</html>"

root = resource.Resource()

tttApiRoot = ApiRoot()
tttApiRoot.putChild('create-game', CreateGameResource())
tttApiRoot.putChild('play-turn', PlayTurnResource())

root.putChild('TTT_API', tttApiRoot)

site = server.Site(root)
reactor.listenTCP(8080, site)
reactor.run()

