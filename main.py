import pygame
import sys
from menu import main_menu
#from game import Game

pygame.init()

WIDTH, HEIGHT= 640, 640

def main():

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Szachy")


    While True:

        main_menu(screen)



    if __name__ == '__main__':
        main()