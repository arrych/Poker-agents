import re

actions = {"跟注": 0, "加注": 1, "弃牌": 2}


def extract_action_from_text(text):
    # 正则表达式，匹配action: 后面的内容，直到换行符或字符串结束
    action_pattern = r"action: (.+)"
    match = re.search(action_pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()  # 提取匹配到的动作并去除两端的空白字符
    else:
        return "弃权"

# 计算牌的点数
def card_value(card):
    if "K" in card:
        return 3
    elif "Q" in card:
        return 2
    else:
        return 1

# 比较两手牌的结果
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
def compare_hands(st):
    player_hand, opponent_hand, community_card = st.session_state.agent_card_name,st.session_state.your_card_name,st.session_state.community_card_name
    return compare_hands_in(player_hand, opponent_hand, community_card)

def bet_result_str(result: str) -> str:  
    if result == "Win":  
        return "你获胜"  
    elif result == "Lose":  
        return "对手获胜"  
    else:  
        return "平局"


def analyse(st,player_hand, community_card):
    cards = ["黑桃J", "红桃J", "黑桃Q", "红桃Q", "黑桃K", "红桃K"]
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
def validate_action_num(action_num):  
    # 首先检查是否为整数类型  
    if not isinstance(action_num, int):  
        raise ValueError("action_num 必须是整数类型,修改为默认值2")  
      
    # 然后检查是否在0, 1, 2之中  
    if action_num not in [0, 1, 2]:  
        action_num = 2  
      
    return action_num 

def get_input():
    user_input = input("请输入一个数字 \n 0:跟注 1:加注 2:弃牌 : ")
    try:
        return validate_action_num(int(user_input))
    except ValueError:
        print("对不起，你输入的不是一个有效的整数。")
        return 2


