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

    def select(self, row, col):
        """
        Obsługuje wybór figury lub wykonanie ruchu.
        :param row: wspolerzedna 1 (wiersz)
        :param col: wspolerzedna 2 (kolumna)
        """

        if self.selected:
            if (row, col) in self.legal_moves:
                self.move_piece(self.selected, (row, col))
                self.selected = None
                self.legal_moves = []
        elif self.board[row][col] and self.board[row][col].color == self.turn:
            self.selected = (row, col)

    def move_piece(self, start, end):
        """
        Wykonuje ruch i obsługuje spejcalne przypadki takie jak roszada, promocja, en passant.
        :param start: początek ruchu
        :param end: koniec ruchu
        """

        sr, sc = start
        er, ec = end
        figure = self.board[sr][sc]

        # Roszada
        if isinstance(figure, King) and abs(sc - ec) == 2:
            if ec == 6:  # krótka roszada
                self.board[er][5] = self.board[er][7]
                self.board[er][7] = None
            elif ec == 2:  # długa roszada
                self.board[er][3] = self.board[er][0]
                self.board[er][0] = None

        # Bicie w przelocie
        if isinstance(figure, Pawn) and (er, ec) == self.en_passant_target:
            self.board[sr][ec] = None

        # Wykonanie ruchu
        self.board[er][ec] = figure
        self.board[sr][sc] = None
        figure.moved = True

        # Promocja piona
        if isinstance(figure, Pawn) and (er == 0 or er == 7):
            self.board[er][ec] = Queen(figure.color)

        # Ustawienie pola do e.p.
        self.en_passant_target = None
        if isinstance(figure, Pawn) and abs(er - sr) == 2:
            self.en_passant_target = ((sr + er) // 2, sc)

        self.last_move = end
        self.turn = 'b' if self.turn == 'w' else 'w'

        # Sprawdzanie zakończenia gry
