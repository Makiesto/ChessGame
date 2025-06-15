import pygame
import sys
from game import Game
from menu import main_menu

pygame.init()

#stałe określające rozmiar okna gry
WIDTH, HEIGHT= 640, 640

def main():
    """
    Główna funkcja uruchamiająca aplikację
    Tworzy okno Pygame, wyświetla menu, a następnie uruchami grę.
    Po zaończeniu gry wraca do menu i pozwal na ponowną rozgrywkę.

    """


    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Szachy")


    While True:
        #wyswietlanie menu głównego
        main_menu(screen)

        # utworzenie i uruchaminai instancji gry
        game = Game(screen)
        game.run()


    if __name__ == '__main__':
        #uruchamianie funkcji main tylko gdy skrypt jest wykonany bezposrednio
        main()