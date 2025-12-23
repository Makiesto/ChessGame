# ChessGame

PL

Gra w Szachy — Python + Pygame
Interaktywna, dwuwymiarowa gra w szachy stworzona w języku Python z wykorzystaniem biblioteki Pygame. Projekt zawiera pełną logikę gry, obsługę dźwięków, menu startowe, ekran końcowy oraz system zapisywania wyników.

Funkcje:
- Pełna obsługa zasad gry w szachy (w tym szach i mat)
- Intuicyjny interfejs graficzny oparty na Pygame
- Efekty dźwiękowe dla ruchów i szacha
- Menu główne oraz ekran końcowy z opcją powrotu lub podglądu wyników
- Zapisywanie wyników do pliku results.txt
- System zliczający zwycięstwa białych i czarnych

Struktura projektu:
main.py              # Główna pętla aplikacji, menu i uruchomienie gry
game.py              # Logika rozgrywki, wyświetlanie ekranu końcowego
board.py             # Obsługa planszy i zasad gry
pieces.py            # Klasy figur szachowych i ich ruchy
menu.py              # Ekran menu startowego
score.py             # Zapisywanie i zliczanie wyników
assets/              # Folder z grafiką i dźwiękami
results.txt          # Plik z wynikami gier

ENG

Chess Game — Python + Pygame
A fully interactive 2D chess game built with Python and Pygame. This project includes full chess logic, sound effects, a graphical interface, a main menu, an endgame screen, and result tracking.

Features:
- Complete chess rules implementation (check, checkmate, etc.)
- User-friendly GUI built with Pygame
- Sound effects for moves and checks
- Main menu and endgame screen with options to return or view scores
- Saves game results to results.txt
- Score tracking for white and black wins

Project Structure:
main.py              # Main game loop and launcher
game.py              # Core gameplay logic and UI
board.py             # Board handling and rules
pieces.py            # Chess piece classes and movement
menu.py              # Main menu screen
score.py             # Result saving and score summary
assets/              # Sounds and graphics
results.txt          # Saved game results
