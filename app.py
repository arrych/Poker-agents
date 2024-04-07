import agentscope
import streamlit as st
from game1 import game1
from game2 import game2

# 设置页面配置
st.set_page_config(page_title="游戏选择", page_icon=":video_game:", layout="wide")
# 定义游戏信息
games_info = {
    "Leduc Hold'em Poker": {
        "描述": "简化版的德州扑克。",
        "图片链接": "images/game1.jpg", 
        "更多信息": "基础版本,没有经验可以先行体验这个版本。"
    },
    "Limit Texas Hold'em": {
        "描述": "标准版的德州扑克,欢迎体验。",
        "图片链接": "images/game2.jpg",  
        "更多信息": "实现中,请耐心等待"
    }
}

# 初始化会话状态
if 'page' not in st.session_state:
    st.session_state.page = '选择界面'
if 'selected_game' not in st.session_state:
    st.session_state.selected_game = None

st.markdown("""
<style>
    body {
        background-color: #f0f2f6;
        font-family: Arial, sans-serif;
    }
    .stButton>button {
        background-color: #1c83e1;
        color: white;
        padding: 8px 20px;
        border-radius: 4px;
        font-size: 16px;
    }
    .stTextInput>div>div>input {
        border: 1px solid #ddd;
        padding: 8px;
        border-radius: 4px;
    }
    h1 {
        color: #1c83e1;
    }
    h2 {
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

def render_game_selection():
    st.title("选择你想玩的游戏")
    
    games = list(games_info.keys())
    num_cols = 2
    cols = st.columns(num_cols)
    
    for i, game in enumerate(games):
        with cols[i % num_cols]:
            with st.expander(game, expanded=True):
                st.image(games_info[game]["图片链接"], use_column_width=True)
                st.write(games_info[game]["描述"])
                if st.button(f"开始玩 {game}"):
                    st.session_state.selected_game = game
                    st.session_state.page = '游戏界面'
                    st.rerun()

            
# 游戏详情界面
def render_game_page():
    game = games_info[st.session_state.selected_game]
    
    st.title(f"欢迎来到{st.session_state.selected_game}")
    if st.session_state.selected_game == "Leduc Hold'em Poker":
        game1()
        if st.button("返回游戏选择主界面"):
            st.session_state.page = '选择界面'
            st.rerun()
    else:
        if st.button("返回游戏选择主界面"):
            st.session_state.page = '选择界面'
            st.rerun()
        game2()

# 根据当前会话状态渲染相应界面
if st.session_state.page == '选择界面':
    render_game_selection()
elif st.session_state.page == '游戏界面':
    render_game_page()
