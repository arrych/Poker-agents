import agentscope
from agentscope.agents import DialogAgent, UserAgent
import prompt
from agentscope.message import Msg

# read model configs
agentscope.init(
    model_configs=[
        {
            "model_type": "tongyi_chat",
            "config_name": "qwenMax",
            "model_name": "qwen-max",
            "api_key": "sk-d413e323467b438cb83c9222db25df62",
            "generate_args": {
                "temperature": 0.5,
            },
            "messages_key": "input",
        }
    ]
)

y = Msg(name="agentA2", content="最开始不了解对手,无法判断对方是保守还是激进")


def getAgent(prompt_str: str):
    A1 = DialogAgent(
        name="agentA1",
        model_config_name="qwenMax",
        sys_prompt=prompt.agentA1+f".你的性格是:{prompt_str},要好好根据你的性格风格来玩游戏")

    A2 = DialogAgent(
        name="agentA2",
        model_config_name="qwenMax",
        sys_prompt=prompt.agentA2)

    A3 = DialogAgent(
        name="agentA3",
        model_config_name="qwenMax",
        sys_prompt=prompt.agentA3+f".你的性格是:{prompt_str},要好好根据你的性格风格来玩游戏")
    A4 = DialogAgent(
        name="agentA4",
        model_config_name="qwenMax",
        sys_prompt=prompt.agentA4+f".你的性格是:{prompt_str},要好好根据你的性格风格来玩游戏")
    return A1,A2,A3,A4
