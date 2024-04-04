from agentscope.prompt import PromptEngine, PromptType
from agent import CustomizedAgent

act_tuple = tuple['跟注', '加注', '弃牌']


class Npc(CustomizedAgent):

    def __init__(self, name, avatar, sys_prompt, model_config_name):
        super().__init__(name, sys_prompt=sys_prompt, model_config_name=model_config_name)
        self.engine = PromptEngine(self.model, prompt_type=PromptType.LIST)
        self.name = name
        self.avatar = avatar
        self.principal = 100
        self.act = None
        self.bet = 0
        self.shadows = []
        for _ in range(3):
            self.shadows.append(CustomizedAgent(name, sys_prompt, model_config_name))
