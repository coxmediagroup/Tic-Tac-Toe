import pygame, sys
import TicTacToeLib as TTTL
BG = "res/paper.png"
CD = "res/choosedialog.png"
XB = "res/xboxbutton.png"
OB = "res/oboxbutton.png"
BOARD = "res/board.png"

STATE_CHOOSE = 0
STATE_PLAY = 1
STATE_GAME_OVER = 2


class BoxButton(pygame.sprite.Sprite):
    def __init__(self, img, name, x, y):
        super(BoxButton, self).__init__()
        self.name = name
        temp_image = pygame.image.load(img)
        self.size = (self.width, self.height) = (66,66)
        self.image = pygame.transform.smoothscale(temp_image, self.size)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
class GameBoard(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(GameBoard, self).__init__()
        temp_image = pygame.image.load(BOARD)
        self.size = (self.width, self.height) = (288,288)
        self.cell_size = (self.cell_width, self.cell_height) = (96,96)
        self.image = pygame.transform.smoothscale(temp_image, self.size)
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.cell_list = self.createCellList()
        self.board = None
        
    def createCellList(self):
        cells = []
        x,y = 0,0
        for i in xrange(9):
            cells.append(pygame.Rect(x,y,96,96))
            # new row
            if (i+1) % 3 == 0:
                x = 0
                y += self.cell_height
            else:
                x += self.cell_width
                
        return cells            
        
    def getRelativePos(self, pos):
        absolute_x, absolute_y = pos
        relative_x = absolute_x - self.rect.left
        relative_y = absolute_y - self.rect.top
        return (relative_x, relative_y)
    
    def whichCell(self, pos):
        relative_pos = self.getRelativePos(pos)
        for idx, cell in enumerate(self.cell_list):
            if cell.collidepoint(relative_pos):
                return idx
            
    def update(self):
        # TODO will process game board and draw X's and O's
        pass
                

class Main(object):
    def __init__(self):
        self.setup()
        
    def setup(self):
        pygame.init()
        size = (self.width, self.height) = (640,480)
        self.black = (0, 0, 0)
        self.background_image = pygame.image.load(BG)
        self.choose_dialog = pygame.image.load(CD)
        self.game_board = GameBoard(200,100)
        self.boardGroup = pygame.sprite.GroupSingle(self.game_board)
        self.screen = pygame.display.set_mode(size)
        self.game_state = STATE_CHOOSE
        self.clicked = False
        self.click_pos = (0,0)
        self.player = None
        self.aiplayer = None
        self.aipiece = None
        self.box_buttons = pygame.sprite.Group()
        self.box_buttons.add(BoxButton(XB, TTTL.PIECE_X, 255, 179))
        self.box_buttons.add(BoxButton(OB, TTTL.PIECE_O, 339,179))
        self.setup_background()
    
    def setup_background(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.screen.blit(self.background_image, (0, 0))
        pygame.display.flip()
        
    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        if self.game_state == STATE_CHOOSE:
            self.screen.blit(self.choose_dialog, (250, 150))
            self.box_buttons.update()
            self.box_buttons.draw(self.screen)
        if self.game_state == STATE_PLAY:
            self.boardGroup.update()
            self.boardGroup.draw(self.screen)
            
        pygame.display.flip()
        
    def processClick(self, state):
        if state == STATE_CHOOSE:
            for button in self.box_buttons.sprites():
                if button.rect.collidepoint(self.click_pos):
                    self.player = TTTL.Player(button.name)
                    self.aipiece = TTTL.PIECE_X if button.name == TTTL.PIECE_X else TTTL.PIECE_O
                    self.aiplayer = TTTL.AIPlayer(self.aipiece)
                    self.game_board.board = TTTL.Board()
                    # TODO randomly determine who goes first
                    self.game_state = STATE_PLAY
                    return
        if state == STATE_PLAY:
            if self.game_board.rect.collidepoint(self.click_pos):
                print self.game_board.getRelativePos(self.click_pos)
                print self.game_board.whichCell(self.click_pos)
              
            
        

    def event_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
                    self.click_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONUP and self.clicked:
                    self.clicked = False
                    self.processClick(self.game_state)
                    
#                elif event.type == pygame.KEYDOWN:
            self.draw()
            pygame.time.delay(30)


if __name__ == '__main__':
    app = Main()
    app.event_loop()