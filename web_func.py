import streamlit as st
import re
import agent
from points import Points
from poker import Porker
from prompt import rag,characters
from utils import analyse,compare_hands,extract_action_from_text

def agentL_process_message(message):
    """处理来自聊天界面的消息，并返回一个响应。"""
    # 示例：简单地回显消息
    res = st.session_state.A3(f'{message},[{st.session_state.recording}]') 
    return res['content'] if 'content' in res else '你说啥?我有点耳背,没听清楚,你再说一遍吧'

def init():
    ''' 初始化游戏'''
    st.session_state.game = 0
    st.session_state.points = Points(20)
    st.session_state.porker = Porker()
    st.session_state.game_state = "init"
    st.session_state.chat_history = []
    st.session_state.recording = None
    st.session_state['role_selected'] = False
    st.session_state['selected_character'] = None
    st.session_state.perspective_eye = False
    st.session_state.mind_reading = False

def new_game():
    p = Porker()
    st.session_state.porker = p
    p.LicensingCards() # 发牌
    st.session_state.round = 1
    st.session_state.game += 1
    st.session_state.agent_card_name = p.AgentCardName
    st.session_state.agent_card_id = p.AgentCardId
    st.session_state.your_card_name = p.YourCardName
    st.session_state.your_card_id = p.YourCardId
    st.session_state.community_card_name = p.CommunityCardName
    st.session_state.community_card_id = p.CommunityCardId
    # init -> start -> next -> end
    st.session_state.game_state = "start"
    st.session_state.points.InitBet()   # 每局开始投入1个积分打底
    # 聊天记录
    st.session_state.chat_history = []
    st.session_state.recording = ''

def col1_f():
    st.subheader("玩家区域")
    # 显示积分
    st.metric(label="玩家积分", value=st.session_state.points.User)
    
    if 'game_state' not in st.session_state or st.session_state.game_state == 'init':
        st.image("images/back.jpg", caption="玩家手牌", width=100)
    else:
        hand_card = Porker.id_to_str_map[st.session_state.your_card_id]
        st.image(f"images/{hand_card}.jpg", width=100)

def col2_f():
    # 显示牌
    st.metric(label="底池积分", value=st.session_state.points.Pool)
    if st.session_state.game_state == "next" or st.session_state.game_state == "end" or st.session_state.perspective_eye:
        community_card = Porker.id_to_str_map[st.session_state.community_card_id]
        st.image(f"images/{community_card}.jpg", width=100)
    else:
    	st.image("images/back.jpg", caption="公共牌", width=100)
    
def col3_f():
    st.subheader("Agent区域")
    st.metric(label="Agent积分", value=st.session_state.points.Agent)
    if st.session_state.game_state == "end" or st.session_state.perspective_eye:
        agent_card = Porker.id_to_str_map[st.session_state.agent_card_id]
        st.image(f"images/{agent_card}.jpg", caption="Agent手牌", width=100)
    else: 
        st.image("images/back.jpg", caption="Agent手牌", width=100)
        # 这里添加判定胜负的逻辑

def user_action(action: str):
    points = st.session_state.points
    if action == "弃牌":
        st.error("你选择了弃牌,输掉了本局")
        points.AgentWin()
        temp_str = f'第{st.session_state.game}局第{st.session_state.round}轮,对手弃牌,局结果对手:Lose,积分情况:{points.record()}.'
        st.session_state.recording += temp_str
        st.session_state.A2(st.session_state.recording)
        st.session_state.game_state = "next"
    else:
        st.session_state.recording += f'第{st.session_state.game}局第{st.session_state.round}轮,对手选择了{action}'
        st.success(f"你选择了{action}")
        points.UserAction(actions[action])
        agent_action(action)
    st.session_state.round += 1

def user_action_info(user_action: str) -> str:
    s = f"第{st.session_state.game}局第{st.session_state.round}轮,你有{st.session_state.agent_card_name},"
    if st.session_state.round == 1:
        s = f"{s},对手牌未知,公共牌未知,"
    else:
        s = f"{s},对手牌未知,公共牌{st.session_state.community_card_name},"
    
    return f"{s}对手选择:{user_action}."

    
actions = {"跟注": 0, "加注": 1, "弃牌": 2}

def agent_action(user_action: str):
    points = st.session_state.points
    if st.session_state.round == 1:
        info = user_action_info(user_action)
        if st.session_state.game == 1:
            advise = f"{info}agentA2的建议:最开始不了解对手,无法判断对方是保守还是激进."
        else:
            advise = f"{info}agentA2的建议:{st.session_state.A2(info).content}."
    else:
        analyse_str = analyse(st,st.session_state.agent_card_name, st.session_state.community_card_name)
        advise = f'当前牌面分析:{analyse_str}.'
    os = st.session_state.A1(advise).content
    action = extract_action_from_text(os)
    points.AgentAction(actions[action])

    if  st.session_state.mind_reading:
        st.session_state.chat_history.append(f"Agent内心OS: {os}")

    if action == "弃牌":
        st.error("对手选择了弃牌,你获得了胜利")
        st.session_state.game_state = "next"
    else:
        st.success(f"对手选择了{action}")

        if st.session_state.round == 2:
            result = compare_hands(st)
            points.settlement(result)
            st.session_state.A2(f"第{st.session_state.game}局第{st.session_state.round}轮,局结果:你{result},积分情况:{points.record()}.")
            result = f"对局结果：Agent {result}"
            st.success(result)
            st.session_state.game_state = "next"
