from collections import defaultdict

class NFA:
    def __init__(self, start_state=0):
        self.start_state = start_state
        # defaultdict: serve para NÃO precisar fzr os ifs para checar se o estado ou o símbolo já existem no dicionário
        self.transitions = defaultdict(lambda: defaultdict(list))  # { estado_origem: { 'simbolo': [estados_destino] } }
        self.accept_states = {}

    def add_transition(self, from_state, symbol, to_state):
        # if from_state not in self.transitions:
        #     self.transitions[from_state] = {}
        # if symbol not in self.transitions[from_state]:
        #     self.transitions[from_state][symbol] = []
        
        if to_state not in self.transitions[from_state][symbol]:
            self.transitions[from_state][symbol].append(to_state)

    def set_accept(self, state, token_type):
        self.accept_states[state] = token_type

class DFA:
    def __init__(self, start_state=0):
        self.start_state = start_state
        self.transitions = defaultdict(dict)
        self.accept_states = {}

    def add_transition(self, from_state, symbol, to_state):
        # if from_state not in self.transitions:
        #     self.transitions[from_state] = {}
        self.transitions[from_state][symbol] = to_state

    def set_accept(self, state, token_type):
        self.accept_states[state] = token_type

