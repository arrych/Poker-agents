import itertools
import random

from PIL import Image, ImageDraw, ImageFont

ranks_list = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']


class CardDeck:
    def __init__(self):
        self.suits = ['hearts', 'diamonds', 'clubs', 'spades']
        self.ranks = ranks_list
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
    isBack = False

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.rank_idx = ranks_list.index(rank)
        self.image_path = f'assets/cards/{suit}/{suit}{rank}.png'
        suit_map = {'h': '红心', 'd': '方块', 's': '黑桃', 'c': '梅花'}
        self.description = f'{suit_map.get(suit[0])}{rank}'


class BackCard(Card):
    def __init__(self):
        self.isBack = True
        self.image_path = 'assets/cards/back.jpg'


def parse_round_level(cards):
    groups = group([card.rank_idx for card in cards])
    (points, counts) = unzip(groups)

    straight = (len(counts) == 5) and (max(counts) - min(counts) == 4)
    flush = len(set([card.suit for card in cards])) == 1

    (level, description) = ((9, f'同花顺{[ranks_list[point] for point in points]}') if straight and flush else
                            (8, f'四条{ranks_list[points[0]]}') if (4, 1) == counts else
                            (7, f'葫芦，三条{ranks_list[points[0]]}带一对{ranks_list[points[1]]}') if (3,
                                                                                                      2) == counts else
                            (6, f'同花') if flush else
                            (5, f'顺子{[ranks_list[point] for point in points]}') if straight else
                            (4, f'三条{ranks_list[points[0]]}') if (3, 1, 1) == counts else
                            (3, f'一对{ranks_list[points[0]]}和一对{ranks_list[points[1]]}') if (2, 2, 1) == counts else
                            (2, f'一对{ranks_list[points[0]]}') if (2, 1, 1, 1) == counts else
                            (1, f'高牌{ranks_list[points[0]]}'))
    value = compute_cards_value(level, points)

    return value, level, description, counts, points


"""
    对于每手牌进行牌型价值计算
    ------------------------------------------------------
    这里，对计算方法进行如下说明：
    ---------------------
    | A | B | C | D | E |
    ---------------------
    其中，我们其大小顺序为：A>B>C>D>E
    （基于总共13张, 牌值为2-14, 因此牌值减2作为系数）
    对于高牌，其值最小：
        value = A*13^4 + B*13^3 + C*13^2 + D*13 + E
        对于其最大值，假设五张可能为一样（虽然不可能，但不影响结果）
        base_1 = 13^5（五张全为14 plus 1）
    对于一对(A==B)，其值肯定大于高牌：
        value = base_1 + A*13^3 + C*13^2 + D*13 + E
        对于其最大值，同上：
        base_2 = base_2 + 13^4
    对于顺子和同花，有如下讨论：
    对于顺子，仅仅考虑最大值即可：
        value = base + A
    对于同花，同高牌一样：
        value = base + A*13^4 + B*13^3 + C*13^2 + D*13 + E
    其余，如下面程序所示
    ------------------------------------------------------
    结果讨论：
    高牌：0-371293
    一对：371293-399854
    两对：399854-402051
    三条：402051-404248
    顺子：404248-404261
    同花：404261-775554
    葫芦：775554-775723
    四条：775723-775892
    同花顺：775892-775905
"""


def compute_cards_value(level, points):
    base_1 = 13 ** 5
    base_2 = base_1 + 13 ** 4
    base_3 = base_2 + 13 ** 3
    base_4 = base_3 + 13 ** 2
    base_5 = base_4 + 13

    value = 0
    if level == 1:
        value = sum([point * (13 ** (4 - i)) for i, point in enumerate(points)])
    elif level == 2:
        value = base_1 + sum([point * (13 ** (3 - i)) for i, point in enumerate(points[:2])])
    elif level == 3:
        value = base_2 + sum([point * (13 ** (2 - i)) for i, point in enumerate(points[:2])])
    elif level == 4:
        value = base_3 + points[0] * 169 + points[1] * 13 + points[2]
    elif level == 5:
        value = base_4 + points[0]
    elif level == 6:
        value = base_5 + sum([point * (13 ** (4 - i)) for i, point in enumerate(points)])
    elif level == 7:
        value = base_5 + points[0] * 13 + points[1]
    elif level == 8:
        value = base_5 + points[0] * 13 + points[1]
    elif level == 9:
        value = base_5 + points[0]

    return value


def group(cards):
    # Group the cards by rank and return as a dictionary of counts
    counter = {}
    for card in cards:
        counter[card] = counter.get(card, 0) + 1
    return sorted(counter.items(), key=lambda x: (x[1], x[0]), reverse=True)


def unzip(groups):
    return tuple(zip(*groups))


def parse_round_max(cards):
    result = []
    max_ret = None
    combs = itertools.combinations(cards, 5)
    for comb in combs:
        ret = parse_round_level(comb)
        result.append(ret)
    if result:
        max_ret = max(result, key=lambda x: (x[0], x[1]))
    return max_ret


# Example usage:
# flopcards = [{"suits": "hearts", "rank": 2}, {"suits": "hearts", "rank": 3}, {"suits": "hearts", "rank": 4}, {"suits": "hearts", "rank": 5}, {"suits": "hearts", "rank": 6}]
# parse_round_max(flopcards)


if __name__ == '__main__':
    deck = CardDeck()
    deck.shuffle()  # 洗牌
    card_count = 7  # card_count>=5
    drawn_cards = deck.draw_cards(card_count)
    print([card.description for card in drawn_cards])
    max_ret = parse_round_max(drawn_cards)
    print(max_ret)
