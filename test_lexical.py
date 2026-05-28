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

    # ------------------------------------------------------------------
    # Teste 2: Programa completo da especificação
    # ------------------------------------------------------------------
    print("\nTeste 2 – Programa completo da especificação:")
    print("-" * 50)
    source_code_2 = (
        'show 2 > 2 ;\n'
        'num a = 5 ;\n'
        'num b = 10 ;\n'
        'num soma = a + b ;\n'
        'text mensagem = "Oi!" ;\n'
        'show mensagem ;\n'
        'show a ;\n'
        'show soma ;\n'
        'show a < b ;\n'
        'show a == 5 ;\n'
    )
    print(source_code_2.rstrip())
    print("\nSaída:")
    print(analyze(source_code_2, dfa))
    print("-" * 50)

    # ------------------------------------------------------------------
    # Teste 3: Palavras reservadas e booleanos
    # ------------------------------------------------------------------
    print("\nTeste 3 – Palavras reservadas e booleanos:")
    print("-" * 50)
    source_code_3 = (
        'bool flag = true ;\n'
        'bool outro = false ;\n'
        'show flag ;\n'
    )
    print(source_code_3.rstrip())
    print("\nSaída:")
    print(analyze(source_code_3, dfa))
    print("-" * 50)

    # ------------------------------------------------------------------
    # Teste 4: Erro léxico
    # ------------------------------------------------------------------
    print("\nTeste 4 – Erro léxico:")
    print("-" * 50)
    source_code_4 = (
        'num x = 5 ;\n'
        'num y = @invalido ;\n'
        'show x ;\n'
    )
    print(source_code_4.rstrip())
    print("\nSaída:")
    print(analyze(source_code_4, dfa))
    print("-" * 50)

    # ------------------------------------------------------------------
    # Teste 5: Identificador com mais de 30 caracteres (erro léxico)
    # ------------------------------------------------------------------
    print("\nTeste 5 – Identificador com mais de 30 caracteres:")
    print("-" * 50)
    source_code_5 = 'num VariavelComMaisDeTrintaCaracteresAqui = 1 ;\n'
    print(source_code_5.rstrip())
    print("\nSaída:")
    print(analyze(source_code_5, dfa))
    print("-" * 50)