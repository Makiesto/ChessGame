def save_result(winner_color):
    """
    Zaposuje wynik gry do pliku tekstowego 'results.txt'
    Dodaje linię informującą o zwyciężcy (np. "Zwyciężca: Białe").

    :param winner_color: kolor zwyciężcy ("Białe" lub "Czarne")
    :return:
    """

    with open("results.txt", "a", encoding="utf-8") as file:
        file.write(f"Zwyciężca: {winner_color}\n")


def get_score_summary():
    """
    Odczytuje plik 'results.txt' i zlicza, ile razy wygrały białe i czarne figury.
    :return: krotka (white_wins, black_wins), gdzie każdy element to liczba zwycięstw danego koloru
    """

    try:
        with open("results.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

            # Zlicz wystąpienie słó∑ "Biale" i "Czarne" w każdej linii
            white_wins = sum(1 for line in lines if "Białe" in line)
            black_wins = sum(1 for line in lines if "Czarne" in line)

        return white_wins, black_wins

    # Obsługa przypadku, gdy plik jeszcze nie istnieje (np. pierwsze uruchomienie)
    except FileNotFoundError:
        return 0, 0
