

import json

from trello import TrelloClient


def connect():
    with open("trello-credentials.json") as f:
        creds = json.load(f)
    return TrelloClient(**creds)


if __name__ == "__main__":

    client = connect()

    apsap_board = client.get_board("5f3fef2a37edc64a9914d8eb")
    player_list = [l for l in apsap_board.all_lists() if l.name == "Joueurs"][0]

    mutedLabel = [label for label in apsap_board.get_labels() if label.name == "Muté"][0]
    boyCard = [card for card in player_list.list_cards() if card.name == "Boy"][0]
    girlCard = [card for card in player_list.list_cards() if card.name == "Girl"][0]

    with open("players.json", encoding="utf-8") as f:
        players = json.load(f)

    for name, genre, rankS, rankD, rankM, muted in players:

        card = player_list.add_card(
            name=f"{name} ({rankS} {rankD} {rankM})",
            source=boyCard.id if genre == "H" else girlCard.id
        )
        if muted == "oui":
            card.add_label(mutedLabel)
