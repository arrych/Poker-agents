
import streamlit as st

import rlcard
from rlcard.agents import RandomAgent
from rlcard.utils import set_seed
from rlcard.agents import LimitholdemHumanAgent as HumanAgent
from rlcard.agents import RandomAgent
from rlcard.games.limitholdem.game import LimitHoldemGame
from rlcard.utils.utils import print_card
import agentscope
from agentscope import msghub
from npc import Npc
from points import Points
from poker import Porker
from utils2 import CardDeck, Card
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
    {'name': 'YOU', 'avatar': 'assets/avatars/player.png'},
    {'name': 'NPC_1', 'avatar': 'assets/avatars/npc1.png'},
    {'name': 'NPC_2', 'avatar': 'assets/avatars/npc1.png'},
    {'name': 'NPC_3', 'avatar': 'assets/avatars/npc1.png'},
    {'name': 'NPC_4', 'avatar': 'assets/avatars/npc1.png'},
    {'name': 'NPC_5', 'avatar': 'assets/avatars/npc1.png'}
]

# 手牌
hand_cards = st.session_state.hand_cards = {}
# 公共牌
community_cards = st.session_state.community_cards = []
user_cards = st.session_state.community_cards = []
# 牌库
card_deck = st.session_state.card_deck = CardDeck()
# 奖池
jackpot = st.session_state.jackpot = 0
# 说话人
who_speak = st.session_state.who_speak = player_list[5]

# players = agentscope.init(
#     model_configs="./config/model_configs.json"
# )

import streamlit as st


def game2():

    st.session_state.round = round.show_hand_round  # 控制阶段
    # 初始化session_state

    # 初始化游戏状态，包括玩家信息、奖池等
    # game_phase: pre-flop -> flop -> turn -> river -> showdown
    if 'game_phase' not in st.session_state:
        init()

    game_info = st.session_state.game_info

    round_info = st.session_state.round_info
    var = game_info.game.public_cards
    st.session_state.community_cards = convert_cards_list(game_info.game.public_cards)
    state_info = st.session_state.state
    player_id = st.session_state.player_id
    player = game_info.game.players[0]

    trajectories = [[] for _ in range(game_info.num_players)]

    trajectories[player_id].append(state_info)
    var1 = st.session_state['continue']
    st.write("round_counter: "+str(game_info.game.round_counter))
    # st.write(state_info)
    st.write("player_id:" + str(player_id))
    st.session_state.action = 'check'
    if not game_info.is_over() and not st.session_state['continue']:
        if player_id == 0:
            # action = user_step(state_info)
            st.session_state.user_cards = convert_cards_list(player.hand)
            st.session_state['continue'] = True
        else:
            # 机器人行动
            st.session_state.action = game_info.agents[player_id].step(state_info)
            # action = 'fold'
            step(game_info, state_info, player_id, st.session_state.action, trajectories)

    var2 = st.session_state.action
    var3 = player_id
    show(game_info, state_info, st.session_state.action, player_id, trajectories)

    # if player_id == 0 and not st.session_state['continue']:
    #     step(game_info, state_info, player_id, st.session_state.action, trajectories)

    if game_info.is_over():
        if st.button("新的一局!"):
            new_game()
        st.stop()

    if st.sidebar.button("重新开始!"):
        init()

    st.rerun()


    # # 准备阶段
    # if st.session_state.game_phase == "pre-flop":
    #     # 发5张公共牌，每个人发两张手牌
    #     deal_community_cards(5)
    #     deal_hand_cards_to_each_player(2)
    #
    #     # 展示NPC和玩家的手牌 - 可能需要调整展示方式，确保手牌暂时不被对方看见
    #     show_hand_cards()
    #
    #     # 设置游戏阶段为"flop"
    #     st.session_state.game_phase = "flop"
    #     # 提示用户进行下一步操作
    #     st.button("进入翻牌阶段", on_click=advance_game_phase)
    #
    # # 翻牌阶段
    # elif st.session_state.game_phase == "flop":
    #     # 翻前三张公共牌
    #     show_community_cards(3)
    #
    #     # NPC1~5和玩家依次发言，这一阶段不允许弃牌
    #     player_actions(allow_fold=False)
    #
    #     # 设置游戏阶段为"turn"
    #     st.session_state.game_phase = "turn"
    #     # 提示用户进行下一步操作
    #     st.button("进入转牌阶段", on_click=advance_game_phase)
    #
    # # 转牌阶段
    # elif st.session_state.game_phase == "turn":
    #     # 翻第四张公共牌
    #     show_community_card(4)
    #
    #     # NPC1~5和玩家依次发言
    #     player_actions()
    #
    #     # 设置游戏阶段为"river"
    #     st.session_state.game_phase = "river"
    #     # 提示用户进行下一步操作
    #     st.button("进入合牌阶段", on_click=advance_game_phase)
    #
    # # 合牌阶段
    # elif st.session_state.game_phase == "river":
    #     # 翻第五张公共牌
    #     show_community_card(5)
    #
    #     # NPC1~5和玩家依次发言
    #     player_actions()
    #
    #     # 设置游戏阶段为"showdown"
    #     st.session_state.game_phase = "showdown"
    #     # 提示用户进行下一步操作
    #     st.button("进入展示手牌阶段", on_click=advance_game_phase)
    #
    # # 展示手牌阶段
    # elif st.session_state.game_phase == "showdown":
    #     # 展示所有玩家的手牌，决定赢家，清算积分
    #     show_all_hand_cards()
    #     decide_winner()
    #     clear_points()
    #
    #     # 游戏结束，或准备下一轮
    #     st.session_state.game_phase = "pre-flop"  # 重新设置为准备阶段，或根据需求调整
    #     # 提示用户重新开始或结束游戏
    #     st.button("开始新一轮游戏", on_click=reset_game)

    # 第一块：NPC展示区


def step(game_info, state_info, player_id, action, trajectories):
    # Environment steps
    next_state, next_player_id = game_info.step(action, game_info.agents[player_id].use_raw)
    # Save action
    trajectories[player_id].append(action)

    # Set the state and player
    st.session_state.state = next_state
    st.session_state.player_id = next_player_id

    # Save state.
    if not game_info.game.is_over():
        trajectories[player_id].append(state_info)


def show(game_info, state_info, rd, player_id, trajectories):
    with st.sidebar:
        for i, npc in enumerate(player_list[1:]):  # 展示后五个NPC
            row = st.container(border=True)
            cols = row.columns(4)
            cols[0].image(npc['avatar'], caption=npc['name'])  # NPC头像和姓名
            round.show_hand_cards(cols[1:3], npc)
            if i == player_id:
                round.npc_act(npc, cols[3], rd)

    canvas = st.columns(1)[0]
    # 第二行：公共信息区
    round.show_game_round_step(canvas)
    canvas.subheader(
        f"场上奖池累积至{st.session_state.jackpot}积分，现在轮到{st.session_state.who_speak['name']}行动……")  # 使用分隔线创建视觉上的行分隔
    row = canvas.container(border=True)
    row.caption("公共牌")
    round.show_community_cards(row)
    canvas.divider()

    # 第三行：用户操作界面
    player_canvas = canvas.container(border=True)
    player_cols = player_canvas.columns(6)
    player_cols[0].image(player_list[0]['avatar'], caption=player_list[0]['name'])
    if "user_cards" not in st.session_state:
        round.show_hand_cards(player_cols[1:3], player_list[0])
    else:
        player_cols[1].image(st.session_state.user_cards[0].image_path)  # NPC手牌图片
        player_cols[2].image(st.session_state.user_cards[1].image_path)  # NPC手牌图片

    operate_menu = player_cols[3]
    # operate_menu.radio("你的行动：", options=['跟注', '加注', '弃牌'])
    # round.show_button(operate_menu, player_id)

    ability_menu = player_cols[4]
    ability_menu.write('你的能力')
    ability_menu.toggle(label='读心术', key='read_mind')
    ability_menu.toggle(label='透视眼', key='see_through')
    if st.session_state['continue']:
        legal_action = state_info['raw_legal_actions']
        with st.spinner('Please wait...'):
            # 这里执行你的操作
            disabled = player_id != 0
            # 为每个操作创建一个按钮
            for action in legal_action:
                # 获取中文标签
                label = translate_dict[action]

                # 创建按钮
                if operate_menu.button(key=action, label=label, disabled=disabled):
                    st.session_state['continue'] = False
                    st.session_state.action = action
                    step(game_info, state_info, player_id, st.session_state.action, trajectories)
                    st.rerun()
            # st.session_state['continue'] = False
        st.stop()

    bet_statistic = player_cols[5]
    round.player_act(bet_statistic)


def init():
    # 初始化游戏状态逻辑
    # 需要定义玩家列表、奖池大小、游戏阶段等
    game_info = rlcard.make('limit-holdem', config={'game_num_players': 6})
    human_agent = HumanAgent(game_info.num_actions)
    agent_1 = RandomAgent(num_actions=game_info.num_actions)
    agent_2 = RandomAgent(num_actions=game_info.num_actions)
    agent_3 = RandomAgent(num_actions=game_info.num_actions)
    agent_4 = RandomAgent(num_actions=game_info.num_actions)
    agent_5 = RandomAgent(num_actions=game_info.num_actions)
    game_info.set_agents([
        human_agent,
        agent_1, agent_2, agent_3, agent_4, agent_5
    ])
    st.session_state.game_info = game_info
    st.session_state.round_info = game_info.game.round
    st.session_state.game_phase = "pre-flop"
    st.session_state['continue'] = False
    st.session_state.state, st.session_state.player_id = st.session_state.game_info.reset()
    st.session_state.jackpot = 0
    # st.session_state.recording = None
    # st.session_state['role_selected'] = False
    # st.session_state['selected_character'] = None
    st.session_state.perspective_eye = False
    st.session_state.mind_reading = False
    pass


def new_game():
    st.session_state.state, st.session_state.player_id = st.session_state.game_info.reset()
    st.session_state['continue'] = False
    st.session_state.round_info = st.session_state.game_info.game.round
    # p = Porker()
    # st.session_state.porker = p
    # p.LicensingCards()  # 发牌
    # st.session_state.round = 1
    # st.session_state.game += 1
    # st.session_state.agent_card_name = p.AgentCardName
    # st.session_state.agent_card_id = p.AgentCardId
    # st.session_state.your_card_name = p.YourCardName
    # st.session_state.your_card_id = p.YourCardId
    # st.session_state.community_card_name = p.CommunityCardName
    # st.session_state.community_card_id = p.CommunityCardId
    # init -> start -> next -> end
    # st.session_state.game_state = "start"
    # st.session_state.points.InitBet()  # 每局开始投入1个积分打底
    # # 聊天记录
    # st.session_state.chat_history = []
    # st.session_state.recording = ''

def user_step(state_info):
    return state_info['raw_legal_actions'][0]


def convert_card_notation(card_str):
    # 定义扑克牌花色和对应的标准表示
    suits = {
        'C': 'clubs',
        'H': 'hearts',
        'D': 'diamonds',
        'S': 'spades'
    }

    # 假设输入的card_str是单个扑克牌表示，包含两个字符
    suit_char = card_str.suit
    rank_char = '10' if card_str.rank == 'T' else card_str.rank

    # 获取标准的花色和数值/字母，并拼接成完整的扑克牌表示
    standard_suit = suits.get(suit_char, suit_char)  # 如果suit_char不在suits字典中，则返回它本身
    # standard_card = f"{standard_suit}{rank_char.upper()}"  # 转换为大写字母表示数值或字母

    return Card(standard_suit, rank_char)


translate_dict = {
    'raise': '加注',
    'call': '跟注',
    'fold': '弃牌',
    'check': '过牌',
}

def convert_cards_list(cards_list):
    # 遍历列表中的每个扑克牌表示，并调用convert_card_notation函数进行转换
    converted_list = [convert_card_notation(card) for card in cards_list]
    return converted_list

def deal_community_cards(n):
    # 发n张公共牌的逻辑
    pass

def deal_hand_cards_to_each_player(n):
    # 给每个玩家发n张手牌的逻辑
    pass

def show_hand_cards():
    # 展示手牌的逻辑
    pass

def advance_game_phase():
    # 游戏阶段推进逻辑
    pass

def player_actions(allow_fold=True):
    # 玩家行动逻辑，根据allow_fold参数决定是否允许弃牌
    pass

def show_community_cards(n):
    # 展示前n张公共牌的逻辑
    pass

def show_community_card(n):
    # 展示第n张公共牌的逻辑
    pass

def show_all_hand_cards():
    # 展示所有玩家手牌的逻辑
    pass

def decide_winner():
    # 决定赢家的逻辑
    pass

def clear_points():
    # 清算积分的逻辑
    pass

def reset_game():
    # 游戏重置逻辑
    pass
