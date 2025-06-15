import pygame
from board import Board
from score import save_result, get_score_summary


class Game:

    def __init__ (self, screen):

        self.screen = screen
        self.board= Board()
        self.clock = pygame.time.Clock()
        self.running = True

