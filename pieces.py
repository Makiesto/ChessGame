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
