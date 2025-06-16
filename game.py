import pygame

from board import Board
from score import save_result, get_score_summary


class Game:
    """
    Klasa reprezentująca logikę gry szachowej wraz z interfejsem graficznym i dźwiękiem.
    Zarządza przebiegiem gry, obsługuje zdarzenia użytkownika, rysowanie oraz ekran końcowy.
    """

    def __init__(self, screen):
        """
        Inicjalizacja gry: ustawienie planszy, zegara, dźwięków oraz głównej pętli.

        """
        self.screen = screen
        self.board = Board()
        self.clock = pygame.time.Clock()
        self.running = True

        # Inicjalizacja dźwięków gry
        pygame.mixer.init()
        self.move_sound = pygame.mixer.Sound("assets/sounds/move_sound.wav")
        self.check_sound = pygame.mixer.Sound("assets/sounds/check_sound.mp3")

        # przechowywanie metody wykonania ruchu, aby dodać efekty dźwiękowe
        self.original_movie_piece = self.board.move_piece
        self.board.movie_piece = self.wrapped_move_piece

    def wrapped_move_piece(self, start, end):
        """
        Zastępcza metoda wykonująca ruch, dodająca dźwięki ruchu i szacha.

        :param start: współrzędne pola początkowego (rząd, kolumna)
        :param end: współrzędne pola końcowego (rząd, kolumna)

        """
        current_turn = self.board.turn
        self.original_movie_piece(start, end)
        self.move_sound.play()
        # Jeśli po ruchu przeciwnik jestw szachu, odtwórz dźwięk
        if self.board.is_check(self.board.turn):
            self.check_sound.play()

    def run(self):
        # Główna petla gry. Obsługuje zdarzenia, rysuje i sprawdza warunki zakończenia.
        while self.running:
            self.clock.tick(60)

            # Obsługa zdarzeń (zamknięcię okna, kliknięcie myszy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // self.board.square_size, x // self.board.square_size
                    self.board.select(row, col)
            # Rysowanie planszy i aktualizacja okna
            self.board.draw(self.screen)
            pygame.display.update()

            # Sprawdzenie czy gra się zakończyła
            if self.board.winner:
                self.display_winner(self.board.winner)
                save_result(self.board.winner)
                self.wait_for_postgame_action()
                self.running = False

    def display_winner(self, winner):

        """
         Wyświetla ekran końcowy z informacją o zwycięzcy lub remisie.
        : param winner: tekst informujący o zwycięzcy ("Białe", "czarne", "remis")
        """

        font = pygame.font.SysFont("arial", 36)
        if self.board.is_insufficient_material():
            text = font.render("Remis!", True, (255, 255, 0))
        else:
            text = font.render(f"Szach Mat! Wygrywają {winner}", True, (255, 0, 0))

        self.screen.fill((0, 0, 0))
        self.screen.blit(text, ((640 - text.get_width()) // 2, 200))

        # Rysowanie przyciskó gry
        button_font = pygame.font.SysFont("arial", 28)

        menu_text = button_font.render("Powrót do menu", True, (255, 255, 255))
        menu_rect = pygame.Rect(195, 280, 250, 50)
        pygame.draw.rect(self.screen, (100, 100, 100), menu_rect)
        self.screen.blit(menu_text, (menu_rect.x + 20, menu_rect.y + 10))

        score_text = button_font.render("Tabela wyników", True, (255, 255, 255))
        score_rect = pygame.Rect(195, 350, 250, 50)
        pygame.draw.rect(self.screen, (100, 100, 100), score_rect)
        self.screen.blit(score_text, (score_rect.x + 20, score_rect.y + 10))

        pygame.display.update()

        self.menu_button = menu_rect
        self.score_button = score_rect


    def wait_for_postgame_action(self):
        """Oczekuje na wybór użytkownika po zakonczeniu gry
        - powrót do menu
        - wyświetlenie tabeli wyników (potem znów powrót do wyboru)
        """
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if self.menu_button.collidepoint(x, y):
                        waiting = False
                    elif self.score_button.collidepoint(x, y):
                        self.display_score_table()
                        # Po powrocie z tabeli wyników, odśwież ekran końcowy gry
                        self.display_winner(self.board.winner)


    def display_score_table(self):
        """
        Wyświetla tabelę wyników z licznikami zwycięstw białych i czarnych        :param self:

        """

        white_wins, black_wins = get_score_summary()
        self.screen.fill((20, 20, 20))

        font = pygame.font.SysFont("arial", 32)
        title = font.render("Tabela wyników", True, (255, 255, 255))
        self.screen.blit(title, ((640 - title.get_width()) // 2, 50))

        # Etykiety i wartości punktów
        label_font = pygame.font.SysFont("arial", 26)
        label1 = label_font.render("Białe", True, (255, 255, 255))
        label2 = label_font.render("Czarne", True, (255, 255, 255))

        score_font = pygame.font.SysFont("arial", 24)
        white_text = score_font.render(f"{white_wins}", True, (200, 200, 200))
        black_text = score_font.render(f"{black_wins}", True, (200, 200, 200))

        self.screen.blit(label1, (180, 150))
        self.screen.blit(white_text, (200, 190))
        self.screen.blit(label2, (400, 150))
        self.screen.blit(black_text, (420, 190))

        # Notka informacyjna
        note_font = pygame.font.SysFont("arial", 20)
        note = note_font.render("Kliknij gdziekolwiek, aby wrócić", True, (160, 160, 160))
        self.screen.blit(note, ((640 - note.get_width()) // 2, 500))

        pygame.display.update()

        # Czekaj na kliknięcie, aby powrocic
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
