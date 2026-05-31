from config import REGEX_SPEC
from nfa_generator import build_global_nfa
from dfa_converter import nfa_to_dfa

def simulate_dfa(dfa, input_string):
    """Simula a execução de um DFA caractere por caractere (Questão 3)."""
    current_state = dfa.start_state
    
    for char in input_string:
        if current_state in dfa.transitions and char in dfa.transitions[current_state]:
            current_state = dfa.transitions[current_state][char]
        else:
            return None
            
    if current_state in dfa.accept_states:
        return dfa.accept_states[current_state]
    return None

if __name__ == "__main__":
    print("==================================================")
    print(" TESTE DA QUESTÃO 3: CONVERSÃO E EXECUÇÃO DO DFA")
    print("==================================================\n")

    nfa_base = build_global_nfa(REGEX_SPEC)
    meu_dfa = nfa_to_dfa(nfa_base, REGEX_SPEC)
    
    print(f"-> DFA criado com sucesso! O autômato gerado possui {len(meu_dfa.transitions)} estados.\n")

    testes = [
        "num", "show", "==", "=", "+", "bool", ";",
        "idade", "_nome", "valor1",
        '"Lucas"', '"Ola mundo!"',
        "if", "while", "1valor", "25", "0", "VariavelComMaisDe30CaracteresAa"
    ]

    print("Resultados da Leitura pelo DFA:")
    print("-" * 50)
    
    for palavra in testes:
        resultado = simulate_dfa(meu_dfa, palavra)
        if resultado:
            print(f" > '{palavra:<20}' -> Token: {resultado}")
        else:
            print(f" > '{palavra:<20}' -> ERRO (Rejeitado)")
            
    print("-" * 50)