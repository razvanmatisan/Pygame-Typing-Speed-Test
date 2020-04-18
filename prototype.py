import pygame
from pygame.locals import *

WIDTH = 800
HEIGHT = 600

class Game:

    def __init__(self):
        self.window = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption('Typing Speed Test')
        # pygame.time.Clock().tick(60)
        # self.smiley = Smiley(self, [WIDTH // 2, HEIGHT // 2])
        # self.gameObjects = [self.smiley]

    def run(self):
        running = True
        while running:
            # Game logic happens here
            self.input()
            self.update()
            self.draw()    def input(self):

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = FALSE

    def update(self):
        pass
        # for gameObject in self.gameObjects:
        #     gameObject.update()


    def draw(self):
        pass
        # self.window.fill(BLACK)

        # for gameObject in self.gameObjects:
        #     gameObject.draw()

        # pygame.display.update()

def main():
    # Run game
    game = Game()
    game.run()

if __name__ == '__main__':
    main()