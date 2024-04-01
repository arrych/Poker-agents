import streamlit as st
import re
import agent
from points import Points
from poker import Porker
from prompt import rag,characters
from utils import analyse,compare_hands,extract_action_from_text
from web_func import init,new_game,col1_f,col2_f,col3_f,user_action,agent_action,user_action_info,agentL_process_message

# 游戏界面设计
st.header("Leduc Hold'em Poker")

if 'game_state' not in st.session_state:
    init()

# 首次访问页面或需要重置时初始化状态
# 根据游戏状态显示按钮
if st.session_state['role_selected']:
    button_label = "重新开始!"
else:
    button_label = "开始游戏!"

# 角色选择和显示逻辑
if not st.session_state['role_selected']:
    # 显示人物选择界面
    st.sidebar.title("人物选择")
    st.session_state['selected_character'] = st.sidebar.radio(
        "请选择人物：", [character["name"] for character in characters]
    )

    # 显示选定人物的头像和姓名
    for character in characters:
        if character["name"] == st.session_state['selected_character']:
            st.sidebar.image(character["avatar"], width=100)
            st.sidebar.write("姓名：", character["name"])
            st.sidebar.write("性格：", character["personality"])
else:
    # 如果游戏已经开始，显示已选择的角色信息
    role = st.session_state['role']
    st.sidebar.write("已选择的角色：")
    st.sidebar.image(role["avatar"], width=100)
    st.sidebar.write("姓名：", role["name"])
    st.sidebar.write("性格：", role["personality"])

# 游戏开始/重新开始按钮逻辑
if st.sidebar.button(button_label):
    if st.session_state['role_selected']:
        # 如果游戏已开始，点击重新开始游戏
        init()
    else:
        # 如果是初始开始游戏，设置角色选择状态为True
        st.session_state['role_selected'] = True
        selected_character = st.session_state['selected_character']
        st.session_state['role'] = next((character for character in characters if character["name"] == selected_character), None)
        st.session_state.A1,st.session_state.A2,st.session_state.A3 = agent.getAgent(st.session_state['role']['prompt'])
        # 这里添加开始游戏后的代码逻辑
    st.rerun()


# 游戏初始化
st.sidebar.header("聊天区域")
#user_input = st.sidebar.text_input("与机器人聊天:", "")
user_message = st.sidebar.text_input("与Agent聊天:", key="chat")
if st.sidebar.button("发送"):
    st.session_state.chat_history.append(f"你: {user_message}")
    response = agentL_process_message(user_message)
    # 将响应添加到聊天历史记录中  
    #agentG_receive_message(response)
    st.session_state.chat_history.append(f"Agent: {response}")

col1, col2 ,col3= st.columns([1, 1, 1])
# 创建一个空容器用于存放按钮
button_container = st.empty()

# 创建一个按钮
if st.session_state['role_selected']:
    clicked = button_container.button("新的对局!")

    # 如果按钮被点击，则清空容器
    if clicked:
        button_container.empty()
        new_game()
    else:
        pass

# st.title(st.session_state.game_state)
if st.session_state.game_state == 'start' or st.session_state.game_state == 'next':
    # 玩家动作选择  
    action = st.radio("选择你的动作:", ("加注", "跟注", "弃牌"))  

    # confirmed_button = st.empty()
    confirmed = button_container.button("确定")

    # 如果按钮被点击，则清空容器
    if confirmed:
        # 如果用户已经选择了动作并且点击了确认按钮  
        if action is not None:  
                    
            user_action(action)

            # 清除用户选择，以便进行下一轮选择  
            action = None  
            if st.session_state.game_state == "start":
                st.session_state.game_state = "next"
            elif st.session_state.game_state == "next":
                st.session_state.game_state = "end"
                
                points = st.session_state.points
                if not points.IsValid():
                    if points.User > points.Agent:
                        st.success("游戏结束，恭喜获得胜利")
                    else:
                        st.error("游戏结束，请继续努力")
                else:
                    button_container.empty()
                    confirmed = button_container.button("确认")
        else:  
            # 如果用户没有点击确认按钮，则不执行任何操作  
            pass  
    feature_enabled = False
    
    # 添加一个切换按钮，并在按钮旁边显示当前状态
    st.session_state.perspective_eye = st.checkbox('透视眼')
    st.session_state.mind_reading =  st.checkbox('读心术(聊天区 粉色内容就是Agent的分析)')

with col1: 
 col1_f()
with col2:
 col2_f()
with col3:
 col3_f()
    # 展示聊天历史记录  
for message in st.session_state.chat_history:
    if message.startswith("你:"):
        # 用户的消息，靠右显示
        st.sidebar.markdown(f"<p style='text-align: right; color: blue;'>{message}</p>", unsafe_allow_html=True)
    elif message.startswith("Agent:"):
        # Agent的消息，靠左显示
        st.sidebar.markdown(f"<p style='text-align: left; color: green;'>{message}</p>", unsafe_allow_html=True)
    else:
        message = message.replace('\n', '<br>')
        st.sidebar.markdown(f"<p style='text-align: left; color: pink;'>{message}</p>", unsafe_allow_html=True)
    
