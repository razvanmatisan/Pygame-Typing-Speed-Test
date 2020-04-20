import pygame
from pygame.locals import *
import time
import random

WIDTH = 800
HEIGHT = 600
RED = (255, 0, 0)

class button():
    def __init__(self, color, x, y, width, height, text = ''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            window.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width and pos[1] > self.y and pos[1] < self.y + self.height:
            return True
        return False


class Game:
    def __init__(self):
        pygame.init()

        self.running = True
        self.input_words = []
        self.word = ''

        self.background = pygame.image.load('background.jpeg')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.window = pygame.display.set_mode([WIDTH, HEIGHT])
        
        pygame.display.set_caption('Typing Speed Test')
        
        pygame.time.Clock().tick(60)

    def random_words(self):
        fin = open('words.txt').read()
        words = fin.split('\n')
        random_word = random.choice(words)
        return random_word

    def run(self):
        self.reset_game()

        while self.running:
            self.first_page()

    def first_page(self):
        self.window.blit(self.background, (0, 0))
        start_button = button(RED, 310, 265, 200, 100, "Start")

        start_button.draw(self.window, (0, 0, 0))
        pos = pygame.mouse.get_pos()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isOver(pos):
                    pygame.display.update()
                    print("DAAAAAA")
                    self.main_page()
        pygame.display.update()
    
    def main_page(self):
        self.window.blit(self.background, (0, 0))
        pygame.display.update()

        clock = pygame.time.Clock()
        start = 60
        dt = 0

        running = True
        while running:
            pygame.draw.rect(self.window, (255, 255, 255), (250, 300, 300, 50), 5)
            
            self.draw_text((230, 230, 0), "Time: " + str(start), (400, 100))

            start -= dt
            if start <= 0:
                start = 60
            pygame.display.flip()
            dt = clock.tick(30) / 1000
            self.window.blit(self.background, (0, 0))

            random_word = self.random_words()
            self.draw_text((230, 230, 0), random_word, (400, 300))
            self.input_words.append(random_word)

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.MOUSEMOTION:
                    pass
                clock = pygame.time.Clock()
                self.draw_text((230, 230, 0), "Caterinca", (400, 200))
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
    
    def update(self):
        pass
        # for gameObject in self.gameObjects:
        #     gameObject.update()


    def draw_text(self, color, message, position):
        
        # def draw_text(self, screen, msg, y ,fsize, color):
        #msg = "Typing Speed Test"
        #self.draw_text(self.screen, msg,80, 80,self.HEAD_C)

        # draw icon image
        # self.time_img = pygame.image.load('icon.png')
        # self.time_img = pygame.transform.scale(self.time_img, (150,150))

        #screen.blit(self.time_img, (80,320))
        # self.window.blit(None, (80, 130))
        # self.draw_text(screen,"Reset", self.h - 70, 26, (100,100,100))

        font = pygame.font.SysFont('comicsans', 60)
        text = font.render(message, 1, color)
        text_rect = text.get_rect(center = position)
        self.window.blit(text, text_rect)

        # self.window.blit(self.time_img, (-75,self.h-140))
        # self.draw_text(screen,"Reset", self.h - 70, 26, (100,100,100))
        pygame.display.update()
    
    def reset_game(self):
        pass

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()