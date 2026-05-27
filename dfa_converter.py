from automato import DFA
from nfa_generator import epsilon_closure 

def nfa_to_dfa(nfa, regex_spec):
    """
    Converte um NFA em um DFA usando o algoritmo de Construção de Subconjuntos.
    """
    dfa = DFA(start_state=0)
    priority_map = {token_name: i for i, (token_name, _) in enumerate(regex_spec)}
    
    start_closure = frozenset(epsilon_closure(nfa, {nfa.start_state}))
    dfa_states_map = {start_closure: 0}
    unmarked_states = [start_closure]
    state_counter = 1
    
    alphabet = set()
    for from_state, trans in nfa.transitions.items():
        for symbol in trans.keys():
            if symbol != '':
                alphabet.add(symbol)
                
    while unmarked_states:
        current_nfa_states = unmarked_states.pop(0)
        current_dfa_state_id = dfa_states_map[current_nfa_states]
        
        accepted_tokens = []
        for nfa_state in current_nfa_states:
            if nfa_state in nfa.accept_states:
                accepted_tokens.append(nfa.accept_states[nfa_state])
        
        if accepted_tokens:
            accepted_tokens.sort(key=lambda t: priority_map.get(t, float('inf')))
            dfa.set_accept(current_dfa_state_id, accepted_tokens[0])
            
        for symbol in alphabet:
            reachable = set()
            for nfa_state in current_nfa_states:
                if nfa_state in nfa.transitions and symbol in nfa.transitions[nfa_state]:
                    reachable.update(nfa.transitions[nfa_state][symbol])
            
            if not reachable:
                continue 
                
            next_nfa_states = frozenset(epsilon_closure(nfa, reachable))
            
            if next_nfa_states not in dfa_states_map:
                dfa_states_map[next_nfa_states] = state_counter
                unmarked_states.append(next_nfa_states)
                state_counter += 1
            
            next_dfa_state_id = dfa_states_map[next_nfa_states]
            dfa.add_transition(current_dfa_state_id, symbol, next_dfa_state_id)
            
    return dfa