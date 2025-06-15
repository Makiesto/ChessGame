from pieces import *

# Kolory pól i podświetleń ruchów
WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Board:
    """
    Klasa reprezentująca szachownicę i logikę gry.
    """

    def __init__(self):
        """
        Inicjalizacja szachownicy 8x8, ustawienie pionków i stanu gry,
        """

        self.rows = self.cols = 8
        self.square_size = 640 // self.cols
        self.board = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.turn = 'w'  # 'w' - białe, 'b' - czarne -> białe zaczynają
        self.selected = None  # Aktualnie wybrana figura (współrzędna)
        self.legal_moves = []  # Dozwolone ruchy dla wybranej figury
        self.last_move = None  # Ostatni ruch (do podświetleń)
        self.winner = None  # Zwyciężca: 'Białe', 'Czarne', lub 'Remis'
        self.en_passant_target = None  # Pole oznaczające bicie w przelocie
        self.place_pieces()

    def place_pieces(self):
        """Ustawienie wszystkich figur na pozycjach startowych."""
        for col in range(self.cols):
            self.board[1][col] = Pawn('b')
            self.board[6][col] = Pawn('w')

        pieces_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_class in enumerate(pieces_order):
            self.board[0][col] = piece_class('b')
            self.board[7][col] = piece_class('w')

    def draw(self, win):
        """
        Rysowanie sachownicy, figur, możliwych ruchów i ostatniego ruchu.
        :param win: (pygame.Surface) powierzchnia do rysowania (okno gry)
        """

        for row in range(self.rows):
            for col in range(self.cols):
                # Rsyowanie planszy
                color = WHITE if (row + col) % 2 == 0 else GRAY
                pygame.draw.rect(win, color,
                                 (col * self.square_size, row * self.square_size, self.square_size, self.square_size))

                # Podświetalnie możliwych ruchów
                if (row, col) in self.legal_moves:
                    pygame.draw.rect(win, GREEN, (
                    col * self.square_size, row * self.square_size, self.square_size, self.square_size), 3)

                # Podświetlenie ostatniego ruchu
                if self.last_move == (row, col):
                    overlay = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                    pygame.draw.rect(overlay, (255, 0, 0, 120), overlay.get_rect(), 3)
                    win.blit(overlay, (col * self.square_size, row * self.square_size))

                # Rysowanie figury
                figura = self.board[row][col]
                if figura:
                    figura.draw(win, row, col, self.square_size)
