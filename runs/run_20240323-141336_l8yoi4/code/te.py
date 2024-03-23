import streamlit as st  
import random  
  
# 初始化游戏状态  
if 'game_state' not in st.session_state:  
    st.session_state.game_state = {'score': 0, 'game_over': False}  
  
# 游戏逻辑函数  
def play_game():  
    if not st.session_state.game_state['game_over']:  
        # 这里是你的游戏逻辑代码  
        # 假设游戏是通过点击按钮来随机增加分数  
        if st.button('Play Game'):  
            st.session_state.game_state['score'] += random.randint(1, 10)  
            st.write(f"Current Score: {st.session_state.game_state['score']}")  
        # 添加一些条件来结束游戏  
        if st.session_state.game_state['score'] >= 100:  
            st.session_state.game_state['game_over'] = True  
            st.write("Game Over!")  
  
# 聊天区域  
def chat_area():  
    message = st.text_input('Enter your message')  
    if st.button('Send'):  
        st.write(f"You sent: {message}")  
  
# 主界面布局  
st.sidebar.title('Chat Area')  
chat_area()  
  
st.title('Game Area')  
#play_game()  
  
# 如果你需要在页面加载时不立即渲染游戏，可以添加条件判断  
if not 'game_initialized' in st.session_state or not st.session_state.game_initialized:  
    play_game()  
    st.session_state.game_initialized = True
