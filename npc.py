import random

import prompt2
import round
from agentscope.message import Msg
from agentscope.prompt import PromptEngine, PromptType
from agent2 import CustomizedAgent

act_tuple = tuple['跟注', '加注', '弃牌']
MAX_NEGOTIATE_ROUNDS = 5


class Npc(CustomizedAgent):

    def __init__(self, name, avatar, sys_prompt, model_config_name, num_actions, principal=100):
        super().__init__(name, sys_prompt=sys_prompt, model_config_name=model_config_name, num_actions=num_actions)
        self.engine = PromptEngine(self.model, prompt_type=PromptType.LIST)
        self.num_actions = num_actions
        self.name = name
        self.avatar = avatar
        self.principal = principal
        self.act = None
        self.bet = 0
        self.shadows = []
        for prompt in prompt2.shadow_assistants:
            self.shadows.append(CustomizedAgent(prompt['name'], prompt['sys_prompt'], model_config_name, num_actions))

    def step(self, state):
        """ Predict the action given the current state in generating training data.

        Args:
            state (dict): An dictionary that represents the current state

        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
        """
        # return np.random.choice(list(state['legal_actions'].keys()))
        self.shadows_negotiate(state)
        return 'check'

    def shadows_negotiate(self, state):
        print(state)
        x = Msg('player', content=prompt2.negotiate_announcement[round.round_steps[0]])
        # forlooppipeline(self, random.choice([MAX_NEGOTIATE_ROUNDS,MAX_NEGOTIATE_ROUNDS+1]),)

