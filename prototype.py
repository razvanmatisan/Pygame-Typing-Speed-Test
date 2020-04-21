import pygame
from pygame.locals import *
import time
import random

WIDTH = 800
HEIGHT = 600
RED = (255, 0, 0)
YELLOW = (230, 230, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

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
        self.high_score = 0
        self.speed = 0
        self.accuracy = 0

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
        while self.running:
            self.reset_game()
            self.first_page()

    def first_page(self):
        self.window.blit(self.background, (0, 0))
        start_button = button(RED, 310, 265, 200, 100, "Start")

        start_button.draw(self.window, BLACK)
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
                    self.main_page()
        pygame.display.update()
    
    def main_page(self):
        self.window.blit(self.background, (0, 0))
        pygame.display.update()

        start = 60
        dt = 0

        running = True
        enabled = True
        active = False
        start_game = False
        end_game = False
        actual_word = ''

        while running:
            pygame.display.update()
            self.window.blit(self.background, (0, 0))
            self.draw_text(YELLOW, "Time: " + str(int(start)), (400, 50), 60)
            self.draw_text(YELLOW, "Highscore: " + str(int(self.high_score)), (65, 20), 30)

            pygame.display.update()

            #Se genereaza cate un cuvant la o apasare pe tasta ENTER
            if enabled:
                random_word = self.random_words()
                self.input_words.append(random_word)
                enabled = False
            self.draw_text(YELLOW, random_word, (400, 215), 60)

            #Desenare cuvant din fisier + chenarul in care trebuie scrise cuvintele
            pygame.draw.rect(self.window, WHITE, (250, 300, 300, 50), 5)
            self.draw_text(YELLOW, actual_word, (400, 325), 60)

            #Countdown-ul incepe numai cand se apasa pe dreptunghi
            if start_game:
                clock = pygame.time.Clock()
                self.draw_text((230, 230, 0), "Time: " + str(int(start)), (400, 50), 60)
                start -= dt
                #Aici trebuie sa incluzi rezultatele
                if start <= 0:
                    start = 0
                    if end_game:
                        self.print_results() # Se afiseaza acuratetea, viteza (High_score-ul se va afisa mereu, tu doar tb sa l actualizezi aici)
                        try_again_button = button(RED, 400, 475, 300, 100, "Try Again")
                        try_again_button.draw(self.window, BLACK)

                        pos = pygame.mouse.get_pos()
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                self.running = False
                                pygame.quit()
                                quit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if try_again_button.isOver(pos):
                                    running = False
                    pygame.display.update()
                dt = clock.tick(30) / 100

            if start == 0:
                end_game = True
                #self.user_words.append(actual_word)
                #actual_word = ''

            if not end_game:
                pos = pygame.mouse.get_pos()
                events = pygame.event.get()

                for event in events:
                    #Butonul de inchidere
                    if event.type == pygame.QUIT:
                        running = False
                        pygame.quit()
                        quit()
                    #Apasare de mouse (daca se apasa pe chenar, se afiseaza countdown-ul)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pos[0] > 250 and pos[0] < 250 + 300 and pos[1] > 300 and pos[1] < 300 + 50:
                            active = True
                            start_game = True
                            

                    if event.type == pygame.KEYDOWN:
                        if active:
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
    
    # Metoda care afiseaza in joc rezultatele
    # Aici se vor calcula viteza si acuratetea
    # Am adaugat si o variabila in __init__ numita high_score
    # (o poti folosi ca numar de cuvinte scrise perfect --> va ramane salvata cat timp se da reset la joc)
    def print_results(self):
        count = 0 # nr de litere corecte de la user
        completely_correct = 0 #nr de cuvinte complet corecte
        total_len = 0 # nr total de litere din input
        for i, c in enumerate(self.user_words):
            j = 0
            extra = 0 #lotere care depasesc lungimea cuvantului
            for k, letter in list(enumerate(c)):
                if j < int(len(self.input_words[i])):
                    if self.input_words[i][j] == letter:
                        count += 1
                    j += 1
                else:
                    extra = len(c) - len(self.input_words[i])
                    count -= extra
                
            if c:
                total_len += len(self.input_words[i])
                
            if self.input_words[i] == c:
                completely_correct += 1
        
        self.accuracy = count/total_len * 100

        print(total_len)
        print(count)

        for word in self.user_words:
            if word:
                print(word)
                self.speed += 1
        
        #  self.speed = len(self.user_words)
      
        self.draw_text(RED, "Speed: " + str(int(self.speed)) + " wpm", (100, 20), 30)
        self.draw_text(RED, str(int(self.accuracy)), (400, 150), 50)

        print(self.input_words)
        print(self.user_words)
        pygame.display.update()
        #pass

    # Se afiseaza pe ecran un anumit mesaj
    def draw_text(self, color, message, position, dim):
        font = pygame.font.SysFont('comicsans', dim)
        text = font.render(message, 1, color)
        text_rect = text.get_rect(center = position)
        self.window.blit(text, text_rect)

        pygame.display.update()
    
    def reset_game(self):
        self.input_words = []
        self.user_words = []
        self.accuracy = 0
        self.speed = 0

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()