
class Points:
    def __init__(self, points: int):
        self.User = points
        self.Agent = points
        self.UserOri = points
        self.AgentOri = points
        self.Pool = 0
        self.base = 1

    def IsValid(self) -> bool:
        return self.User > 0 and self.Agent > 0

    def game_over(self):
        result = "你战胜了Agent" if self.User > 0 else "你被Agent击败了"
        print("游戏结束: " + result)

    # 加注
    def UserRaise(self):
        self.User -= 2 * self.base
        self.Pool += 2 * self.base
        self.base *= 2

    # 跟注
    def UserCall(self):
        self.User -= self.base
        self.Pool += self.base

    # 加注
    def AgentRaise(self):
        self.Agent -= 2 * self.base
        self.Pool += 2 * self.base
        self.base *= 2

    # 跟注
    def AgentCall(self):
        self.Agent -= self.base
        self.Pool += self.base

    def UserWin(self):
        self.User += self.Pool
        self.AgentOri = self.Agent
        self.UserOri = self.User
        self.Pool = 0

    def AgentWin(self):
        self.Agent += self.Pool
        self.AgentOri = self.Agent
        self.UserOri = self.User
        self.Pool = 0

    def InitBet(self):
        self.Agent -= 1
        self.User -= 1
        self.Pool += 2
        self.base = 1

    def Draw(self):
        self.Pool = 0
        self.Agent = self.AgentOri
        self.User = self.UserOri

    def settlement(self, res: str):
        if res == "Win":
            self.UserWin()
        elif res == "Lose":
            self.AgentWin()
        else:
            self.Draw()

    # 0:跟注 1:加注 2:弃牌
    def UserAction(self, action: str):
        if 1 == action:
            self.UserRaise()
        elif 0 == action:
            self.UserCall()
        else:
            self.AgentWin()

    def AgentAction(self, action: str):
        if 1 == action:
            self.AgentRaise()
        elif 0 == action:
            self.AgentCall()
        else:
            self.UserWin()

    def __str__(self) -> str:
        return f"你当前积分: {self.User}\r\nAgent积分: {self.Agent}\r\nPool积分: {self.Pool}"

    def record(self) -> str:
        return f"你当前积分: {self.Agent}\r\n对手积分: {self.User}\r\nPool积分: {self.Pool}"

    def Info(self) -> str:
        return f"你当前积分: {self.User},对手积分: {self.Agent},台面积分: {self.Pool}"

