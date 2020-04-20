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

    def draw(self, window, outline = None):
        if outline:
            pygame.draw.rect(window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
            
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
        self.user_words = []

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

        start = 60
        dt = 0

        running = True
        enabled = True
        start_game = False
        actual_word = ''

        while running:
            pygame.display.update()
            self.window.blit(self.background, (0, 0))
            if enabled:
                random_word = self.random_words()
                self.input_words.append(random_word)
                enabled = False
            self.draw_text((230, 230, 0), random_word, (400, 215))
            
            pygame.draw.rect(self.window, (255, 255, 255), (250, 300, 300, 50), 5)
            self.draw_text((230, 230, 0), actual_word, (400, 325))
            
            if start_game:
                clock = pygame.time.Clock()
                self.draw_text((230, 230, 0), "Time: " + str(int(start)), (400, 50))
                start -= dt
                if start <= 0:
                    print("Caterinca!!!")

                    running = False
                dt = clock.tick(40) / 1000

            pos = pygame.mouse.get_pos()

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pos[0] > 250 and pos[0] < 250 + 300 and pos[1] > 300 and pos[1] < 300 + 50:
                        start_game = True

                if event.type == pygame.KEYDOWN:
                    # if self.active and not self.end:
                    if event.key == pygame.K_RETURN:
                        enabled = True
                        self.user_words.append(actual_word)
                        actual_word = ''
                            
                    elif event.key == pygame.K_BACKSPACE:
                        actual_word = actual_word[:-1]
                    else:
                        try:
                            actual_word += event.unicode
                        except:
                            pass

        pygame.display.update()
    
    def update(self):
        pass
        # for gameObject in self.gameObjects:
        #     gameObject.update()


    def draw_text(self, color, message, position):
        font = pygame.font.SysFont('comicsans', 60)
        text = font.render(message, 1, color)
        text_rect = text.get_rect(center = position)
        self.window.blit(text, text_rect)

        pygame.display.update()
    
    def reset_game(self):
        pass

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()