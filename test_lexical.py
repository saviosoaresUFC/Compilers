from config import REGEX_SPEC
from nfa_generator import build_global_nfa
from dfa_converter import nfa_to_dfa
from lexical import analyze


# ---------------------------------------------------------------------------
# Inicialização do analisador
# ---------------------------------------------------------------------------

# O DFA é montado apenas uma vez e reutilizado em todos os testes
global_nfa = build_global_nfa(REGEX_SPEC)
global_dfa = nfa_to_dfa(global_nfa, REGEX_SPEC)


def run_analysis(source_code):
    return analyze(source_code, global_dfa)


# ---------------------------------------------------------------------------
# Casos de teste
# ---------------------------------------------------------------------------

def test_exemplo_enunciado():
    codigo = (
        'num a = 0 ;\n'
        'num b = 5 + a ;\n'
        'text c = "teSte" ;\n'
    )

    esperado = (
        'NUM VAR EQ NUM SEMICOLON\n'
        'NUM VAR EQ NUM ADD VAR SEMICOLON\n'
        'TEXT VAR EQ CONST SEMICOLON'
    )

    resultado = run_analysis(codigo)

    assert resultado == esperado


def test_programa_completo():
    codigo = (
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

    esperado = (
        'SHOW NUM GT NUM SEMICOLON\n'
        'NUM VAR EQ NUM SEMICOLON\n'
        'NUM VAR EQ NUM SEMICOLON\n'
        'NUM VAR EQ VAR ADD VAR SEMICOLON\n'
        'TEXT VAR EQ CONST SEMICOLON\n'
        'SHOW VAR SEMICOLON\n'
        'SHOW VAR SEMICOLON\n'
        'SHOW VAR SEMICOLON\n'
        'SHOW VAR LT VAR SEMICOLON\n'
        'SHOW VAR EQ NUM SEMICOLON'
    )

    resultado = run_analysis(codigo)

    assert resultado == esperado


def test_booleanos_e_reservadas():
    codigo = (
        'bool flag = true ;\n'
        'bool outro = false ;\n'
        'show flag ;\n'
    )

    esperado = (
        'BOOL VAR EQ TRUE SEMICOLON\n'
        'BOOL VAR EQ FALSE SEMICOLON\n'
        'SHOW VAR SEMICOLON'
    )

    resultado = run_analysis(codigo)

    assert resultado == esperado


def test_caractere_invalido():
    codigo = (
        'num x = 5 ;\n'
        'num y = @invalido ;\n'
        'show x ;\n'
    )

    resultado = run_analysis(codigo)

    assert resultado == 'ERRO'


def test_identificador_maior_que_limite():
    codigo = 'num VariavelComMaisDeTrintaCaracteresAqui = 1 ;\n'

    resultado = run_analysis(codigo)

    assert resultado == 'ERRO'


def test_linhas_vazias():
    codigo = (
        'num a = 1 ;\n'
        '\n'
        '   \n'
        'show a ;\n'
    )

    esperado = (
        'NUM VAR EQ NUM SEMICOLON\n'
        'SHOW VAR SEMICOLON'
    )

    resultado = run_analysis(codigo)

    assert resultado == esperado


def test_operador_duplo_igual():
    codigo = 'show a == 5 ;\n'

    resultado = run_analysis(codigo)

    assert resultado == 'SHOW VAR EQ NUM SEMICOLON'


def test_operador_igual():
    codigo = 'show a = 5 ;\n'

    resultado = run_analysis(codigo)

    assert resultado == 'SHOW VAR EQ NUM SEMICOLON'


# ---------------------------------------------------------------------------
# Execução manual
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 50)
    print("TESTES DO ANALISADOR LEXICO - LangC")
    print("=" * 50)

    print(f"\nDFA inicializado com {len(global_dfa.transitions)} estados.\n")

    casos_teste = [
        (
            "Teste 1 - Exemplo basico",
            'num a = 0 ;\nnum b = 5 + a ;\ntext c = "teSte" ;\n'
        ),

        (
            "Teste 2 - Programa completo",
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
        ),

        (
            "Teste 3 - Booleanos",
            'bool flag = true ;\n'
            'bool outro = false ;\n'
            'show flag ;\n'
        ),

        (
            "Teste 4 - Erro lexico",
            'num x = 5 ;\n'
            'num y = @invalido ;\n'
            'show x ;\n'
        ),

        (
            "Teste 5 - Identificador muito grande",
            'num VariavelComMaisDeTrintaCaracteresAqui = 1 ;\n'
        ),

        (
            "Teste 6 - Linhas vazias",
            'num a = 1 ;\n\n   \nshow a ;\n'
        ),

        (
            "Teste 7 - == e =",
            'show a == 5 ;\nshow a = 5 ;\n'
        )
    ]

    for titulo, codigo in casos_teste:

        print(f"\n{titulo}")
        print("-" * 50)

        print("Codigo de entrada:\n")
        print(codigo.rstrip())

        print("\nSaida gerada:\n")

        resultado = run_analysis(codigo)

        print(resultado)
        print("-" * 50)

    # -----------------------------------------------------------------------
    # Verificação automática
    # -----------------------------------------------------------------------

    testes = [
        test_exemplo_enunciado,
        test_programa_completo,
        test_booleanos_e_reservadas,
        test_caractere_invalido,
        test_identificador_maior_que_limite,
        test_linhas_vazias,
        test_operador_duplo_igual,
        test_operador_igual,
    ]

    print("\nExecutando assertions...\n")

    todos_ok = True

    for teste in testes:

        try:
            teste()
            print(f"[OK] {teste.__name__}")

        except AssertionError:
            print(f"[FALHA] {teste.__name__}")
            todos_ok = False

    print("\n" + "=" * 50)

    if todos_ok:
        print("Todos os testes passaram.")
    else:
        print("Alguns testes falharam.")

    print("=" * 50)