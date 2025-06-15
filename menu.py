import pygame
import sys

#Kolory RGB
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)


def main_menu(screen):

    """ Wyświetla głowne menu gry.
    
    Użytkownik może:
    -Nacisnąc SPACJE, aby przejść do gry.
    -Nacisnąć ESC, aby wyjść z aplikacji.
    
    Parametry:
    - screen (pygame.Surface): powierzchnia, na której rysowane jest menu.
    
    """
    #Ustawienie czcionek
    font = pygame.font.SysFont("arial", 48)
    small_font = pygame.font.SysFont("arial",30)

    #Zegar do kontroli FPS
    clock = pygame.time.Clock()

    #Główna pętla menu
    while True:
        #Wypełnienie tła na biało
        screen.fill(WHITE)

        # Renderowanie tekstów
        title =font.render("Witamy w grze szachy", True, BLACK)
        play_text = small_font.render("Nacisnij SPACJĘ, aby rozpocząć", True, BLUE)
        quit_text = small_font.render("naciśnij ESC, aby wyjść", True, BLUE)

        # Rysowanie tekstów na środku ekranu
        screen.blit(title,((640-title.get_width()) // 2,200))
        screen.blit(play_text,((640-title.get_width()) // 2,300))
        screen.blit(quit_text, ((640-title.get_width()) // 2,350))

        #Aktualizacja ekranu
        pygame.display.update()

        #Ograniczenie liczby klatek na sekunde do 30
        clock.tick(30)

        #Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:

                #Zamknięcie gry przez kliknięcię X
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_SPACE:
                    #start gry
                    return
                elif event.key == pygame.K_ESCAPE:
                    #Wyjście z gry
                    pygame.quit()
                    sys.exit()
