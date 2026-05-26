from automato import NFA
from config import REGEX_SPEC

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

def _add_id_token(global_nfa, state_counter, letras, digitos):
    """Processa um token de identificador (ID)"""
    start_id = state_counter
    accept_id = state_counter + 1
    
    for char in letras + "_":
        global_nfa.add_transition(start_id, char, accept_id)
        
    for char in letras + digitos + "_":
        global_nfa.add_transition(accept_id, char, accept_id)
        
    global_nfa.add_transition(global_nfa.start_state, '', start_id)
    global_nfa.accept_states[accept_id] = "ID"
    return state_counter + 2

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
    global_nfa.accept_states[accept_str] = "STRING"
    return state_counter + 3

def build_global_nfa(spec):
    global_nfa = NFA(start_state=0)
    state_counter = 1
    
    letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digitos = "0123456789"
    todos_caracteres_string = letras + digitos + " +-*/=><();_!@#$%&?| \t" # Alfabeto completo da LangC menos as aspas
    
    for token_name, pattern in spec:
        if token_name == "ID":
            state_counter = _add_id_token(global_nfa, state_counter, letras, digitos)
        elif token_name == "STRING":
            state_counter = _add_string_token(global_nfa, state_counter, todos_caracteres_string)
        else:
            state_counter = _add_literal_token(global_nfa, token_name, pattern, state_counter)
            
    return global_nfa

def epsilon_closure(nfa, states):
    """Retorna todos os estados alcançáveis a partir dos 'states' usando apenas transições vazias ('')"""
    closure = list(states)
    stack = list(states)
    
    while stack:
        current = stack.pop()
        if current in nfa.transitions and '' in nfa.transitions[current]:
            for next_state in nfa.transitions[current]['']:
                if next_state not in closure:
                    closure.append(next_state)
                    stack.append(next_state)
    return closure

def simulate_nfa(nfa, input_string):
    """Simula a execução do NFA para uma string de entrada completa"""
    current_states = epsilon_closure(nfa, [nfa.start_state])
    
    for char in input_string:
        next_states = []
        for state in current_states:
            if state in nfa.transitions and char in nfa.transitions[state]:
                next_states.extend(nfa.transitions[state][char])
        
        current_states = epsilon_closure(nfa, next_states)
        
        if not current_states:
            return None
            
    for state in current_states:
        if state in nfa.accept_states:
            return nfa.accept_states[state] # retorna o nome do token por ex. "SHOW"
            
    return None

if __name__ == "__main__":
    nfa_completo = build_global_nfa(REGEX_SPEC)
    print("NFA Global criado com sucesso!")
    print("-" * 40)
    
    testes = [
        "num", "show", "==", "=", "+", "bool", ";", 
        "idade", "_nome", "valor1", 
        '"Lucas"', '"Ola mundo!"',
        "if", "while", "1valor"
    ]
    
    print("Resultado dos Testes Unitarios no NFA:")
    for palavra in testes:
        resultado = simulate_nfa(nfa_completo, palavra)
        if resultado:
            print(f"  > {palavra} -> Casou com o Token: {resultado}")
        else:
            print(f"  > {palavra} -> Nao reconhecido (Retornou REJEITA/ERRO)")
