''' Limit Hold 'em rule model
'''
import rlcard
from rlcard.models.model import Model


class LimitholdemRuleAgentV1(object):
    ''' Limit Hold 'em Rule agent version 1
    '''

    def __init__(self):
        self.use_raw = True

    @staticmethod
    def step(state):
        ''' Predict the action when given raw state. A simple rule-based AI.
        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        '''
        legal_actions = state['raw_legal_actions']
        state = state['raw_obs']
        hand = state['hand']
        public_cards = state['public_cards']
        action = 'fold'
        print(f"state['public_cards']={state['public_cards']}")
        # When having only 2 hand cards at the game start, choose fold to drop terrible cards:
        # Acceptable hand cards:
        # Pairs
        # AK, AQ, AJ, AT
        # A9s, A8s, ... A2s(s means flush)
        # KQ, KJ, QJ, JT
        # Fold all hand types except those mentioned above to save money
        if len(public_cards) == 0:
            print("test!!!!!")
            print(f"hand[0][1]={hand[0][1]}    hand[1][1]={hand[1][1]}")
            if hand[0][1] == hand[1][1]:
                action = 'raise'
            elif hand[0][1] == 'A' or hand[1][1] == 'A':
                if 'K' in [hand[0][1], hand[1][1]] or 'Q' in [hand[0][1], hand[1][1]] or 'J' in [hand[0][1],hand[1][1]] or 'T' in [hand[0][1], hand[1][1]]:
                    action = 'raise'
                elif hand[0][0] == hand[1][0]:
                    action = 'raise'
            elif hand[0][1] == 'K' or hand[0][1] == 'Q' or hand[0][1] == 'J' or hand[0][1] == 'T':
                if hand[1][1] == 'K' or hand[1][1] == 'Q' or hand[1][1] == 'J' or hand[1][1] == 'T':
                    action = 'raise'
                else:
                    action = 'call'
        if len(public_cards) == 3:
            public_cards_ranks = ['A', 'A', 'A']
            public_cards_flush = ['S', 'S', 'S']
            for i, _ in enumerate(public_cards):
                public_cards_ranks[i] = public_cards[i][1]
                public_cards_flush[i] = public_cards[i][0]
            if hand[0][1] == hand[1][1]:
                # if the player already have a pair, raise when public cards have card same as the pair
                if hand[0][1] in public_cards_ranks:
                    action = 'raise'
            elif hand[0][1] == 'A' or hand[1][1] == 'A':
                if 'K' in [hand[0][1], hand[1][1]] or 'Q' in [hand[0][1], hand[1][1]] or 'J' in [hand[0][1],
                                                                                                 hand[1][1]] or 'T' in [
                    hand[0][1], hand[1][1]]:
                    # For AK, AQ, AJ, AT types, if public cards have A, K, Q, J, T, raise, because the chance of getting a straight greatly increases
                    if 'A' in public_cards_ranks or 'K' in public_cards_ranks or 'Q' in public_cards_ranks or 'J' in public_cards_ranks or 'T' in public_cards_ranks:
                        action = 'raise'
                # For A9s, A8s, ... A2s types, if public cards have same flush as the hand cards, raise, because the chance of getting a flush greatly increases
                elif hand[0][0] == hand[1][0]:
                    if hand[0][0] in public_cards_flush:
                        action = 'raise'
            elif max(public_cards_ranks) in ['5', '4', '3',
                                             '2']:  # for KQ, KJ, QJ, JT, check when having no cards higher than 5
                action = 'check'
            else:
                action = 'call'

        if len(public_cards) == 5 or len(public_cards) == 4:
            public_cards_ranks = []
            public_cards_flush = []
            for i, _ in enumerate(public_cards):
                public_cards_ranks.append('A')
                public_cards_flush.append('S')
                public_cards_ranks[i] = public_cards[i][1]
                public_cards_flush[i] = public_cards[i][0]
            if hand[0][1] == hand[1][1]:
                # if the player already have a pair, raise when public cards have card same as the pair
                if hand[0][1] in public_cards_ranks:
                    action = 'raise'
            elif hand[0][1] == 'A' or hand[1][1] == 'A':
                if 'K' in [hand[0][1], hand[1][1]] or 'Q' in [hand[0][1], hand[1][1]] or 'J' in [hand[0][1],
                                                                                                 hand[1][1]] or 'T' in [
                    hand[0][1], hand[1][1]]:
                    # For AK, AQ, AJ, AT types, if public cards have A, K, Q, J, T, raise, because the chance of getting a straight greatly increases
                    if 'A' in public_cards_ranks or 'K' in public_cards_ranks or 'Q' in public_cards_ranks or 'J' in public_cards_ranks or 'T' in public_cards_ranks:
                        action = 'raise'
                    # For A9s, A8s, ... A2s types, if public cards have same flush as the hand cards, raise, because the chance of getting a flush greatly increases
                elif hand[0][0] == hand[1][0]:
                    if hand[0][0] in public_cards_flush:
                        action = 'raise'
            elif max(public_cards_ranks) in ['5', '4', '3',
                                             '2']:  # for KQ, KJ, QJ, JT, fold when having no cards higher than 5
                action = 'fold'
            else:
                action = 'call'

        # return action
        if action in legal_actions:
            return action
        else:
            if action == 'raise':
                if 'call' in legal_actions:
                    return 'call'
                elif 'check' in legal_actions:
                    return 'check'
                else:
                    return 'fold'
            if action == 'check':
                return 'fold'
            if action == 'call':
                if 'check' in legal_actions:
                    return 'check'
                elif 'raise' in legal_actions:
                    return 'raise'
                else:
                    return 'fold'
            else:
                return action

    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(state), []

class LimitholdemRuleAgentV2(object):
    ''' Limit Hold 'em Rule agent version 1
    '''

    def __init__(self):
        self.use_raw = True

    @staticmethod
    def step(state):
        ''' Predict the action when given raw state. A simple rule-based AI.
        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        '''
        legal_actions = state['raw_legal_actions']
        state = state['raw_obs']
        hand = state['hand']
        public_cards = state['public_cards']
        action = 'fold'
        # When having only 2 hand cards at the game start, choose fold to drop terrible cards:
        # Acceptable hand cards:
        # Pairs
        # AK, AQ, AJ, AT
        # A9s, A8s, ... A2s(s means flush)
        # KQ, KJ, QJ, JT
        # Fold all hand types except those mentioned above to save money
        if len(public_cards) == 0:
            if hand[0][1] == hand[1][1]:
                action = 'raise'
            elif hand[0][1] == 'A' or hand[1][1] == 'A':
                if 'K' in [hand[0][1], hand[1][1]] or 'Q' in [hand[0][1], hand[1][1]] or 'J' in [hand[0][1],
                                                                                                 hand[1][
                                                                                                     1]] or 'T' in [
                    hand[0][1], hand[1][1]]:
                    action = 'raise'
                elif hand[0][0] == hand[1][0]:
                    action = 'raise'
            elif hand[0][1] == 'K' or hand[0][1] == 'Q' or hand[0][1] == 'J' or hand[0][1] == 'T':
                if hand[1][1] == 'K' or hand[1][1] == 'Q' or hand[1][1] == 'J' or hand[1][1] == 'T':
                    action = 'raise'
        if len(public_cards) == 3:
            public_cards_ranks = ['A', 'A', 'A']
            public_cards_flush = ['S', 'S', 'S']
            for i, _ in enumerate(public_cards):
                public_cards_ranks[i] = public_cards[i][1]
                public_cards_flush[i] = public_cards[i][0]
            if hand[0][1] == hand[1][1]:
                # if the player already have a pair, raise when public cards have card same as the pair
                if hand[0][1] in public_cards_ranks:
                    action = 'raise'
            elif hand[0][1] == 'A' or hand[1][1] == 'A':
                if 'K' in [hand[0][1], hand[1][1]] or 'Q' in [hand[0][1], hand[1][1]] or 'J' in [hand[0][1],
                                                                                                 hand[1][
                                                                                                     1]] or 'T' in [
                    hand[0][1], hand[1][1]]:
                    # For AK, AQ, AJ, AT types, if public cards have A, K, Q, J, T, raise, because the chance of getting a straight greatly increases
                    if 'A' in public_cards_ranks or 'K' in public_cards_ranks or 'Q' in public_cards_ranks or 'J' in public_cards_ranks or 'T' in public_cards_ranks:
                        action = 'raise'
                # For A9s, A8s, ... A2s types, if public cards have same flush as the hand cards, raise, because the chance of getting a flush greatly increases
                elif hand[0][0] == hand[1][0]:
                    if hand[0][0] in public_cards_flush:
                        action = 'raise'
            elif max(public_cards_ranks) in ['5', '4', '3',
                                             '2']:  # for KQ, KJ, QJ, JT, check when having no cards higher than 5
                action = 'check'
            else:
                action = 'call'

        if len(public_cards) == 5 or len(public_cards) == 4:
            public_cards_ranks = []
            public_cards_flush = []
            for i, _ in enumerate(public_cards):
                public_cards_ranks.append('A')
                public_cards_flush.append('S')
                public_cards_ranks[i] = public_cards[i][1]
                public_cards_flush[i] = public_cards[i][0]
            if hand[0][1] == hand[1][1]:
                # if the player already have a pair, raise when public cards have card same as the pair
                if hand[0][1] in public_cards_ranks:
                    action = 'raise'
            elif hand[0][1] == 'A' or hand[1][1] == 'A':
                if 'K' in [hand[0][1], hand[1][1]] or 'Q' in [hand[0][1], hand[1][1]] or 'J' in [hand[0][1],
                                                                                                 hand[1][
                                                                                                     1]] or 'T' in [
                    hand[0][1], hand[1][1]]:
                    # For AK, AQ, AJ, AT types, if public cards have A, K, Q, J, T, raise, because the chance of getting a straight greatly increases
                    if 'A' in public_cards_ranks or 'K' in public_cards_ranks or 'Q' in public_cards_ranks or 'J' in public_cards_ranks or 'T' in public_cards_ranks:
                        action = 'raise'
                    # For A9s, A8s, ... A2s types, if public cards have same flush as the hand cards, raise, because the chance of getting a flush greatly increases
                elif hand[0][0] == hand[1][0]:
                    if hand[0][0] in public_cards_flush:
                        action = 'raise'
            elif max(public_cards_ranks) in ['5', '4', '3',
                                             '2']:  # for KQ, KJ, QJ, JT, fold when having no cards higher than 5
                action = 'fold'
            else:
                action = 'call'

        # return action
        if action in legal_actions:
            return action
        else:
            if action == 'raise':
                if 'call' in legal_actions:
                    return 'call'
                elif 'check' in legal_actions:
                    return 'check'
                else:
                    return 'fold'
            if action == 'check':
                return 'fold'
            if action == 'call':
                if 'check' in legal_actions:
                    return 'check'
                elif 'raise' in legal_actions:
                    return 'raise'
                else:
                    return 'fold'
            else:
                return action

    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(state), []


class LimitholdemRuleModelV1(Model):
    ''' Limitholdem Rule Model version 1
    '''

    def __init__(self):
        ''' Load pretrained model
        '''
        env = rlcard.make('limit-holdem')

        rule_agent = LimitholdemRuleAgentV1()
        self.rule_agents = [rule_agent for _ in range(env.num_players)]

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.rule_agents

    @property
    def use_raw(self):
        ''' Indicate whether use raw state and action

        Returns:
            use_raw (boolean): True if using raw state and action
        '''
        return True


import numpy as np


class RandomAgent(object):
    ''' A random agent. Random agents is for running toy examples on the card games
    '''

    def __init__(self, num_actions):
        ''' Initilize the random agent

        Args:
            num_actions (int): The size of the ouput action space
        '''
        self.use_raw = True
        self.num_actions = num_actions

    @staticmethod
    def step(state):
        ''' Predict the action given the curent state in gerenerating training data.

        Args:
            state (dict): An dictionary that represents the current state

        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
        '''
        return np.random.choice(state['raw_legal_actions'])

    def eval_step(self, state):
        ''' Predict the action given the current state for evaluation.
            Since the random agents are not trained. This function is equivalent to step function

        Args:
            state (dict): An dictionary that represents the current state

        Returns:
            action (int): The action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        '''
        probs = [0 for _ in range(self.num_actions)]
        for i in state['legal_actions']:
            probs[i] = 1 / len(state['legal_actions'])

        info = {}
        info['probs'] = {state['raw_legal_actions'][i]: probs[list(state['legal_actions'].keys())[i]] for i in
                         range(len(state['legal_actions']))}

        return self.step(state), info
