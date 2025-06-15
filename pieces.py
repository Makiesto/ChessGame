import pygame

# Wczytywanie obrazków figur do słownika piece_images
piece_images = {}
SQUARE_SIZE = 640 // 8  # Plansza 640x640 pixeli

figures_symbols = ["p", "r", "n", "b", "q", "k"]
figures_colors = ['w', 'b']

for name in figures_symbols:
    for color in figures_colors:
        key = color + name
        piece_images[key] = pygame.transform.scale(pygame.image.load(f"assets/images/{key}.png"),
                                                   (SQUARE_SIZE, SQUARE_SIZE))


class Piece:
    """
    Klasa bazowa dla wszystkich figur
    """

    def __init__(self, color):
        """
        Inicjalizacja figury
        :param color: 'w' dla białej figury, 'b' dla czarnej.
        """

        self.color = color
        self.moved = False  # Funkcjonalnosc dla roszady

    def draw(self, win, row, col, size):
        """
        Rysuje figure na planszy.
        :param win: powierzchnia pygame
        :param row: wiersz planszy
        :param col: kolumna planszy
        :param size: rozmiar pojedynczego pola
        """

        piece_code = self.get_piece_code()
        image = piece_images[self.color + piece_code]
        win.blit(image, (col * size, row * size))

    def get_piece_code(self):
        """
        Zwraca jednoznaczny skrót figury (np. 'r' dla wieży)
        """
        piece_map = {
            'Pawn': 'p',
            'Rook': 'r',
            'Knight': 'n',
            'Bishop': 'b',
            'Queen': 'q',
            'King': 'k'
        }

        return piece_map[self.__class__.__name__]

    def get_moves(self, row, col, board):
        """
        Zwraca liste legalnych ruchów dla figury
        :param row: wiersz planszy
        :param col: kolumna planszy
        :param board: dwuwymiarowa lista z figurami
        :return: legalne ruchy
        """
        return []


class Pawn(Piece):
    """
    Klasa reprezentująca pionka
    """

    def get_moves(self, row, col, board):
        """
        Zwraca możliwe ruchy piona, uwzględniając ruch o 1 lub 2 pola oraz bicia na ukos.
        :param row: wiersz planszy
        :param col: kolumna planszy
        :param board: dwuwymiarowa lista z figurami (lub None)
        :return: legalne ruchy
        """

        moves = []
        direction = -1 if self.color == 'w' else 1
        start_row = 6 if self.color == 'w' else 1

        # Ruch do przodu o jedno pole
        if 0 <= row + direction < 8 and board[row + direction][col] is None:
            moves.append((row + direction, col))

            # Ruch o dwa pola ze startowej pozycji
            if row == start_row and board[row + 2 * direction][col] is None:
                moves.append((row + 2 * direction, col))

        # Bicie na ukos
        for dc in [-1, 1]:
            nr, nc = row + direction, col + dc
            if 0 <= nr < 8 and 0 <= nc < 8:
                if board[nr][nc] and board[nr][nc].color != self.color:
                    moves.append((nr, nc))

        return moves


class Rook(Piece):
    """
    Klasa reprezentująca wieżę
    """

    def get_moves(self, row, col, board):
        """
        Zwraca możliwe ruchy wieży w linii prostej.
        :param row: wiersz planszy
        :param col: kolumna planszy
        :param board: dwuwymiarowa lista z figurami (lub None)
        :return: legalne ruchy
        """

        return self._linear_moves(row, col, board, [(-1, 0), (1, 0), (0, -1), (0, 1)])

    def _linear_moves(self, row, col, board, directions):
        """
        Zwraca ruchy w podanych kierunkach
        :param row: wiersz planszy
        :param col: kolumna planszy
        :param board: dwuwymiarowa lista z figurami (lub None)
        :param directions: kierunki
        :return: legalne ruchy
        """

        moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != self.color:
                    moves.append((r, c))  # można bić
                    break
                else:
                    break  # zablokowany przez wlasną figurę

                r += dr
                c += dc

        return moves


class Bishop(Rook):
    """
    Klasa reprezentująca gońca.
    """

    def get_moves(self, row, col, board):
        """
        Goniec porusza się tylko po przekątnych.
        :param row: wiersz planszy
        :param col: kolumna planszy
        :param board: dwuwymiarowa lista z figurami (lub None)
        :return: legalne ruchy
        """

        return self._linear_moves(row, col, board, [(-1, -1), (-1, 1), (1, -1), (1, 1)])


class Queen(Rook):
    """
    Klasa reprezentująca hetmana (królowa).
    """

    def get_moves(self, row, col, board):
        """
        Hetman porusza się jak wieża + goniec.
        :param row: wiersz planszy
        :param col: kolumna planszy
        :param board: dwuwymiarowa lista z figurami (lub None)
        :return: legalne ruchy
        """

        return self._linear_moves(
            row, col, board, [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        )


class Knight(Piece):
    """
    Klasa reprezentująca skoczka.
    """

    def get_moves(self, row, col, board):
        """
        Skoczek porusza się w kształcie litery 'L'.
        :param row: wiersz planszy
        :param col: kolumna planszy
        :param board: dwuwymiarowa lista z figurami (lub None)
        :return: legalne ruchy
        """

        moves = []
        for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] is None or board[r][c].color != self.color:
                    moves.append((r, c))

        return moves
