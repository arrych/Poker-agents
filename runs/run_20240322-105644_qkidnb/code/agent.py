import agentscope
from agentscope.agents import DialogAgent, UserAgent
import prompt

# read model configs
agentscope.init(
    model_configs=[
        {
            "model_type": "tongyi_chat",
            "config_name": "qwenMax",
            "model_name": "qwen-max",
            "api_key": "sk-0c0a723ca29442088c388d7c670a88a8",
            "generate_args": {
                "temperature": 0.5,
            },
            "messages_key": "input",
        }
    ]
)

A1 = DialogAgent(
    name="agentA1",
    model_config_name="qwenMax",
    sys_prompt=prompt.agentA1)

A2 = DialogAgent(
    name="agentA2",
    model_config_name="qwenMax",
    sys_prompt=prompt.agentA2)


y = Msg(name="agentA2", content="最开始不了解对手,无法判断对方是保守还是激进")
