import streamlit as st
import random
import agent
from points import Points
from poker import Porker

id_to_str_map = {0: "SJ", 1: "HJ", 2: "SQ", 3: "HQ", 4: "SK", 5: "HK"}

def agentL_process_message(message):
    """处理来自聊天界面的消息，并返回一个响应。"""
    # 示例：简单地回显消息
    return f"AgentL received your message: {message}"

def agentG_receive_message(message):
    """将消息显示在游戏界面。这里可以根据需要进行扩展，比如改变游戏状态。"""
    st.session_state.agentG_message = message

def init():
    ''' 初始化游戏'''
    st.session_state.A1,st.session_state.A2,st.session_state.A3 = agent.getAgent()
    st.session_state.game = 1
    st.session_state.points = Points(20)
    st.session_state.porker = Porker()
    st.session_state.game_state = "init"

def new_game():
    p = st.session_state.porker
    p.LicensingCards() # 发牌
    st.session_state.round = 1
    st.session_state.agent_card_name = p.AgentCardName
    st.session_state.agent_card_id = p.AgentCardId
    st.session_state.your_card_name = p.YourCardName
    st.session_state.your_card_id = p.YourCardId
    # init -> start -> next -> end
    st.session_state.game_state = "start"

def col1_f():
    st.subheader("玩家区域")
    # 显示积分
    st.metric(label="玩家积分", value=st.session_state.points.User)
    
    if 'game_state' not in st.session_state or st.session_state.game_state == 'init':
    	st.image("back.jpg", caption="公共牌", width=100)
    else:
        hand_card = id_to_str_map[st.session_state.your_card_id]
        st.image(f"{hand_card}.jpg", width=100)
    # 玩家动作选择  
    action = st.radio("选择你的动作:", ("加注", "跟注", "弃牌"))  
      
    # 确认按钮  
    if st.button("确定"):  
        # 如果用户已经选择了动作并且点击了确认按钮  
        if action is not None:  
            user_action = action  # 存储用户选择的动作  
              
            # 根据用户的选择显示不同的消息，并在这里添加相应的处理逻辑  
            if user_action == "加注":  
                st.success("你选择了加注")  
                # 这里添加处理逻辑  
            elif user_action == "跟注":  
                st.success("你选择了跟注")  
                # 这里添加处理逻辑  
            elif user_action == "弃牌":  
                st.error("你选择了弃牌")  
                # 这里添加处理逻辑  
              
            # 清除用户选择，以便进行下一轮选择  
            action = None  
        if st.session_state.game_state == "start":
            st.session_state.game_state = "next"
        elif st.session_state.game_state == "next":
            st.session_state.game_state = "end"
    else:  
        # 如果用户没有点击确认按钮，则不执行任何操作  
        pass  

def col2_f():
    # 显示牌
    community_card = random.choice(cards)
    
    st.metric(label="底池积分", value=st.session_state.points.Pool)
    if st.session_state.game_state == "next" or st.session_state.game_state == "end":
        st.image(f"{community_card}.jpg", width=100)
    else:
    	st.image("back.jpg", caption="公共牌", width=100)
    
def col3_f():
    st.subheader("Agent手牌")
    st.metric(label="Agent积分", value=st.session_state.points.Agent)
    agent_card = random.choice(cards)
    if st.session_state.game_state == "end":
        st.image(f"{agent_card}.jpg", caption="Agent手牌", width=100)
    else: 
        st.image("back.jpg", caption="Agent手牌", width=100)
        # 这里添加判定胜负的逻辑

# 游戏界面设计
st.header("Leduc Hold'em Poker")

if st.button("重新开始!"):	
    init()
# 游戏初始化
if 'game_state' not in st.session_state:
    init()
    if st.button("开始玩!"):
        new_game()
else:
    if st.button("下一局!"):	
        new_game()


st.title(st.session_state.game_state)
cards = ["SK", "HK", "SQ", "HQ", "SJ", "HJ"]
st.sidebar.header("聊天区域")
#user_input = st.sidebar.text_input("与机器人聊天:", "")
user_message = st.sidebar.text_input("与Agent聊天:", key="chat")
if st.sidebar.button("发送"):
    response = agentL_process_message(user_message)
    agentG_receive_message(response)




col1, col2 ,col3= st.columns([1, 1, 1])

with col1:
 col1_f()
with col2:
 col2_f()
with col3:
 col3_f()
