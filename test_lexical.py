from config import REGEX_SPEC
from nfa_generator import build_global_nfa
from dfa_converter import nfa_to_dfa
from lexical import analyze

# DFA construído uma única vez e reutilizado em todos os testes
_nfa = build_global_nfa(REGEX_SPEC)
_dfa = nfa_to_dfa(_nfa, REGEX_SPEC)


def _run(source):
    return analyze(source, _dfa)


# ---------------------------------------------------------------------------
# Testes com assertions
# ---------------------------------------------------------------------------

def test_exemplo_enunciado():
    source = (
        'num a = 0 ;\n'
        'num b = 5 + a ;\n'
        'text c = "teSte" ;\n'
    )
    expected = (
        'NUM VAR EQ NUM SEMICOLON\n'
        'NUM VAR EQ NUM ADD VAR SEMICOLON\n'
        'TEXT VAR EQ CONST SEMICOLON'
    )
    assert _run(source) == expected

def test_programa_completo():
    source = (
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
    expected = (
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
    assert _run(source) == expected

def test_palavras_reservadas_e_booleanos():
    source = (
        'bool flag = true ;\n'
        'bool outro = false ;\n'
        'show flag ;\n'
    )
    expected = (
        'BOOL VAR EQ TRUE SEMICOLON\n'
        'BOOL VAR EQ FALSE SEMICOLON\n'
        'SHOW VAR SEMICOLON'
    )
    assert _run(source) == expected

def test_erro_lexico_caracter_invalido():
    # Qualquer linha inválida invalida toda a entrada
    source = (
        'num x = 5 ;\n'
        'num y = @invalido ;\n'
        'show x ;\n'
    )
    assert _run(source) == 'ERRO'

def test_erro_lexico_id_maior_que_30_chars():
    source = 'num VariavelComMaisDeTrintaCaracteresAqui = 1 ;\n'
    assert _run(source) == 'ERRO'

def test_linhas_em_branco_sao_ignoradas():
    source = (
        'num a = 1 ;\n'
        '\n'
        '   \n'
        'show a ;\n'
    )
    expected = (
        'NUM VAR EQ NUM SEMICOLON\n'
        'SHOW VAR SEMICOLON'
    )
    assert _run(source) == expected

def test_op_eq_maximal_munch():
    # '==' deve ser reconhecido como EQ único, não dois '=' separados
    source = 'show a == 5 ;\n'
    assert _run(source) == 'SHOW VAR EQ NUM SEMICOLON'

def test_op_assign():
    # '=' sozinho deve ser reconhecido corretamente
    source = 'show a = 5 ;\n'
    assert _run(source) == 'SHOW VAR EQ NUM SEMICOLON'


# ---------------------------------------------------------------------------
# Execução direta: roda e imprime resultados de forma legível
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("==================================================")
    print(" TESTE DA QUESTÃO 4: ANALISADOR LÉXICO – LangC")
    print("==================================================\n")
    print(f"-> DFA carregado com {len(_dfa.transitions)} estados.\n")

    testes = [
        ("Teste 1 – Exemplo do enunciado", 'num a = 0 ;\nnum b = 5 + a ;\ntext c = "teSte" ;\n'),
        ("Teste 2 – Programa completo da especificação",
            'show 2 > 2 ;\nnum a = 5 ;\nnum b = 10 ;\nnum soma = a + b ;\n'
            'text mensagem = "Oi!" ;\nshow mensagem ;\nshow a ;\nshow soma ;\n'
            'show a < b ;\nshow a == 5 ;\n'),
        ("Teste 3 – Palavras reservadas e booleanos",
            'bool flag = true ;\nbool outro = false ;\nshow flag ;\n'),
        ("Teste 4 – Erro léxico (caracter inválido)",
            'num x = 5 ;\nnum y = @invalido ;\nshow x ;\n'),
        ("Teste 5 – ID com mais de 30 caracteres",
            'num VariavelComMaisDeTrintaCaracteresAqui = 1 ;\n'),
        ("Teste 6 – Linhas em branco ignoradas",
            'num a = 1 ;\n\n   \nshow a ;\n'),
        ("Teste 7 – Maximal munch: == vs =",
            'show a == 5 ;\nshow a = 5 ;\n'),
    ]

    todos_passaram = True
    for titulo, source in testes:
        print(f"{titulo}:")
        print("-" * 50)
        print(source.rstrip())
        print("\nSaída:")
        resultado = _run(source)
        print(resultado)
        print("-" * 50 + "\n")

    # Roda as assertions programaticamente
    fns = [
        test_exemplo_enunciado,
        test_programa_completo,
        test_palavras_reservadas_e_booleanos,
        test_erro_lexico_caracter_invalido,
        test_erro_lexico_id_maior_que_30_chars,
        test_linhas_em_branco_sao_ignoradas,
        test_op_eq_maximal_munch,
        test_op_assign,
    ]
    print("Verificando assertions...")
    print("-" * 50)
    for fn in fns:
        try:
            fn()
            print(f"  ✅ {fn.__name__}")
        except AssertionError as e:
            print(f"  ❌ {fn.__name__} FALHOU: {e}")
            todos_passaram = False
    print("-" * 50)
    print("\n✅ Todos os testes passaram!" if todos_passaram else "\n❌ Alguns testes falharam.")