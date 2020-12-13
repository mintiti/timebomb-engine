from collections import deque
from random import shuffle
from typing import Iterable


# Basic game roles and card types
class Role:
    """
    Class representing the role of a player.
    The role is either Terrorist (wants to find the bomb) or Counter-terrorist (wants to defuse the bomb)
    """
    TERRORIST = 0
    COUNTER_TERRORIST = 1
    NAME = {
        0: "Terrorist",
        1: "Counter-terrorist"
    }

    def __init__(self, role):
        assert role in [0, 1], "Player role must be either 0 (Terrorist) or 1 (Counter Terrorist)"
        self.role = role

    def __eq__(self, other):
        return isinstance(other, Role) & other.role == self.role

    def __str__(self):
        return f"{Role.NAME[self.role]}"


class CardType:
    """
    Class representing the type of the card.
    This can be either of those :
        - 0 : Bomb
        - 1 : Defuser
        - 2 : Cable
    """
    BOMB = 0
    DEFUSER_CABLE = 1
    NORMAL_CABLE = 2

    NAME = {
        0: "Bomb",
        1: "Defuser",
        2: "Cable"
    }

    def __init__(self, card_type):
        assert card_type in [0, 1, 2], "card_type has to be either 0 (Bomb), 1 (Defuser) or 2 (Cable)."
        self.card_type = card_type

    def __eq__(self, other):
        return isinstance(other, CardType) & other.card_type == self.card_type

    def __str__(self):
        return f"{CardType.NAME[self.card_type]}"


# Interface definition
class AbstractCard:
    """
    Interface for objects representing individual cards in a deck.

    Attributes:
        id : (int) A unique card identifier
        card_type : (CardType) The card type
        is_hidden : (bool) Whether the card is face down
    """
    BOMB = CardType.BOMB
    DEFUSER_CABLE = CardType.DEFUSER_CABLE
    NORMAL_CABLE = CardType.NORMAL_CABLE

    NAME = CardType.NAME

    @property
    def card_type(self) -> CardType:
        """
        Return the type of card the object is.
        Returns:
            card_type: (int) An int refering to the type of card, e.g. 1 is a defuser cable, 0 is a bomb, ...

        """
        raise NotImplementedError

    @property
    def id(self) -> int:
        """
        Returns the unique card identifier corresponding to this card
        Returns:
            id : (int) The unique id attributed to this card

        """
        raise NotImplementedError

    @property
    def is_hidden(self) -> bool:
        """
        Returns whether this card is face down or not.
        Returns:
            is_hidden : (bool) True if the card is face down, False if it's face up
        """
        raise NotImplementedError


class CardSet:
    """
    Interface for a set of cards, which is a collection of AbstractCard objects. It is responsible for initializing itself and its cards.
    You need to implement the collection as an iterable of your choice

    Methods:
        shuffle: Shuffle the deck of cards
        get_card : Get a card from the deck
    """

    def shuffle(self) -> None:
        """Shuffle the cards"""
        shuffle(self.collection)

    @property
    def collection(self) -> Iterable:
        raise NotImplementedError

    def __len__(self):
        return len(self.collection)

    def __iter__(self):
        return iter(self.collection)


class AbstractPlayer:
    """
    Interface for a player in a game.

    Attributes
        id: (int) Unique player identifier
        role : (Role) the role of the player
        hand : (PlayerHand) The cards the player has in hand
        announced : () The cards that the player has announced having

    Methods:
        shuffle_hand : shuffle the player's hand
    """

    @property
    def player_id(self) -> int:
        raise NotImplementedError

    @property
    def role(self) -> Role:
        raise NotImplementedError

    @property
    def hand(self) -> "PlayerHand":
        raise NotImplementedError

    @property
    def announced(self) -> "CardSet":
        raise NotImplementedError


# Concrete implementations


class Card(AbstractCard):

    def __init__(self, card_type, card_id):
        assert card_type in range(3), "card type must be an int in [0,2]"
        self._card_type = CardType(card_type)
        self._id = card_id
        self._is_hidden = True

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def card_type(self) -> CardType:
        return self._card_type

    @card_type.setter
    def card_type(self, value):
        self._card_type = value

    @property
    def is_hidden(self) -> bool:
        return self._is_hidden

    @is_hidden.setter
    def is_hidden(self, value):
        self._is_hidden = value

    def __str__(self):
        return f"Card {self.id} type {Card.NAME[self.card_type]}"


class Deck(CardSet):

    def __init__(self, cables=15, defusers=4, bomb=1):
        self._number_of_cards = cables + defusers + bomb
        self._deck = deque(maxlen=self._number_of_cards)

        # Initialize the deck
        self._init_deck(cables, defusers)

    def _init_deck(self, cables, defusers):
        # Initialize the deck
        index = 0
        while len(self) < cables:
            cable = Card(Card.NORMAL_CABLE, index)
            self.collection.append(cable)
            index += 1
        while len(self) < cables + defusers:
            defuser = Card(Card.DEFUSER_CABLE, index)
            self.collection.append(defuser)
            index += 1
        while len(self) < self._number_of_cards:
            bomb = Card(Card.BOMB, index)
            self.collection.append(bomb)
            index += 1

        self.shuffle()

    @property
    def collection(self) -> Iterable:
        return self._deck

    @collection.setter
    def collection(self, value):
        self._deck = value

    def get_top_card(self) -> AbstractCard:
        """
        Get the top card in the deck
        Returns: (AbstractCard) The top card in the deck

        Raises:
            IndexError if the deck is empty

        """
        return self._deck.popleft()


class PlayerHand(CardSet):

    def __init__(self):
        self._card_set = []

    @property
    def collection(self) -> Iterable:
        return self._card_set

    @collection.setter
    def collection(self, value):
        self.collection = value

    def append(self, item):
        self.collection.append(item)

    def __getitem__(self, item):
        return self.collection[item]

    def show_card(self, index) -> CardType:
        """
        Show the designated card in the player's hand.
        Args:
            index: index of the card yoiu wish to flip and see

        Returns:

        """
        card = self[index]
        card.is_hidden = False
        return card.card_type


class Player(AbstractPlayer):

    def __init__(self, player_id, role):
        self._player_id = player_id
        self._role = Role(role)
        self._hand = PlayerHand()
        self._announced = None

    @property
    def player_id(self) -> int:
        return self._player_id

    @player_id.setter
    def player_id(self, value):
        self._player_id = value

    @property
    def role(self) -> Role:
        return self._role

    @role.setter
    def role(self, value):
        self._role = value

    @property
    def hand(self) -> "PlayerHand":
        return self.hand

    @hand.setter
    def hand(self, value):
        self._hand = value

    @property
    def announced(self) -> "CardSet":
        return self._announced

    @announced.setter
    def announced(self, value):
        self._announced = value
