import streamlit as st

def agentL_process_message(message):
    """处理来自聊天界面的消息，并返回一个响应。"""
    # 示例：简单地回显消息
    return f"AgentL received your message: {message}"

def agentG_receive_message(message):
    """将消息显示在游戏界面。这里可以根据需要进行扩展，比如改变游戏状态。"""
    st.session_state.agentG_message = message

def main():
    # 初始化session state变量
    if 'agentG_message' not in st.session_state:
        st.session_state.agentG_message = 'No messages yet.'

    # 创建两列：左边是聊天界面，右边是游戏界面
    col1, col2 = st.columns(2)

    with col1:
        st.write("Chat Interface")
        user_message = st.text_input("Enter your message:", key="chat")
        if st.button("Send"):
            response = agentL_process_message(user_message)
            agentG_receive_message(response)

    with col2:
        st.write("Game Interface")
        # 显示从agentL接收的消息
        st.write(f"Message from AgentL: {st.session_state.agentG_message}")
        
        # 简单的游戏逻辑（猜数字游戏）
        guess = st.number_input("Guess a number between 1 and 10", min_value=1, max_value=10, key="guess")
        if st.button("Guess"):
            answer = 5  # 假设答案是5
            if guess == answer:
                st.success("You guessed it right!")
            else:
                st.error("Try again!")

if __name__ == "__main__":
    main()


import streamlit as st
import random

# 初始化或获取游戏状态
if 'game_state' not in st.session_state:
    st.session_state.game_state = "start"
if 'agent_card' not in st.session_state:
    st.session_state.agent_card = random.choice(['A', 'K', 'Q'])
if 'community_card' not in st.session_state:
    st.session_state.community_card = random.choice(['A', 'K', 'Q'])
if 'hand_card' not in st.session_state:
    st.session_state.hand_card = random.choice(['A', 'K', 'Q'])

st.header("Leduc Hold'em Poker")

# 聊天侧边栏（示例，根据需要实现）
with st.sidebar:
    st.text_input("发送消息", key="chat_message")
    if st.button("发送"):
        # 这里实现发送消息的逻辑
        pass

# 游戏界面设计
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.subheader("机器人手牌")
    agent_score = 0  # 这里设置机器人初始积分
    st.metric(label="机器人积分", value=agent_score)
    st.image("back.jpg", caption="Agent手牌", width=100)

with col2:
    player_score = 0  # 这里设置玩家初始积分
    st.metric(label="底池积分", value=player_score)
    st.image("back.jpg", caption="公共牌", width=100)

with col3:
    st.subheader("玩家区域")
    st.metric(label="玩家积分", value=player_score)
    st.image(f"{st.session_state.hand_card}.jpg", width=100)

action = st.radio("选择你的动作:", ("加注", "跟注", "弃牌"), key="player_action")

if st.button("确认动作"):
    # 根据玩家选择的动作更新游戏状态
    st.session_state.game_state = "next_round"  # 举例更新状态，需要根据游戏逻辑调整
    # 显示选择结果
    st.write(f"你选择了：{action}")

# 根据游戏状态决定是否显示机器人牌和下一步操作
if st.session_state.game_state == "next_round":
    # 这里可以根据实际游戏逻辑添加代码，比如显示机器人牌，判断胜负等
    pass
