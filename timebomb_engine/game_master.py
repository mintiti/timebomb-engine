import timebomb_engine.core as core
from random import sample
import random
from itertools import cycle

class GameMaster:

    def __init__(self,numbers_players,players):
        self.number_players = numbers_players
        self.players = self._create_players(players)
        self.deck = self._initialize_deck()
        self.turn_id = self._select_player_turn()
        self.round_number = 0
        self._distribute_cards()

    def _initialize_deck(self):
        if self.number_players==4:
            Deck = core.Deck(cables=15, defusers=4)
        elif self.number_players == 5:
            Deck = core.Deck(cables=19, defusers=5)
        elif self.number_players == 6:
            Deck = core.Deck(cables=23, defusers=6)
        elif self.number_players == 7:
            Deck = core.Deck(cables=27, defusers=7)
        elif self.number_players == 8:
            Deck = core.Deck(cables=31, defusers=8)
        return Deck

    def _create_players(self, players):
        if self.number_players == 4:
            nb_terrorist_cards = 2
            nb_counter_terrorist_cards = 3
        elif self.number_players == 5:
            nb_terrorist_cards = 2
            nb_counter_terrorist_cards = 3
        elif self.number_players == 6:
            nb_terrorist_cards = 2
            nb_counter_terrorist_cards = 4
        elif self.number_players == 7:
            nb_terrorist_cards = 3
            nb_counter_terrorist_cards = 5
        elif self.number_players == 8:
            nb_terrorist_cards = 3
            nb_counter_terrorist_cards = 5

        roles = sample([0] * nb_terrorist_cards + [1] * nb_counter_terrorist_cards, k=self.number_players)

        players = [core.Player(player,role)for player,role in zip(players,roles)]
        return players

    def _select_player_turn(self):
        return random.randint(0,self.number_players-1)

    def _distribute_cards(self):
        self.deck.shuffle()
        distribution_cycle = cycle(range(self.number_players))
        for i,player in zip(range(self.number_players-round*(5-round)),distribution_cycle):
            card = self.deck.get_top_card()
            self.players[player].give_card(card)
