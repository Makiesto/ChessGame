import pygame
from board import Board
from score import save_result, get_score_summary


class Game:

    def __init__ (self, screen):

        self.screen = screen
        self.board= Board()
        self.clock = pygame.time.Clock()
        self.running = True

def run(self):

    while self.running:
        self.clock.tick(60)

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                self.running = False
            elif event.type ==pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                row,col = y // self.board.square_size, x // self.board.square_size
                self.board.select(row, col)

        self.board.draw(self.screen)
        pygame.display.update()


        if self.board.winner:

            self.display_winner(self.board.winner)
            save_result(self.board.winner)
            self.wait_for_postgame_action()
            self.running =False


