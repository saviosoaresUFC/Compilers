from automato import NFA
from config import REGEX_SPEC, STRING_ALPHABET


def build_nfa_for_literal(token_name, text, start_counter):
    """ Cria um NFA simples e sequencial para palavras reservadas e operadores """
    nfa = NFA(start_state=start_counter)
    current = start_counter
    
    for char in text:
        nfa.add_transition(current, char, current + 1)
        current += 1
        
    nfa.set_accept(current, token_name)
    return nfa, current + 1


def _add_literal_token(global_nfa, token_name, pattern, state_counter):
    """Processa um token literal (palavra reservada ou operador)"""
    sub_nfa, next_counter = build_nfa_for_literal(token_name, pattern, state_counter)
    
    global_nfa.add_transition(global_nfa.start_state, '', sub_nfa.start_state)
    
    for src_state, trans in sub_nfa.transitions.items():
        for sym, destinations in trans.items():
            for dest in destinations:
                global_nfa.add_transition(src_state, sym, dest)
    
    global_nfa.accept_states.update(sub_nfa.accept_states)
    return next_counter


def _add_int_token(global_nfa, state_counter, digitos):
    """Processa um token de literal numérico inteiro"""
    start_int = state_counter
    accept_int = state_counter + 1
    
    for char in digitos:
        global_nfa.add_transition(start_int, char, accept_int)
        global_nfa.add_transition(accept_int, char, accept_int)
        
    global_nfa.add_transition(global_nfa.start_state, '', start_int)
    global_nfa.set_accept(accept_int, "INT_LITERAL")
    return state_counter + 2


def _add_id_token(global_nfa, state_counter, letras, digitos):
    """Processa um token de identificador (ID) com limite máximo de 30 caracteres"""
    start_id = state_counter
    max_id_length = 30
    id_chars = letras + digitos + "_"
    
    global_nfa.add_transition(global_nfa.start_state, '', start_id)
    previous_state = start_id
    
    for position in range(1, max_id_length + 1):
        current_state = state_counter + position
        allowed_chars = letras + "_" if position == 1 else id_chars
        
        for char in allowed_chars:
            global_nfa.add_transition(previous_state, char, current_state)
            
        global_nfa.set_accept(current_state, "ID")
        previous_state = current_state
        
    return state_counter + max_id_length + 1


def _add_string_token(global_nfa, state_counter, todos_caracteres_string):
    """Processa um token de string"""
    start_str = state_counter
    body_str = state_counter + 1
    accept_str = state_counter + 2
    
    global_nfa.add_transition(start_str, '"', body_str)
    
    for char in todos_caracteres_string:
        global_nfa.add_transition(body_str, char, body_str)
        
    global_nfa.add_transition(body_str, '"', accept_str)
    
    global_nfa.add_transition(global_nfa.start_state, '', start_str)
    global_nfa.set_accept(accept_str, "STRING")
    return state_counter + 3


def build_global_nfa(spec):
    global_nfa = NFA(start_state=0)
    state_counter = 1
    
    letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digitos = "0123456789"
    
    for token_name, pattern in spec:
        if token_name == "ID":
            state_counter = _add_id_token(global_nfa, state_counter, letras, digitos)
        elif token_name == "STRING":
            state_counter = _add_string_token(global_nfa, state_counter, STRING_ALPHABET)
        elif token_name == "INT_LITERAL":
            state_counter = _add_int_token(global_nfa, state_counter, digitos)
        else:
            state_counter = _add_literal_token(global_nfa, token_name, pattern, state_counter)
            
    return global_nfa

def epsilon_closure(nfa, states):
    """Retorna todos os estados alcançáveis a partir dos 'states' usando apenas transições vazias ('')"""
    closure = set(states)
    stack = list(closure)
    
    while stack:
        current = stack.pop()
        if current in nfa.transitions and '' in nfa.transitions[current]:
            for next_state in nfa.transitions[current]['']:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return closure


def simulate_nfa(nfa, input_string):
    """Simula a execução do NFA para uma string de entrada completa"""
    current_states = epsilon_closure(nfa, {nfa.start_state})
    
    for char in input_string:
        next_states = set()
        for state in current_states:
            if state in nfa.transitions and char in nfa.transitions[state]:
                next_states.update(nfa.transitions[state][char])
        
        current_states = epsilon_closure(nfa, next_states)
        
        if not current_states:
            return None
            
    priority_map = {token_name: i for i, (token_name, _) in enumerate(REGEX_SPEC)}
    
    accepted_tokens = []
    for state in current_states:
        if state in nfa.accept_states:
            accepted_tokens.append(nfa.accept_states[state])
            
    if accepted_tokens:
        accepted_tokens.sort(key=lambda t: priority_map.get(t, float('inf')))
        return accepted_tokens[0]  # retorna o nome do token com maior prioridade
            
    return None


if __name__ == "__main__":
    nfa_completo = build_global_nfa(REGEX_SPEC)
    print("NFA Global criado com sucesso!")
    print("-" * 40)
    
    testes = [
        "num", "show", "==", "=", "+", "bool", ";",
        "idade", "_nome", "valor1",
        '"Lucas"', '"Ola mundo!"',
        "if", "while", "1valor", "25", "0", "SavioDeCarvalhoSoaresTestandoMaisDe30Caracteres"
    ]
    
    print("Resultado dos Testes Unitarios no NFA:")
    for palavra in testes:
        resultado = simulate_nfa(nfa_completo, palavra)
        if resultado:
            print(f"  > {palavra} -> Casou com o Token: {resultado}")
        else:
            print(f"  > {palavra} -> Nao reconhecido (Retornou REJEITA/ERRO)")
