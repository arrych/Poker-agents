import random
from typing import Dict

import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from utils import Card, CardDeck

pre_flop_round = 'pre_flop'
flop_round = 'flop'
turn_round = 'turn'
river_round = 'river'
show_hand_round = 'show_hand'
round_steps = [pre_flop_round, flop_round, turn_round, river_round, show_hand_round]


def check_cards(npc: Dict = None):
    if 'round' not in st.session_state:
        st.session_state.round = pre_flop_round
    if st.session_state.round == pre_flop_round or len(st.session_state.community_cards) == 0:
        st.session_state.card_deck.shuffle()  # 洗牌
        st.session_state.community_cards = st.session_state.card_deck.draw_cards(5)

    if npc is not None and npc['name'] not in st.session_state.hand_cards:
        cards = st.session_state.card_deck.draw_cards(2)
        st.session_state.hand_cards[npc['name']] = cards


def show_community_cards(layout: DeltaGenerator):
    cols = layout.columns(5)
    check_cards()
    round_index = round_steps.index(st.session_state.round)
    for i, col in enumerate(cols):
        card = st.session_state.community_cards[i]
        if (i < 3 and round_index > 0  # flop
                or i == 3 and round_index > 1  # turn
                or i == 4 and round_index > 2):  # river or show_hands
            col.image(card.image_path)
        else:
            col.image(card.BACK_IMAGE_PATH)


def show_hand_cards(layout: list[DeltaGenerator], npc):
    check_cards(npc)
    if st.session_state.round == show_hand_round:
        layout[0].image(st.session_state.hand_cards[npc['name']][0].image_path)  # NPC手牌图片
        layout[1].image(st.session_state.hand_cards[npc['name']][1].image_path)  # NPC手牌图片
    else:
        layout[0].image(Card.BACK_IMAGE_PATH)  # NPC手牌图片
        layout[1].image(Card.BACK_IMAGE_PATH)  # NPC手牌图片


def show_game_round_step(layout: DeltaGenerator):
    if 'round' not in st.session_state:
        st.session_state.round = pre_flop_round
    layout.radio("当前的游戏阶段："
             , index=round_steps.index(st.session_state.round)
             , horizontal=True
             , disabled=True
             , options=round_steps)


def npc_act(npc: Dict, layout: DeltaGenerator):
    layout = layout.empty()
    # 自定义修改
    rd = random.randint(0, 1)
    npc['bet_component'] = layout
    if rd == 1:
        layout.metric(label="押注积分", value=f'25', delta='5')
    else:
        layout.metric(label="弃牌", value=f'X', delta='-20')   ##此时失去所有押注金额


def player_act(layout: DeltaGenerator):
    bet = layout.container()
    bet.metric(label="押注积分", value=f'25', delta='')
    principal = layout.container()
    principal.metric(label="剩余积分", value=f'25', delta='')


def show_button(layout: DeltaGenerator):
    disabled = st.session_state.who_speak['name'] is not 'YOU'
    if disabled:
        label = '未轮到你'
    else:
        label = '确认选择'
    if layout.button(key="player_action", label=label, disabled=disabled):
        st.rerun()

