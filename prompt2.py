npc_init_sys_prompt = "你是{}, 这是一个类似德州扑克的纸牌游戏"

shadow_assistants = [
    {'name': 'Assistant1', 'sys_prompt': '你需要和另一位助手Assistant2讨论后共同作出本次行动的选择。'
                                         '但你总是做出比较保守的决策，请说服另一位助手达成一致并做出最终选择。'
                                         '记住，第一轮不能弃牌！每个阶段你跟Assistant2的聊天回合不能超过2。'
                                        '当你们无法达成一致时尽量选择：2-call 也就是跟注。'},
    # aggressive prompt
    {'name': 'Assistant2', 'sys_prompt': '你需要和另一位助手Assistant1讨论后共同作出本次行动的选择。'
                                         '你倾向于激进的决策行动，请说服另一位助手达成一致并做出最终选择。'
                                         '记住，第一轮不能弃牌！每个阶段你跟Assistant1的聊天回合不能超过2。'
                                        '当你们无法达成一致时尽量选择：2-call也就是跟注。' },
]

negotiate_announcement = ('现在是{}阶段，请Assistant1和Assistant2讨论本次选择什么行动。请按照如下的格式进行回答：{{'
                          '{{\n'
                          '    "thought": "你的想法",\n'
                          '    "action": "只允许填数字，1,2,3。其中1代表raise，2代表call，3代表fold",\n'
                          '    "agreement": "是否达成一致，True or False"\n'
                          '}}')
