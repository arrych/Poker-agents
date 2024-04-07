import re
import time
from typing import Any, Sequence

from agentscope import msghub

import agentscope

from agentscope.message import Msg

from agentscope.prompt import PromptEngine, PromptType

from agentscope.agents import AgentBase, UserAgent


def filter_agents(string: str, agents: Sequence) -> Sequence:
    """
    该函数会筛选输入字符串中以'@'为前缀的给定名称的出现，并返回找到的名称列表。
    """
    if len(agents) == 0:
        return []
    # 创建一个匹配@后跟任何候选名字的模式
    pattern = (
            r"@(" + "|".join(re.escape(agent.name) for agent in agents) + r")\b"
    )
    # 在字符串中找到所有模式的出现
    matches = re.findall(pattern, string)

    # 为了快速查找，创建一个将代理名映射到代理对象的字典
    agent_dict = {agent.name: agent for agent in agents}
    # 返回匹配的代理对象列表，保持顺序
    ordered_agents = [
        agent_dict[name] for name in matches if name in agent_dict
    ]
    return ordered_agents


def select_next_one(agents: Sequence, rnd: int) -> AgentBase:
    return agents[rnd % len(agents)]


class CustomizedAgent(AgentBase):

    def __init__(self, name, sys_prompt, model_config_name, num_actions):
        super().__init__(name, sys_prompt=sys_prompt, model_config_name=model_config_name, use_memory=True)
        self.engine = PromptEngine(self.model, prompt_type=PromptType.LIST)
        self.use_raw = True
        self.num_actions = num_actions

    def reply(self, x: dict = None) -> dict:
        # 将问题x（或者理解为用户提示）加入记忆
        if x is not None:
            if self.memory:
                self.memory.add(x)

        # 将记忆和系统提示合并
        prompt = self.engine.join(
            self.sys_prompt,
            self.memory and self.memory.get_memory(),
        )

        # 调用模型接口（千问API）
        response = self.model(prompt).text
        # ,parse_func = my_parse_func)

        # 包装成Msg
        msg = Msg(self.name, response)

        # logger.chat(content)日志打印，会被内置的Gradio接口捕捉，该接口不会广播消息
        # 注意该操作是异步
        self.speak(msg)

        # 将回复加入记忆
        if self.memory:
            msg_memory = Msg(
                name=self.name,
                content=str(msg.content),
                role=self.name,
            )
            self.memory.add(msg_memory)

        return msg

    @staticmethod
    def step(state):
        ''' Predict the action given the curent state in gerenerating training data.

        Args:
            state (dict): An dictionary that represents the current state

        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
        '''
        # return np.random.choice(list(state['legal_actions'].keys()))
        return 'check'

    def __call__(self, *args: Any, **kwargs: Any) -> dict:
        # 调用接口等待回复
        res = self.reply(*args, **kwargs)
        # 观察者模式
        # 当进入with MsgHub语法块时，self._audience会被自动填充
        # 当广播时，会调用每个agent的observe()方法
        if self._audience is not None:
            self._broadcast_to_audience(res)

        return res

    # 删除上次对话
    def forget_last_chat_round(self):
        memory = self.memory.get_memory()
        if memory is None or len(memory) < 1:
            return
        last_chat_point = self.find_latest_chat_round_idx(1)
        self.memory.delete(list(range(last_chat_point, len(memory))))

    # 删除所有记忆
    def flush_memory(self):
        if self.memory is not None:
            self.memory.clear()

    # 保留最近交流的记忆，记忆中既包括问题也包含回答，通过身份来判断
    def reserve_latest_chat_rounds(self, count):
        if self.memory is None:
            return
        last_chat_point = self.find_latest_chat_round_idx(count)
        self.memory.delete(list(range(last_chat_point)))

    def find_latest_chat_round_idx(self, count) -> int:
        if self.memory is None:
            return -1
        memory = self.memory.get_memory()
        last_chat_point = 0
        for i in range(len(memory) - 1, -1, -1):
            chat_log = memory[i]
            if count <= 0:
                last_chat_point = i
                break
            if chat_log["name"] == self.name:
                count -= 1
        return last_chat_point


if __name__ == "__main__":
    agentscope.init(
        model_configs="./config/model_configs.json"
    )
    ashely = CustomizedAgent("Ashely", "帮助回答一些数学计算问题", "qwen_config")
    ashely()
    ashely(Msg(name="Host", content="1+1等于几？"))
    ashely(Msg(name="Host", content="2+2等于几？"))
    ashely(Msg(name="Host", content="3+3等于几？"))
    ashely(Msg(name="Host", content="4+4等于几？"))
    ashely(Msg(name="Host", content="我之前一共问了你几个问题？复述出来！"))
    time.sleep(1)
    print("遗忘最近一轮谈话")
    ashely.forget_last_chat_round()
    time.sleep(1)
    print("保留最近两轮谈话")
    ashely.reserve_latest_chat_rounds(2)
    ashely(Msg(name="Host", content="我之前一共问了你几个问题？复述出来！"))

    bob = CustomizedAgent("Bob", "你是数学小行家！", "qwen_config")
    cathy = CustomizedAgent("Cathy", "你是数学小行家！", "qwen_config")

    # 循环发言
    npc = [ashely, bob, cathy]
    # 维护一个发言列表
    speak_list = []
    # 第几轮谈话
    rnd = 0
    # 玩家
    user = UserAgent()
    with msghub(participants=npc, announcement=Msg(name="Host", content="你们可以真自由发言了！")):
        while True:
            try:
                x = user(timeout=5000)
                if x.content == "exit":
                    break
                speak_list = filter_agents(x.get("content", ""), npc)
                if len(speak_list) > 0:
                    next_agent = speak_list[0]
                else:
                    next_agent = select_next_one(npc, rnd)
                x = next_agent(x.content)
                rnd += 1
            except TimeoutError:
                x = {"content": ""}
