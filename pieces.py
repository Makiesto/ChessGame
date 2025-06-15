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
