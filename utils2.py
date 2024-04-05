import random

from PIL import Image, ImageDraw, ImageFont


class CardDeck:
    def __init__(self):
        self.suits = ['hearts', 'diamonds', 'clubs', 'spades']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.deck = [(suit, rank) for suit in self.suits for rank in self.ranks]
        self.drawn_cards = []  # 抽了的牌

    def shuffle(self):
        random.shuffle(self.deck)
        self.drawn_cards.clear()

    def draw_card(self):
        if len(self.deck) == 0:
            raise ValueError("Deck is empty. Cannot draw more cards.")
        suit, rank = self.deck.pop()
        self.drawn_cards.append((suit, rank))
        return suit, rank

    def draw_cards(self, n):
        if len(self.deck) < n:
            raise ValueError(f"Cannot draw {n} cards from a deck with only {len(self.deck)} cards.")
        cards = [self.draw_card() for _ in range(n)]

        # Sorting key function for tuples (suit, rank)
        def sort_key(card_tuple):
            suit, rank = card_tuple
            return self.ranks.index(rank), self.suits.index(suit)

        cards.sort(key=sort_key)
        sorted_cards = [Card(suit, rank) for suit, rank in cards]

        return sorted_cards


class Card:
    BACK_IMAGE_PATH = 'assets/cards/back.jpg'

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.image_path = f'assets/cards/{suit}/{suit}{rank}.png'
        suit_map = {'h': '红心', 'd': '方块', 's': '黑桃', 'c': '梅花'}
        self.description = f'{suit_map.get(suit[0])}{rank}'


if __name__ == '__main__':
    deck = CardDeck()
    deck.shuffle()  # 洗牌
    for _ in range(5):
        drawn_cards = deck.draw_cards(2)  # 抽取5张牌
        print(drawn_cards)
