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
            self.legal_moves = self.get_legal_moves(row, col)

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

        if self.is_checkmate(self.turn):
            self.winner = 'Białe' if self.turn == 'b' else 'Czarne'
        elif self.is_insufficient_material():
            self.winner = "Remis"

    def get_legal_moves(self, row, col):
        """
        Zwraca listę legalnych ruchów figury (bez pozostawienia króla w szachu).
        :param row: wspolerzedna 1 (wiersz)
        :param col: wspolerzedna 2 (kolumna)
        """

        figure = self.board[row][col]
        moves = figure.get_moves(row, col, self.board)
        legal = []

        # Sprawdzenie każdego ruchu symulująć go
        for move in moves:
            er, ec = move
            taken = self.board[er][ec]
            self.board[er][ec] = figure
            self.board[row][col] = None
            if not self.is_check(figure.color):
                legal.append(move)
            self.board[row][col] = figure
            self.board[er][ec] = taken

        # Roszada
        if isinstance(figure, King) and not figure.moved:
            wiersz = 7 if figure.color == 'w' else 0

            # Krótka roszada
            rook_k = self.board[wiersz][7]
            if isinstance(rook_k, Rook) and not rook_k.moved:
                if all(self.board[wiersz][c] is None for c in [5, 6]):
                    if not any(self.is_square_attacked(wiersz, c, self.opponent(figure.color)) for c in [4, 5, 6]):
                        legal.append((wiersz, 6))

            # Długa roszada
            rook_d = self.board[wiersz][0]
            if isinstance(rook_d, Rook) and not rook_d.moved:
                if all(self.board[wiersz][c] is None for c in [1, 2, 3]):
                    if not any(self.is_square_attacked(wiersz, c, self.opponent(figure.color)) for c in [4, 3, 2]):
                        legal.append((wiersz, 2))

        # En passant
        if isinstance(figure, Pawn) and self.en_passant_target:
            ep_r, ep_c = self.en_passant_target
            if abs(col - ep_c) == 1 and ((figure.color == 'w' and row == 3) or (figure.color == 'b' and row == 4)):
                legal.append((ep_r, ep_c))

        return legal

    def is_check(self, color):
        """Sprawdza, czy król danego koloru jest w szachu."""
        king_pos = self.find_king(color)


    def find_king(self, color):
        """Zwraca pozycjękróla danego koloru."""
        for r in range(8):
            for c in range(8):
                f = self.board[r][c]
                if isinstance(f, King) and f.color == color:
                    return (r, c)
        return (-1, -1)

    def is_square_attacked(self, row, col, by_color):
        """
        Sprawdza, czy pole jest atakowane przez kolor.
        :param row: wspolerzedna 1 (wiersz)
        :param col: wspolerzedna 2 (kolumna)
        :param by_color: kolor, który atakuje
        :return:
        """

        for r in range(8):
            for c in range(8):
                f = self.board[r][c]
                if f and f.color == by_color:
                    if (row, col) in f.get_moves(r, c, self.board):
                        return True

        return False

    def opponent(self, color):
        """Zwraca przeciwny kolor"""
        return 'b' if color == 'w' else 'w'

    def is_checkmate(self, color):
        """Sprawdza, czy dany kolor jest zamatowany"""
        if not self.is_check(color):
            return False

        for r in range(8):
            for c in range(8):
                figure = self.board[r][c]
                if figure and figure.color == color:
                    if self.get_legal_moves(r, c):
                        return False

        return True

    def is_insufficient_material(self):
        """
        Sprawdza czy jest remis przez niewystarczający materiał:
        - Król vs król
        - Król + skoczek/goniec vs Król
        - Król + goniec vs Król + goniec (na tym samym kolorze pola)
        """

        figures = [f for row in self.board for f in row if f]

        if len(figures) == 2:
            return True # Król vs Król
        elif len(figures) == 3:
            types = [type(f) for f in figures]
            if types.count(King) == 2 and (types.count(Bishop) == 1 or types.count(Knight) == 1):
                return True
        elif len(figures) == 4:
            bishops = [f for f in figures if isinstance(f, Bishop)]
            if len(bishops) == 2:
                colors = []
                for f in range(8):
                    for c in range(8):
                        if self.board[r][c] in bishops:
                            colors.append((r + c) % 2)
                if len(set(colors)) == 1:
                    return True
        return False