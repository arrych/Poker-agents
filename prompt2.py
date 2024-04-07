import game2
import round


npc_sys_prompt = {
    game2.player_list[1]: f'你是{game2.player_list[1]['name']}, 这是一个类似德州扑克的纸牌游戏',
    game2.player_list[2]: f'你是{game2.player_list[2]['name']}, 这是一个类似德州扑克的纸牌游戏',
    game2.player_list[3]: f'你是{game2.player_list[3]['name']}, 这是一个类似德州扑克的纸牌游戏',
    game2.player_list[4]: f'你是{game2.player_list[4]['name']}, 这是一个类似德州扑克的纸牌游戏',
    game2.player_list[5]: f'你是{game2.player_list[5]['name']}, 这是一个类似德州扑克的纸牌游戏',
}

shadow_assistants = [
    {'name': 'Assistant1', 'sys_prompt': '你需要和另一位助手Assistant2讨论后共同作出本次行动的选择。'
                                         '但你总是做出非常激进大胆的决策，请说服另一位助手达成一致并做出最终选择。'},
    # aggressive prompt
    {'name': 'Assistant2', 'sys_prompt': '你需要和另一位助手Assistant1讨论后共同作出本次行动的选择。'
                                         '你倾向于消极保守的决策行动，请说服另一位助手达成一致并做出最终选择。'},
]

negotiate_announcement = {
    round.round_steps[0]: f'现在是{round.round_steps[0]}阶段，请Assistant1和Assistant2讨论本次选择什么行动。',
    round.round_steps[1]: f'现在是{round.round_steps[1]}阶段，请Assistant1和Assistant2讨论本次选择什么行动。',
    round.round_steps[2]: f'现在是{round.round_steps[2]}阶段，请Assistant1和Assistant2讨论本次选择什么行动。',
    round.round_steps[3]: f'现在是{round.round_steps[3]}阶段，请Assistant1和Assistant2讨论本次选择什么行动。',
    round.round_steps[3]: f'现在是{round.round_steps[4]}阶段，请Assistant1和Assistant2讨论本次选择什么行动。',
}
