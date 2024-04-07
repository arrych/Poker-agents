npc_init_sys_prompt = "你是{}, 这是一个类似德州扑克的纸牌游戏"

shadow_assistants = [
    {'name': 'Assistant1', 'sys_prompt': '你需要和另一位助手Assistant2讨论后共同作出本次行动的选择。'
                                         '但你总是做出非常激进大胆的决策，请说服另一位助手达成一致并做出最终选择。'},
    # aggressive prompt
    {'name': 'Assistant2', 'sys_prompt': '你需要和另一位助手Assistant1讨论后共同作出本次行动的选择。'
                                         '你倾向于消极保守的决策行动，请说服另一位助手达成一致并做出最终选择。'},
]

negotiate_announcement = ('现在是{}阶段，请Assistant1和Assistant2讨论本次选择什么行动。请按照如下的格式进行回答：{{'
                          '{{\n'
                          '    "thought": "你的想法",\n'
                          '    "action": "只允许填数字，1-raise,2-call,3-fold",\n'
                          '    "agreement": "是否达成一致，True or False"\n'
                          '}}')
