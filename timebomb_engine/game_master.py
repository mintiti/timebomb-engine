import timebomb_engine.core as core
from random import sample

class GameMaster:
    def __init__(self,numbers_players,players):
        self.number_players = numbers_players
        self.players = self.create_players(players)
        self.deck = self.initialize_deck()

    def initialize_deck(self):
        if(self.number_players==4):
            Deck = core.Deck(cables=15, defusers=4)
        elif (self.number_players == 5):
            Deck = core.Deck(cables=19, defusers=5)
        elif (self.number_players == 6):
            Deck = core.Deck(cables=23, defusers=6)
        elif (self.number_players == 7):
            Deck = core.Deck(cables=27, defusers=7)
        elif (self.number_players == 8):
            Deck = core.Deck(cables=31, defusers=8)
        return Deck

    def create_players(self, players):
        if (self.number_players == 4):
            nb_terrorist_cards = 2
            nb_counter_terrorist_cards = 3
        elif (self.number_players == 5):
            nb_terrorist_cards = 2
            nb_counter_terrorist_cards = 3
        elif (self.number_players == 6):
            nb_terrorist_cards = 2
            nb_counter_terrorist_cards = 4
        elif (self.number_players == 7):
            nb_terrorist_cards = 3
            nb_counter_terrorist_cards = 5
        elif (self.number_players == 8):
            nb_terrorist_cards = 3
            nb_counter_terrorist_cards = 5

        roles = sample([0] * nb_terrorist_cards + [1] * nb_counter_terrorist_cards, k=self.number_players)

        players = [core.Player(player,role)for player,role in zip(players,roles)]
        return players