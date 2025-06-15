def save_result(winner_color):
    """
    Zaposuje wynik gry do pliku tekstowego 'results.txt'
    Dodaje linię informującą o zwyciężcy (np. "Zwyciężca: Białe").

    :param winner_color: kolor zwyciężcy ("Białe" lub "Czarne")
    :return:
    """

    with open("results.txt", "a", encoding="utf-8") as file:
        file.write(f"Zwyciężca: {winner_color}\n")

# def get_score_summary():
#     """
#     Odczytuje plik 'results.txt
#     :return:
#     """