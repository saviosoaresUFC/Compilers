from config import REGEX_SPEC
from nfa_generator import build_global_nfa
from nfa_generator import epsilon_closure


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