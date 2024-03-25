import streamlit as st
import re
import agent
from points import Points
from poker import Porker
from prompt import rag

id_to_str_map = {0: "SJ", 1: "HJ", 2: "SQ", 3: "HQ", 4: "SK", 5: "HK"}


def agentL_process_message(message):
    """处理来自聊天界面的消息，并返回一个响应。"""
    # 示例：简单地回显消息
    res = st.session_state.A3(f'{message},[{st.session_state.recording}]') 
    return res['content'] if 'content' in res else '你说啥?我有点耳背,没听清楚,你再说一遍吧'

def agentG_receive_message(message):
    """将消息显示在游戏界面。这里可以根据需要进行扩展，比如改变游戏状态。"""
    st.session_state.agentG_message = message

def init():
    ''' 初始化游戏'''
    st.session_state.A1,st.session_state.A2,st.session_state.A3 = agent.getAgent()
    st.session_state.game = 0
    st.session_state.points = Points(20)
    st.session_state.porker = Porker()
    st.session_state.game_state = "init"
    st.session_state.chat_history = []
    st.session_state.recording = ''

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
        st.image("back.jpg", caption="公共牌", width=100)
    else:
        hand_card = id_to_str_map[st.session_state.your_card_id]
        st.image(f"{hand_card}.jpg", width=100)

def col2_f():
    # 显示牌
    st.metric(label="底池积分", value=st.session_state.points.Pool)
    if st.session_state.game_state == "next" or st.session_state.game_state == "end":
        community_card = id_to_str_map[st.session_state.community_card_id]
        st.image(f"{community_card}.jpg", width=100)
    else:
    	st.image("back.jpg", caption="公共牌", width=100)
    
def col3_f():
    st.subheader("Agent区域")
    st.metric(label="Agent积分", value=st.session_state.points.Agent)
    if st.session_state.game_state == "end":
        agent_card = id_to_str_map[st.session_state.agent_card_id]
        st.image(f"{agent_card}.jpg", caption="Agent手牌", width=100)
    else: 
        st.image("back.jpg", caption="Agent手牌", width=100)
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

def extract_action_from_text(text):
    # 正则表达式，匹配action: 后面的内容，直到换行符或字符串结束
    action_pattern = r"action: (.+)"
    match = re.search(action_pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()  # 提取匹配到的动作并去除两端的空白字符
    else:
        return "弃权"
    
actions = {"跟注": 0, "加注": 1, "弃牌": 2}

def analyse(player_hand, community_card):
    cards = ["黑桃K", "红桃K", "黑桃Q", "红桃Q", "黑桃J", "红桃J"]
    remaining_cards = [
        card for card in cards if card not in [player_hand, community_card]
    ]
    results = {"Win": 0, "Lose": 0, "Draw": 0}
    output_lines = []  # 创建一个空列表来存储输出字符串

    # 遍历所有可能的对手手牌
    for opponent_hand in remaining_cards:
        result = compare_hands_in(player_hand, opponent_hand, community_card)
        results[result] += 1
        output_lines.append(
            f"当对手手牌是: {opponent_hand}, 结局: {result}"
        )  # 将输出添加到列表中

    total_combinations = sum(results.values())
    for outcome in results:
        probability = results[outcome] / total_combinations
        output_lines.append(
            f"{outcome} 的概率: {probability:.2f}"
        )  # 将概率输出添加到列表中

    return "\n".join(output_lines)  # 使用换行符将列表中的字符串连接起来，并返回结果

# 计算牌的点数
def card_value(card):
    if "K" in card:
        return 3
    elif "Q" in card:
        return 2
    else:
        return 1
    
def compare_hands_in(player_hand, opponent_hand, community_card):
    player_pair = player_hand[2] == community_card[2]
    opponent_pair = opponent_hand[2] == community_card[2]
    player_score = card_value(player_hand)
    opponent_score = card_value(opponent_hand)
    if player_pair and not opponent_pair:
        return "Win"
    elif not player_pair and opponent_pair:
        return "Lose"
    elif player_score > opponent_score:
        return "Win"
    elif player_score < opponent_score:
        return "Lose"
    else:
        return "Draw"
    

# 比较两手牌的结果
def compare_hands():
    player_hand, opponent_hand, community_card = st.session_state.your_card_name,st.session_state.agent_card_name,st.session_state.community_card_name
    compare_hands_in(player_hand, opponent_hand, community_card)

def agent_action(user_action: str):
    points = st.session_state.points
    if st.session_state.round == 1:
        info = user_action_info(user_action)
        if st.session_state.game == 1:
            advise = f"{info}agentA2的建议:最开始不了解对手,无法判断对方是保守还是激进."
        else:
            advise = f"{info}agentA2的建议:{st.session_state.A2(info).content}."
    else:
        analyse_str = analyse(st.session_state.agent_card_name, st.session_state.community_card_name)
        advise = f'当前对手牌面分析:{analyse_str}.'
    action = extract_action_from_text(st.session_state.A1(advise).content+f'其他对局的数据参考:{rag}')
    points.AgentAction(actions[action])

    if action == "弃牌":
        st.error("对手选择了弃牌,你获得了胜利")
        st.session_state.game_state = "next"
    else:
        st.success(f"对手选择了{action}")

        if st.session_state.round == 2:
            result = compare_hands()
            points.settlement(result)
            st.session_state.A2(f"第{st.session_state.game}局第{st.session_state.round}轮,局结果对手:{result},积分情况:{points.record()}.")
            result = f"对局结果：{result}"
            st.success(result)
            st.session_state.game_state = "next"


# 游戏界面设计
st.header("Leduc Hold'em Poker")

if st.button("重新开始!"):	
    init()
# 游戏初始化
if 'game_state' not in st.session_state:
    init()

cards = ["SK", "HK", "SQ", "HQ", "SJ", "HJ"]
st.sidebar.header("聊天区域")
#user_input = st.sidebar.text_input("与机器人聊天:", "")
user_message = st.sidebar.text_input("与Agent聊天:", key="chat")
if st.sidebar.button("发送"):
    st.session_state.chat_history.append(f"你: {user_message}")
    response = agentL_process_message(user_message)
    # 将响应添加到聊天历史记录中  
    agentG_receive_message(response)
    st.session_state.chat_history.append(f"Agent: {response}")

col1, col2 ,col3= st.columns([1, 1, 1])
# 创建一个空容器用于存放按钮
button_container = st.empty()

# 创建一个按钮
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
            # user_action = action  # 存储用户选择的动作  
                    
            # 根据用户的选择显示不同的消息，并在这里添加相应的处理逻辑  
            # if user_action == "加注":  
            #     st.success("你选择了加注")  
            #     # 这里添加处理逻辑  
            # elif user_action == "跟注":  
            #     st.success("你选择了跟注")  
            #     # 这里添加处理逻辑  
            # elif user_action == "弃牌":  
            #     st.error("你选择了弃牌")  
            #     # 这里添加处理逻辑  
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
                    clicked = button_container.button("确认结果")
        else:  
            # 如果用户没有点击确认按钮，则不执行任何操作  
            pass  

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
    else:
        # Agent的消息，靠左显示
        st.sidebar.markdown(f"<p style='text-align: left; color: green;'>{message}</p>", unsafe_allow_html=True)
