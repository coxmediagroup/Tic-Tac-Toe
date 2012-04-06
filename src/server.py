'''
Twisted implementation of tic-tac-toe
'''
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.conch.telnet import TelnetTransport, TelnetProtocol
from common import Storage
from ttt import Board 
from ttt_twisted import  TelnetHuman, TelnetAi, TelnetGame

class TTTProtocol(TelnetProtocol):
    timeout = 300
    """ Where a protocol instance comes to life """
    def connectionMade(self):
        print "connection made"
        if self.factory.number_of_connections >= self.factory.max_connections:
            self.transport.write('Too many connections, try again later')
            self.transport.loseConnection()
            return
        
        self.factory.number_of_connections += 1
        self.identifier = self.factory.number_of_connections
        self.timeout_deferred = reactor.callLater(TTTProtocol.timeout,
                self.transport.loseConnection)
        
        # Have storage allocate us some space
        Storage(self.identifier)._game_board = Board(size=3)
        Storage(self.identifier)._player_one = TelnetAi(self)
        Storage(self.identifier)._player_two = TelnetHuman(self)
        Storage(self.identifier)._game_instance = TelnetGame(self)
        Storage(self.identifier)._game_instance.run()

    def connectionLost(self, reason):
        TelnetProtocol.connectionLost(self, reason)
        self.factory.number_of_connections -= 1
        print "connection lost"
        print reason
        
    def dataReceived(self, data):
        if self.timeout_deferred:
            self.timeout_deferred.cancel()
            self.timeout_deferred = reactor.callLater(TTTProtocol.timeout,
                    self.transport.loseConnection)
        reactor.callLater(0.01, Storage(self.identifier)._player_two.dataReceivedHandler, data)

    def sendData(self, data):
        self.transport.write(data)

class TTTFactory(Factory):
    protocol = TTTProtocol
    max_connections = 10
    
    def __init__(self):
        self.number_of_connections = 0
if __name__ == "__main__":
    reactor.listenTCP(2300, TTTFactory())
    reactor.run()
