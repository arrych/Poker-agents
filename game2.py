import streamlit as st
import re
import agent
from points import Points
from poker import Porker
from prompt import rag,characters
from utils import analyse,compare_hands,extract_action_from_text
from web_func import init,new_game,col1_f,col2_f,col3_f,user_action,agent_action,user_action_info,agentL_process_message,show_chat

def game2():
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
            st.session_state.A1,st.session_state.A2,st.session_state.A3,st.session_state.A4 = agent.getAgent(st.session_state['role']['prompt'])
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
    
    def wait_chat():
        st.session_state.A4()
        res = st.session_state.A4(f'speak')
        res = res['content'] if 'content' in res else '等一下 让我想想'
        st.session_state.chat_history.append(f"Agent: {res}")
    
    # st.title(st.session_state.game_state)
    if st.session_state.game_state == 'start' or st.session_state.game_state == 'next':
        # 玩家动作选择  
        action = st.radio("选择你的动作:", ("加注", "跟注", "弃牌"))  
    
        # confirmed_button = st.empty()
        confirmed = button_container.button("确定")
    
        # 如果按钮被点击，则清空容器
        if confirmed:
            # 如果用户已经选择了动作并且点击了确认按钮  
    
            execute_function = False
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
                            st.error("游戏结束，你输了,请继续努力")
                        init()
                    button_container.empty()
                    confirmed = button_container.button("确认")
            else:  
                # 如果用户没有点击确认按钮，则不执行任何操作  
                pass  
        feature_enabled = False
        # 添加一个切换按钮，并在按钮旁边显示当前状态
        if 'perspective_eye' not in st.session_state:
            st.session_state.perspective_eye = True  # 设置默认值为 True 或 False
        
        if 'mind_reading' not in st.session_state:
            st.session_state.mind_reading = False  # 设置默认值为 True 或 False
        
        perspective_eye = st.checkbox('透视眼', value=st.session_state.perspective_eye)
        mind_reading = st.checkbox('读心术(聊天区 粉色内容就是Agent的分析)', value=st.session_state.mind_reading)
        
        # 在每一轮结束时更新 session_state
        st.session_state.perspective_eye = perspective_eye
        st.session_state.mind_reading = mind_reading
    
    guilden_line = st.checkbox("展示游戏规则",value=True)
    
    if guilden_line:
        st.markdown("""
        <div class="hint" style="background-color: rgba(255, 255, 0, 0.15); padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #ffcc00;">
            <p>🌟🌟 如果在游戏过程中发现问题或者有一些建议希望可以进行一下交流，我们会及时反馈。如果觉得不错点击一下小心心就更好好啦!</p>
            <p>1：这是一个两人对战游戏。一共6张牌，红桃/黑桃的J、Q、K</p>
            <p>2: 游戏一共分为两轮,每轮都可以进行一次动作选择（加注、跟注、弃牌）。游戏开始每名玩家都会抽一张手牌，并在桌上在放置一张公用的牌。</p>
            <p>3：第一轮只能看到自己的手牌,然后选择动作。第二轮展示公共牌，进行第二轮下注。最后结算积分进行下一局。</p>
            <p>4：如果手牌与公共牌凑齐对子(比如手牌是黑桃J,公共牌是红桃J),则为最大牌；没有双方都没有凑成对子，则按点数比较大小。K>Q>J。</p>
            <p>5：游戏开始前你可以选择不同性格的对手，会他们影响后续的动作决策；游戏过程中你可以与Agent进行聊天来刺探情报或者施加压力(让其弃牌)。</p>
            <p>🌟 使用模型分析需要一点时间,请耐心等待,如果好奇Agent分析内容可以点击读心术来查看其内心独白。</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col1: 
     col1_f()
    with col2:
     col2_f()
    with col3:
     col3_f()
        # 展示聊天历史记录  
    show_chat(st)
