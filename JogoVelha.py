# Traduzindo um antigo codigo em Pascal de jogo da velha feito ainda na faculdade para Python


Vazio = ' '
Jogador_X = 'x'
Jogador_O = 'o'

class Tabuleiro:
    #print "Classe representando o tabuleiro."""
    def __init__(self):
        #print "Zerando o tabuleiro."
        self.casas = [Vazio]*9
        self.casas_livres = '123456789'

    def mostraTabuleiro(self):
        #print "Mostra o tabuleiro na tela."
        for linha in [self.casas[0:3], self.casas[3:6], self.casas[6:9]]:
            print ' '.join(linha)
    
    def fazJogada(self, casa, jogador):
       #print "Executa uma jogada."
        self.casas[casa] = jogador

    def desfazJogada(self, casa):
        #print "Desfaz uma jogada."
        self.fazJogada(casa, Vazio)
    
    def retornaCasasLivres(self):
        #print "Retorna uma lsita com as jogadas possiveis."
        return [pos for pos in range(9) if self.casas[pos] == Vazio]

    def numCasa(self, casa):
        #print "Retorna os numeros das casas livres."
        return self.casas_livres[casa]

    def ganhador(self):
        #print "Determina se alguem ganhou o jogo. Retorna Jogador_X, Jogador_O or None"
        jogos_possiveis = [[0,1,2],[3,4,5],[6,7,8], # vertical
                        [0,3,6],[1,4,7],[2,5,8],    # horizontal
                        [0,4,8],[2,4,6]]            # diagonal
        for row in jogos_possiveis:
            if self.casas[row[0]] != Vazio and tudoIgual([self.casas[i] for i in row]):
                return self.casas[row[0]]

    def fimJogo(self):
        #Print "Indica se o jogo acabou, se alguem ganhou ou fim das jogadas."
        return self.ganhador() or not self.retornaCasasLivres()


def jogador(Tabuleiro, jogador):
    #print "Funcao do jogador."
    Tabuleiro.mostraTabuleiro()
    casas_livres = dict([(Tabuleiro.numCasa(move), move) for move in Tabuleiro.retornaCasasLivres()])
    jogada = raw_input("Qual a sua jogada (%s)? " % (', '.join(sorted(casas_livres))))
    while jogada not in casas_livres:
        print "A casa, '%s' nao eh valida. Tente novamente." % move
        jogada = raw_input("Qual a sua jogada (%s)? " % (', '.join(sorted(casas_livres))))
    Tabuleiro.fazJogada(casas_livres[jogada], jogador)
    
def computador(Tabuleiro, jogador):
    #print "Funcao para o computador"
    #t0 = time.time()
    Tabuleiro.mostraTabuleiro()
    #print "Implementar a inteligencia do computador"
    
    #print "Passei aqui!"
    Tabuleiro.fazJogada(1, jogador)
    
def jogo():
    #print "Rodando o jogo"
    b = Tabuleiro()
    turn = 1
    while True:
        print "Jogada %i." % turn
        jogador(b, Jogador_O)
        if b.fimJogo(): 
            break
        computador(b, Jogador_X)
        if b.fimJogo(): 
            break
        turn += 1

    b.mostraTabuleiro()
    if b.ganhador():
        print 'Jogador "%s" ganhou' % b.ganhador()
    else:
        print 'Sem vencedores.'
    
if __name__ == "__main__":
    jogo()