from rlcard.utils.utils import print_card
from random import randint
import time
import random

class Porker:
    def __init__(self):
        self.cards = [
            {"id": 0, "name": "黑桃J"},
            {"id": 1, "name": "红桃J"},
            {"id": 2, "name": "黑桃Q"},
            {"id": 3, "name": "红桃Q"},
            {"id": 4, "name": "黑桃K"},
            {"id": 5, "name": "红桃K"},
        ]
        random.seed(time.time())

    id_to_str_map = {0: "SJ", 1: "HJ", 2: "SQ", 3: "HQ", 4: "SK", 5: "HK"}

    def Licensing(self):
        return self.cards.pop(randint(0, len(self.cards) - 1))

    def LicensingCards(self):
        self.CommunityCard, self.YourCard, self.AgentCard = (
            self.Licensing(),
            self.Licensing(),
            self.Licensing(),
        )
        self.CommunityCardId = self.CommunityCard["id"]
        self.CommunityCardName = self.CommunityCard["name"]
        self.YourCardId = self.YourCard["id"]
        self.YourCardName = self.YourCard["name"]
        self.AgentCardId = self.AgentCard["id"]
        self.AgentCardName = self.AgentCard["name"]

    def PrintLicensingCards(self):
        print("===============  Community Card ===============")
        print_card(None)
        print("=============== Your&Agent Cards ===============")
        print_card([self.id_to_str_map[self.YourCardId], None])

    def PrintCommunityCard(self):
        print("===============  Community Card ===============")
        print_card(self.id_to_str_map[self.CommunityCardId])
        print("=============== Your&Agent Cards ===============")
        print_card([self.id_to_str_map[self.YourCardId], None])

    def PrintCards(self):
        print("===============       Cards     ===============")
        print_card(self.id_to_str_map[self.CommunityCardId])
        print_card(
            [self.id_to_str_map[self.YourCardId], self.id_to_str_map[self.AgentCardId]]
        )

        # 接下来定义打印方法

    def print_cards(self):
        print("Community Card:")
        print("ID:", self.CommunityCardId)
        print("Name:", self.CommunityCardName)
        print("\nYour Card:")
        print("ID:", self.YourCardId)
        print("Name:", self.YourCardName)
        print("\nAgent Card:")
        print("ID:", self.AgentCardId)
        print("Name:", self.AgentCardName)

    def print_cards_to_agent(self):
        return (
            "公共牌: "
            + self.CommunityCardName
            + " 你的牌是"
            + self.AgentCardName
            + ".对手的牌是"
            + self.YourCardName
        )

    # 第一回合，公共牌未知，自己牌已知，对手牌未知
    def GetUserRound1Info(self):
        return f"第一回合，公共牌未知，你的牌是{self.YourCardName}，对手的牌未知"

    # 第二回合，公共牌已知，自己牌已知，对手牌未知
    def GetUserRound2Info(self):
        return f"第二回合，公共牌是{self.CommunityCardName}，你的牌是{self.YourCardName}，对手的牌未知"

    # 开牌，公共牌已知，自己牌已知，对手牌已知
    def GetUserFinalInfo(self):
        return f"开牌，公共牌是{self.CommunityCardName}，你的牌是{self.YourCardName}，对手的牌是{self.AgentCardName}"


