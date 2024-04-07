import random
from typing import Dict

import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from utils2 import Card, CardDeck

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
    # check_cards()
    # round_index = round_steps.index(st.session_state.round)
    cards = st.session_state.community_cards
    for i, col in enumerate(cols):
        if i < len(cards):
            col.image(cards[i].image_path)
        else:
            col.image(Card.BACK_IMAGE_PATH)


def show_back_cards(layout: list[DeltaGenerator]):
    # check_cards(npc)
    # if st.session_state.round == show_hand_round:
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


def npc_act(npc: Dict, layout: DeltaGenerator, rd, point):
    layout = layout.empty()
    # 自定义修改
    npc['bet_component'] = layout
    if rd == 'raise':
        layout.metric(label="押注积分", value=f'{point}', delta='5')
    elif rd == 'check':
        layout.metric(label="过牌", value=f'{point}', delta='0')
    elif rd == 'call':
        layout.metric(label="跟注", value=f'{point}', delta='0')
    else:
        layout.metric(label="弃牌", value=f'X', delta=f'-{point}')   ##此时失去所有押注金额


def player_act(layout: DeltaGenerator, point, all_point):
    bet = layout.container()
    bet.metric(label="押注积分", value=f'{point}', delta='')
    principal = layout.container()
    principal.metric(label="剩余积分", value=f'{all_point-point}', delta='')


def show_button(layout: DeltaGenerator, player_id):
    disabled = player_id != 0
    if layout.button(key="call", label='跟注', disabled=disabled):
        st.session_state['continue'] = False
        st.session_state.action = 'call'
        st.rerun()
    if layout.button(key="raise", label='加注', disabled=disabled):
        st.session_state['continue'] = False
        st.session_state.action = 'raise'
        st.rerun()
    if layout.button(key="fold", label='弃牌', disabled=disabled):
        st.session_state['continue'] = False
        st.session_state.action = 'fold'
        st.rerun()

