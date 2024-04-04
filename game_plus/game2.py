
import streamlit as st

import agentscope
from agentscope import msghub
from npc import Npc
from utils import CardDeck, Card
import round

"""
游戏规则：
六名玩家（Npc1~5和一个玩家）
每个玩家只有跟注、加注和弃牌3种行动
每个阶段结束的条件是每个人都下注了同样的金额

1、准备阶段(pre-flop)
发5张公共牌，每个人发两张手牌

2、翻牌阶段（flop）
NPC1~5，玩家依次发言，
这一阶段不允许弃牌，
翻前三张牌。

3、转牌阶段
NPC1~5，玩家依次发言，
翻第四张牌

4、合牌阶段
NPC1~5，玩家依次发言，
翻第五张牌

5、展示手牌
决定赢家，清算积分
"""

# 假设的NPC数据
player_list = st.session_state.player_list = [
    {'name': 'NPC_1', 'avatar': 'assets/avatars/npc1.png'},
    {'name': 'NPC_2', 'avatar': 'assets/avatars/npc1.png'},
    {'name': 'NPC_3', 'avatar': 'assets/avatars/npc1.png'},
    {'name': 'NPC_4', 'avatar': 'assets/avatars/npc1.png'},
    {'name': 'NPC_5', 'avatar': 'assets/avatars/npc1.png'},
    {'name': 'YOU', 'avatar': 'assets/avatars/player.png'}
]

# 手牌
hand_cards = st.session_state.hand_cards = {}
# 公共牌
community_cards = st.session_state.community_cards = []
# 牌库
card_deck = st.session_state.card_deck = CardDeck()
# 奖池
jackpot = st.session_state.jackpot = 0
# 说话人
who_speak = st.session_state.who_speak = player_list[5]

# players = agentscope.init(
#     model_configs="./config/model_configs.json"
# )


def main():
    # st.session_state.players = {player['name']: Npc(player['name']
    #                                 , player['avatar']
    #                                 , '你好，让我们来玩一个德州扑克的游戏'
    #                                 , "qwen_config") for player in player_list[:5]}
    #
    # with msghub(players) as hub:
    st.session_state.round = round.show_hand_round  # 控制阶段

    # 第一块：NPC展示区
    with st.sidebar:
        for i, npc in enumerate(player_list[:5]):  # 展示前五个NPC
            row = st.container(border=True)
            cols = row.columns(4)
            cols[0].image(npc['avatar'], caption=npc['name'])  # NPC头像和姓名
            round.show_hand_cards(cols[1:3], npc)
            round.npc_act(npc, cols[3])

    canvas = st.columns(1)[0]
    # 第二行：公共信息区
    round.show_game_round_step(canvas)
    canvas.subheader(
        f'场上奖池累积至{st.session_state.jackpot}积分，现在轮到{st.session_state.who_speak['name']}行动……')  # 使用分隔线创建视觉上的行分隔
    row = canvas.container(border=True)
    row.caption("公共牌")
    round.show_community_cards(row)
    canvas.divider()

    # 第三行：用户操作界面
    player_canvas = canvas.container(border=True)
    player_cols = player_canvas.columns(6)
    player_cols[0].image(player_list[5]['avatar'], caption=player_list[5]['name'])
    round.show_hand_cards(player_cols[1:3], player_list[5])
    operate_menu = player_cols[3]
    operate_menu.radio("你的行动：", options=['跟注', '加注', '弃牌'])
    round.show_button(operate_menu)
    ability_menu = player_cols[4]
    ability_menu.write('你的能力')
    ability_menu.checkbox(label='读心术', key='read_mind')
    ability_menu.checkbox(label='透视眼', key='see_through')
    bet_statistic = player_cols[5]
    round.player_act(bet_statistic)


if __name__ == '__main__':
    main()
