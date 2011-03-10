# Traduzindo um antigo c—digo em Pascal de jogo da velha feito ainda na faculdade para Python


Vazio = ' '
Jogador_X = 'x'
Jogador_O = 'o'

class Tabuleiro:

    print "Classe representando o tabuleiro."""
    def __init__(self):
        #print "Zerando o tabuleiro."
        self.casas = [Vazio]*9
        self.casas_livres = '123456789'
        

def jogador(Tabuleiro, jogador):
    print "Funcao do jogador."
    
def computador(Tabuleiro, jogador):
    print "Funcao para o computador"
    
def jogo():
    print "Rodando o jogo"
    
if __name__ == "__main__":
    jogo()