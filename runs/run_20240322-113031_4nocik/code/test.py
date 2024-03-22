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
