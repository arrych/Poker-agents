import json
import re
from json import JSONDecodeError
import streamlit as st
from typing import Sequence

import prompt2
import round
from agent2_rule import LimitholdemRuleAgentV1
from agentscope import msghub
from agentscope.agents import AgentBase
from agentscope.message import Msg
from agentscope.prompt import PromptEngine, PromptType
from agent2 import CustomizedAgent
from rlcard.agents import LimitholdemHumanAgent as HumanAgent

act_tuple = ('raise', 'call', 'fold', 'check')
MAX_NEGOTIATE_ROUNDS = 2

def set_audiences(participants: Sequence[AgentBase]):
    """Reset the audience for agent in `self.participant`"""
    for agent in participants:
        agent.reset_audience(participants)


def find_first_json(text):
    # 匹配JSON对象或数组
    pattern = r'({.*?})|(\[.*?\])'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group()
    else:
        return text


class Npc(CustomizedAgent):

    def __init__(self, name, avatar, num_actions, sys_prompt="", model_config_name='qwenMax', principal=100):
        super().__init__(name, sys_prompt=sys_prompt, model_config_name=model_config_name, num_actions=num_actions)
        self.engine = PromptEngine(self.model, prompt_type=PromptType.LIST)
        self.num_actions = num_actions
        self.name = name
        self.avatar = avatar
        self.principal = principal
        self.act = None
        self.bet = 0
        self.shadows = []
        self.randomAgent = LimitholdemRuleAgentV1()
        for prompt in prompt2.shadow_assistants:
            ## todo 这里的prompt['sys_prompt']是对自己两个性格的agent的初始提示，用于介绍游戏规则等等
            self.shadows.append(CustomizedAgent(prompt['name'], prompt['sys_prompt'], model_config_name, num_actions))

    def step(self, state):
        """ Predict the action given the current state in generating training data.

        Args:
            state (dict): An dictionary that represents the current state

        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
        """
        # return np.random.choice(list(state['legal_actions'].keys()))
        res = self.shadows_negotiate(state)
        print(f'res_==={res}')
        ## todo 这里是对别的NPC玩家进行回答的地方，需要修改格式
        self._broadcast_to_audience(Msg(name=self.name, content=f'我选择{res}'))  ## 将本次动作广播给所有听众
        return res

    def _broadcast_to_audience(self, x: dict) -> None:
        """Broadcast the input to all audiences."""
        super()._broadcast_to_audience(x)
        """Broadcast the input to all shadows."""
        for agent in self.shadows:
            agent.observe(x)

    def shadows_negotiate(self, state):
        game_info = st.session_state.game_info
        state_raw_obs = state['raw_obs']
        legal_actions = state['raw_legal_actions']
        print(f'state_legal_actions:{legal_actions}')
        print(f'state_raw_obs:{state_raw_obs}')
        hand = state_raw_obs['hand']
        public_cards = state_raw_obs['public_cards']
        round_info = round.pre_flop_round  ##对局阶段
        if st.session_state['round_info'] is not None:
            round_info = st.session_state.round_info
        ## todo announcement是在两个agent对话前，对两个性格的agent进行的提示
        with msghub(participants=self.shadows, announcement=prompt2.negotiate_announcement.format(round_info,legal_actions)):
            for i in range(MAX_NEGOTIATE_ROUNDS):
                for agent in self.shadows:
                    ## todo 这里可以自定义消息再进行一次提示
                    msg = agent(Msg(name=self.name, content=f'现在是第()阶段，手牌是{hand}，公共牌是{public_cards},请按照如下的格式进行回答：'
                          '{{\n'
                          '    "thought": "你的想法",\n'
                          '    "action": "只能从当前合法的动作中选择一个,目前的合法动作有{legal_actions},一定记住只能从前面的合法动作里选择一个动作，一定记住只能从前面的合法动作里选择一个动作，一定记住只能从前面的合法动作里选择一个动作,\n'
                          '    "agreement": "是否达成一致，True or False"\n'
                          '}}'))
                    ## todo 接上，像这样msg = agent(Msg(name=self.name, content='自定义消息'))
                    #msg = agent()
                    try:
                        ## todo 注意对回答格式的约束
                        res = json.loads(find_first_json(msg.content))
                        #res = json.loads(msg.content)
                        if res['agreement']:
                            action_= res['action']
                            # action_ = act_tuple[int(act_) - 1]
                            if action_ in legal_actions:
                                return action_
                            else:
                                if action_ == 'raise':
                                    if 'call' in legal_actions:
                                        return 'call'
                                    elif 'check' in legal_actions:
                                        return 'check'
                                    else:
                                        return 'fold'
                                if action_ == 'check':
                                    return 'fold'
                                if action_ == 'call':
                                    if 'check' in legal_actions:
                                        return 'check'
                                    elif 'raise' in legal_actions:
                                        return 'raise'
                                    else:
                                        return 'fold'
                                else:
                                    return action_
                    except JSONDecodeError:
                        for audience in self.shadows:
                            audience.forget_last_answer()
        act_f = self.randomAgent.step(state)
        print(f'act_f==={act_f}')
        return act_f


class Player(Npc):
    def __init__(self, name, avatar, num_actions):
        super().__init__(name, avatar, num_actions)
        self.humanAgent = HumanAgent(num_actions)

    def step(self, step):
        self._broadcast_to_audience(Msg(name=self.name, content=f'我选择{step}'))

    def step2(self, name, step):
        self._broadcast_to_audience(Msg(name=name, content=f'我选择{step}'))
