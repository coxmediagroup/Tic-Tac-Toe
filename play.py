import pygame, sys
BG = "res/paper.png"

class Main(object):
    def __init__(self):
        self.setup()
        
    def setup(self):
        pygame.init()
        size = (self.width, self.height) = (640,480)
        self.black = (0, 0, 0)
        self.background_image = pygame.image.load(BG)
        self.screen = pygame.display.set_mode(size)
        self.setup_background()
    
    def setup_background(self):
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.screen.blit(self.background_image, (0, 0))
        pygame.display.flip()
        
    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        pygame.display.flip()

    def event_loop(self):
        #toon = self.toon
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
#                elif event.type == pygame.KEYDOWN:
            self.draw()
            pygame.time.delay(30)


if __name__ == '__main__':
    app = Main()
    app.event_loop()