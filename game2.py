import streamlit as st

import rlcard
from agent2_rule import LimitholdemRuleAgentV1, LimitholdemRuleAgentV2
import agentscope
from agent2_rule import RandomAgent
from npc import Npc, set_audiences, Player
from utils2 import CardDeck, Card, BackCard
import round
import time

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
player_list_raw = [
    {'name': 'YOU', 'avatar': 'assets/avatars/player.png'},
    {'name': 'NPC_1', 'avatar': 'assets/avatars/npc1.png'},
    {'name': 'NPC_2', 'avatar': 'assets/avatars/npc1.png'},
    {'name': 'NPC_3', 'avatar': 'assets/avatars/npc1.png'},
    {'name': 'NPC_4', 'avatar': 'assets/avatars/npc1.png'},
    {'name': 'NPC_5', 'avatar': 'assets/avatars/npc1.png'}
]

community_cards = st.session_state.community_cards = []
user_cards = st.session_state.community_cards = []
# 牌库
card_deck = st.session_state.card_deck = CardDeck()
# 奖池
jackpot = st.session_state.jackpot = 0


def game2():

    st.session_state.round = round.pre_flop_round  # 控制阶段
    # 初始化游戏状态，包括玩家信息、奖池等
    # game_phase: pre-flop -> flop -> turn -> river -> showdown
    if 'game_phase' not in st.session_state:
        init()

    gulden_line()
    game_info = st.session_state.game_info
    st.session_state.jackpot = 0
    st.session_state.community_cards = convert_cards_list(game_info.game.public_cards)
    state_info = st.session_state.state
    player_id = st.session_state.player_id

    trajectories = [[] for _ in range(game_info.num_players)]
    st.session_state.curr_payoffs[game_info.game.round_counter] = sum(game_info.game.round.raised)*2
    # todo 翻译日志
    trajectories[player_id].append(state_info)
    st.session_state.action = 'check'
    st.session_state.hand_cards[0] = convert_cards_list(game_info.game.players[0].hand)
    if st.sidebar.button("重新开始!"):
        init()
    show(game_info, state_info, player_id, trajectories)

    if not game_info.is_over() and not st.session_state['continue']:
        if player_id == 0:
            # action = user_step(state_info)
            st.session_state['continue'] = True
        else:
            # 机器人行动
            action = game_info.agents[player_id].step(state_info)
            #st.write(f"action: {action}  -> state_info['raw_legal_actions']={state_info['raw_legal_actions']}")
            # todo 了解action为什么会越界 是不是应该取所有的action
            print(f'action={action}')
            st.session_state.action = action
            if player_id == 1 or player_id == 2 or player_id == 3 or player_id == 5:
               st.session_state.broadcast_npc.step2(st.session_state.player_list[player_id]['name'], action)

            player = game_info.game.players[player_id]
            step(game_info, state_info, player_id, action, trajectories)
            st.session_state.agent_actions[player_id-1] = [st.session_state.action, player.in_chips*2]
            st.session_state.hand_cards[player_id] = convert_cards_list(player.hand)

    if game_info.is_over():
        payoffs = game_info.game.get_payoffs()
        st.session_state.payoffs = st.session_state.payoffs + payoffs*2
        if payoffs[0] > 0:
            st.success(f'You win {payoffs[0]*2} chips!')
        elif payoffs[0] == 0:
            st.info('It is a tie.')
        else:
            st.error(f'You lose {-payoffs[0]*2} chips!')
        if st.button("新的一局!"):
            new_game()
            st.rerun()

        st.stop()

    st.rerun()


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


def show(game_info, state_info, player_id, trajectories):

    canvas = st.columns(1)[0]
    # 第二行：公共信息区
    round.show_game_round_step(canvas)
    canvas.subheader(
        f"本轮奖池累积至{sum(game_info.game.round.raised)*2}积分,桌面总积分至{sum(st.session_state.curr_payoffs)},现在轮到{st.session_state.player_list[player_id]['name']}行动……")   # 使用分隔线创建视觉上的行分隔
    row = canvas.container(border=True)
    row.caption("公共牌")
    round.show_community_cards(row)
    canvas.divider()

    # 第三行：用户操作界面
    player_canvas = canvas.container(border=True)
    player_cols = player_canvas.columns(6)
    player_cols[0].image(st.session_state.player_list[0]['avatar'], caption=st.session_state.player_list[0]['name'])
    player_cols[1].image(st.session_state.hand_cards[0][0].image_path)  # NPC手牌图片
    player_cols[2].image(st.session_state.hand_cards[0][1].image_path)  # NPC手牌图片

    operate_menu = player_cols[3]

    ability_menu = player_cols[4]
    ability_menu.write('你的能力')
    ability_menu.toggle(label='读心术', key='read_mind',disabled=True)
    ability_menu.toggle(label='透视眼', key='see_through', disabled=True)
    bet_statistic = player_cols[5]
    player = game_info.game.players[0]
    round.player_act(bet_statistic, player.in_chips*2, st.session_state.payoffs[0])

    with st.sidebar:
        for i, npc in enumerate(st.session_state.player_list[1:]):  # 展示后五个NPC
            i = i + 1
            row = st.container(border=True)
            cols = row.columns(4)

            cols[0].image(npc['avatar'], caption=npc['name'])  # NPC头像和姓名
            agent_action = st.session_state.agent_actions[i-1]
            if agent_action[0] == 'fold' or game_info.game.is_over():
                cols[1].image(st.session_state.hand_cards[i][0].image_path)  # NPC手牌图片
                cols[2].image(st.session_state.hand_cards[i][1].image_path)  # NPC手牌图片
            else:
                cols[1].image(Card.BACK_IMAGE_PATH)  # NPC手牌图片
                cols[2].image(Card.BACK_IMAGE_PATH)  # NPC手牌图片

            if agent_action[0] != '':
                round.npc_act(npc, cols[3], agent_action[0], agent_action[1])

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


def init():
    # 初始化游戏状态逻辑
    # 需要定义玩家列表、奖池大小、游戏阶段等
    game_info = rlcard.make('limit-holdem', config={'game_num_players': 6})
    # human_agent = HumanAgent(game_info.num_actions)
    agentscope.init(
        model_configs="./config/model_configs.json"
    )
    # 初始化session_state
    st.session_state.broadcast_npc = Player(name='test',
                           avatar='test',
                           num_actions=6)
    player = st.session_state.player = Player(name=player_list_raw[0]['name'],
                    avatar=player_list_raw[0]['avatar'],
                    num_actions=game_info.num_actions)
    # agent_1 = Npc(name=player_list_raw[1]['name'],
    #               avatar=player_list_raw[1]['avatar'],
    #               num_actions=game_info.num_actions)
    # agent_2 = Npc(name=player_list_raw[2]['name'],
    #               avatar=player_list_raw[2]['avatar'],
    #               num_actions=game_info.num_actions)
    agent_1 = LimitholdemRuleAgentV1()
    agent_2 = LimitholdemRuleAgentV1()
    agent_3 = LimitholdemRuleAgentV2()
    # agent_3 = Npc(name=player_list_raw[3]['name'],
    #               avatar=player_list_raw[3]['avatar'],
    #               num_actions=game_info.num_actions)
    agent_4 = Npc(name=player_list_raw[4]['name'],
                  avatar=player_list_raw[4]['avatar'],
                  num_actions=game_info.num_actions)
    # agent_5 = Npc(name=player_list_raw[5]['name'],
    #               avatar=player_list_raw[5]['avatar'],
    #               num_actions=game_info.num_actions)
    agent_5 = RandomAgent(num_actions=game_info.num_actions)

    set_audiences(participants=[player, agent_4, st.session_state.broadcast_npc])
    game_info.set_agents([
        player,
        agent_1, agent_2, agent_3, agent_4, agent_5
    ])
    st.session_state.game_info = game_info
    st.session_state.round_info = game_info.game.round
    st.session_state.player_list = player_list_raw
    st.session_state.players = [player, agent_1, agent_2, agent_3, agent_4, agent_5]
    game_info.set_agents(st.session_state.players)
    st.session_state.game_phase = "pre-flop"
    st.session_state['continue'] = False
    st.session_state.state, st.session_state.player_id = st.session_state.game_info.reset()
    st.session_state.agent_actions = [['', 0], ['', 0], ['', 0], ['', 0], ['', 0]]  # index=0 为动作 index=1 为积分
    st.session_state.payoffs = [120, 120, 120, 120, 120, 120]
    st.session_state.curr_payoffs = [0, 0, 0, 0, 0, 0]
    st.session_state.hand_cards = [[BackCard(), BackCard()], [BackCard(), BackCard()], [BackCard(), BackCard()],
                                   [BackCard(), BackCard()], [BackCard(), BackCard()], [BackCard(), BackCard()]]  # 说话人
    st.session_state.perspective_eye = False
    st.session_state.mind_reading = False
    pass


def new_game():
    st.session_state.state, st.session_state.player_id = st.session_state.game_info.reset()
    st.session_state['continue'] = False
    st.session_state.round_info = st.session_state.game_info.game.round
    st.session_state.agent_actions = [['', 0], ['', 0], ['', 0], ['', 0], ['', 0]]  # index=0 为动作 index=1 为积分
    st.session_state.hand_cards = [[BackCard(), BackCard()], [BackCard(), BackCard()], [BackCard(), BackCard()],
                                   [BackCard(), BackCard()], [BackCard(), BackCard()], [BackCard(), BackCard()]]
    st.session_state.curr_payoffs = [0, 0, 0, 0, 0, 0]


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


@st.cache_data
def gulden_line():
    st.expander("展示游戏规则").markdown("""
        <div class="hint" style="background-color: rgba(255, 255, 0, 0.15); padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #ffcc00;">
            <p>🌟🌟 如果在游戏过程中发现问题或者有一些建议希望可以进行一下交流，我们会及时反馈。如果觉得不错点击一下小心心就更好啦!</p>
            <p>1：游戏已经升级成标准的德州扑克游戏,默认会有5个对手,其中一个随机操作的机器人,两个不同算法的机器人以及两个由multi-agent组成的机器人</p>
            <p>2：目前可以体验完整的游戏流程,但是没有更新聊天功能以及角色能力,如果想要获得更丰富的multi-agent体验.建议去玩简单版本</p>
            <p>🌟 使用模型分析需要一点时间,请耐心等待,如果好奇Agent分析内容可以点击读心术来查看其内心独白。</p>
        </div>
        """, unsafe_allow_html=True)
