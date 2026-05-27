import sys
from config import REGEX_SPEC
from nfa_generator import build_global_nfa
from dfa_converter import nfa_to_dfa
from lexical import analyze

if __name__ == "__main__":
    print("==================================================")
    print(" TESTE DA QUESTÃO 4: ANALISADOR LÉXICO – LangC")
    print("==================================================\n")

    nfa_base = build_global_nfa(REGEX_SPEC)
    dfa = nfa_to_dfa(nfa_base, REGEX_SPEC)
    print(f"-> DFA carregado com {len(dfa.transitions)} estados.\n")

    # ------------------------------------------------------------------
    # Teste 1: Exemplo direto do enunciado
    # ------------------------------------------------------------------
    print("Teste 1 – Exemplo do enunciado:")
    print("-" * 50)
    source_code_1 = (
        'num a = 0 ;\n'
        'num b = 5 + a ;\n'
        'text c = "teSte" ;\n'
    )
    print(source_code_1.rstrip())
    print("\nSaída:")
    print(analyze(source_code_1, dfa))
    print("-" * 50)

    