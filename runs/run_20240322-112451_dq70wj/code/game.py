import streamlit as st
import random
import agent


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
# 游戏初始化
cards = ["SK", "HK", "SQ", "HQ", "SJ", "HJ"]
player_score = 0
agent_score = 0
st.sidebar.header("聊天区域")
#user_input = st.sidebar.text_input("与机器人聊天:", "")
user_message = st.sidebar.text_input("与Agent聊天:", key="chat")
if st.sidebar.button("发送"):
    response = agentL_process_message(user_message)
    agentG_receive_message(response)


if st.button("重新开始!"):	
	init()
# 游戏界面设计
st.header("Leduc Hold'em Poker")

col1, col2 ,col3= st.columns([1, 1,1])

with col1:
    st.subheader("机器人手牌")
    st.metric(label="机器人积分", value=agent_score)
    agent_card = random.choice(cards)
    st.image("back.jpg", caption="Agent手牌", width=100)

with col2:
    # 显示牌
    community_card = random.choice(cards)
    
    st.metric(label="底池积分", value=player_score)
    if st.button("展示公共牌"):
        st.image(f"{community_card}.jpg", width=100)
    else:
    	st.image("back.jpg", caption="公共牌", width=100)


with col3:
    st.subheader("玩家区域")
    # 显示积分
    st.metric(label="玩家积分", value=player_score)
    hand_card = random.choice(cards)
    
    st.image(f"{hand_card}.jpg", width=100)
    # 玩家动作选择  
    action = st.radio("选择你的动作:", ("加注", "跟注", "弃牌"))  
      
    # 确认按钮  
    if st.button("动作"):  
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
    else:  
        # 如果用户没有点击确认按钮，则不执行任何操作  
        pass  

    if st.button("摊牌"):
        st.image(f"{agent_card}.jpg", caption="机器人手牌", width=100)
        # 这里添加判定胜负的逻辑
