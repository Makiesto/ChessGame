import pygame
import sys

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)


def main_menu(screen)

    font = pygame.font.SysFont("arial", 30)
    small_font = pygame.font.SysFont("arial",20)



    while True:

        screen.fill(WHITE)

        title =font.render("Witamy w grze szachy", True, BLACK)
        play_text = small_font.render("Nacisnij SPACJĘ, aby rozpocząć", True, BLUE)
        quit_text = small_font.render("naciśnij ESC, aby wyjść", True, BLUE)


        screen.blit(title,((640-title.get_width()) // 2,200))
        screen.blit(play_text,((640-title.get_width()) // 2,300))
        screen.blit(quit_text, ((640-title.get_width()) // 2,350))

        pygame.display.update()

