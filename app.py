import agentscope
import streamlit as st
from game1 import game1
from game2 import game2

# 定义游戏信息
games_info = {
    "Leduc Hold'em Poker": {
        "描述": "简化版的德州扑克。",
        "图片链接": "images/game1.jpg", 
        "更多信息": "基础版本,没有经验可以先行体验这个版本。"
    },
    "Leduc Hold'em Poker Plus": {
        "描述": "强化版本。",
        "图片链接": "images/game2.jpg",  
        "更多信息": "实现中,请耐心等待..."
    }
}

# 初始化会话状态
if 'page' not in st.session_state:
    st.session_state.page = '选择界面'
if 'selected_game' not in st.session_state:
    st.session_state.selected_game = None

# 游戏详情界面
def render_game_page():
    game = games_info[st.session_state.selected_game]
    
    st.title(f"欢迎来到{st.session_state.selected_game}")
    if st.session_state.selected_game == "Leduc Hold'em Poker":
        game1()
    else:
        game2()
    if st.button("返回游戏选择主界面"):
        st.session_state.page = '选择界面'
        st.rerun()

# 游戏选择界面
def render_game_selection():
    st.title("选择你想玩的游戏")
    choice = st.radio("请选择一个游戏：", list(games_info.keys()))
    
    # 当用户做出选择并点击确认时，更新会话状态
    if st.button("确认"):
        st.session_state.selected_game = choice
        st.session_state.page = '游戏界面'
        st.rerun()

    if choice:
        game = games_info[choice]
    
        # 创建两列，每列宽度相等
        col1, col2 = st.columns([1, 1])
        # 显示游戏信息
        with col1:
            st.image(game["图片链接"], width=300)
        with col2:
            st.subheader(choice)
            st.write(game["描述"])
            st.expander("更多信息").write(game["更多信息"])

# 设置页面配置
st.set_page_config(page_title="游戏选择", page_icon=":video_game:", layout="wide")

# 根据当前会话状态渲染相应界面
if st.session_state.page == '选择界面':
    render_game_selection()
elif st.session_state.page == '游戏界面':
    render_game_page()
