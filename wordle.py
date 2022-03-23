import random
import pygame
import words


def main():
    width, height = 435, 570
    pygame.init()
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Wordle Clone')
    game = Game(surface)
    game.play()
    pygame.quit()


class Game():
    def __init__(self, surface):
        self.surface = surface
        self.bg_color = (18, 18, 18)
        self.font = pygame.font.SysFont('Ariel', 70)

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.run = True

        self.secret_word = words.WORDS[random.randint(0, len(words.WORDS))].upper()

        self.board = [
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ']]

        self.attempt = 0
        self.letter = 0
        self.active_attempt = True
        self.game_over = False

    def play(self):
        while self.run:
            self.handle_events()
            self.draw()
            self.game_Clock.tick(self.FPS)

    def draw(self):
        self.surface.fill(self.bg_color)
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                pygame.draw.rect(self.surface, (60, 60, 60), [col * 85 + 10, row * 85 + 10, 75, 75], 2)

                if self.board[row][col] == self.secret_word[col] and row < self.attempt:
                    pygame.draw.rect(self.surface, (80, 140, 80), [col * 85 + 10, row * 85 + 10, 75, 75])
                elif self.board[row][col] in self.secret_word and row < self.attempt:
                    pygame.draw.rect(self.surface, (180, 160, 60), [col * 85 + 10, row * 85 + 10, 75, 75])
                elif row < self.attempt:
                    pygame.draw.rect(self.surface, (60, 60, 60), [col * 85 + 10, row * 85 + 10, 75, 75])

                text = self.font.render(self.board[row][col], True, (255, 255, 255))
                self.surface.blit(text, (col * 85 + 30, row * 85 + 25))
                
        pygame.display.update()

    def check_win(self):
        if ''.join(self.board[self.attempt - 1]) == self.secret_word:
            print('win')
            self.game_over = True
        elif self.attempt > 5:
            print('lose')
            self.game_over = True

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.run = False

            if event.type == pygame.KEYDOWN and not self.game_over:

                if event.key == pygame.K_RETURN and self.letter == 5:
                    self.attempt += 1
                    self.letter = 0
                    self.active_attempt = True
                    self.check_win()

                elif event.key == pygame.K_BACKSPACE and self.letter > 0:
                    self.board[self.attempt][self.letter - 1] = ' '
                    self.letter -= 1

            if event.type == pygame.TEXTINPUT and self.active_attempt and not self.game_over:
                key = event.__getattribute__('text')
                if key.isalpha():
                    self.board[self.attempt][self.letter] = key.upper()
                    self.letter += 1

            if self.letter == 5:
                self.active_attempt = False
            if self.letter < 5:
                self.active_attempt = True


if __name__ == "__main__":
    main()
