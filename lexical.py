import sys
from config import REGEX_SPEC
from nfa_generator import build_global_nfa
from dfa_converter import nfa_to_dfa

# ---------------------------------------------------------------------------
# Mapeamento interno -> nome de saída exigido pelo enunciado
# ---------------------------------------------------------------------------
TOKEN_OUTPUT_NAME = {
    "NUM":              "NUM",
    "TEXT":             "TEXT",
    "BOOL":             "BOOL",
    "SHOW":             "SHOW",
    "TRUE":             "TRUE",
    "FALSE":            "FALSE",
    "OP_EQ":            "EQ",
    "OP_ASSIGN_OR_EQ":  "EQ",
    "OP_ADD":           "ADD",
    "OP_SUB":           "SUB",
    "OP_MULT":          "MULT",
    "OP_DIV":           "DIV",
    "OP_GT":            "GT",
    "OP_LT":            "LT",
    "LPAREN":           "LPAREN",
    "RPAREN":           "RPAREN",
    "SEMICOLON":        "SEMICOLON",
    "INT_LITERAL":      "NUM",
    "ID":               "VAR",
    "STRING":           "CONST",
}


def simulate_dfa(dfa, input_string):
    current_state = dfa.start_state

    for char in input_string:
        if current_state in dfa.transitions and char in dfa.transitions[current_state]:
            current_state = dfa.transitions[current_state][char]
        else:
            return None

    if current_state in dfa.accept_states:
        return dfa.accept_states[current_state]
    return None

    """
    Percorre a linha caractere usando a estratégia de maximal munch.
    Retorna uma lista de tokens de saída ou None em caso de erro léxico.
    """
def tokenize_line(dfa, line):
    tokens = []
    i = 0
    n = len(line)

    while i < n:
        if line[i] in (' ', '\t'):
            i += 1
            continue

        last_valid_end = -1
        last_valid_token = None

        for j in range(i + 1, n + 1):
            lexeme = line[i:j]
            result = simulate_dfa(dfa, lexeme)
            if result is not None:
                last_valid_end = j
                last_valid_token = result

        if last_valid_token is None:
            return None
        
        if last_valid_token in ("ID", "INT_LITERAL"):
            if last_valid_end < n:
                next_char = line[last_valid_end]
                if next_char.isalnum() or next_char == '_':
                    # A palavra foi cortada no meio (ex: estourou limite de tamanho)
                    return None

        output_name = TOKEN_OUTPUT_NAME.get(last_valid_token, last_valid_token)
        tokens.append(output_name)
        i = last_valid_end

        output_name = TOKEN_OUTPUT_NAME.get(last_valid_token, last_valid_token)
        tokens.append(output_name)
        i = last_valid_end

    return tokens

def analyze(source_code, dfa):
    output_lines = []

    for line in source_code.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        result = tokenize_line(dfa, stripped)

        if result is None:
            return "ERRO"
        else:
            output_lines.append(" ".join(result))

    return "\n".join(output_lines)


if __name__ == "__main__":
    nfa_base = build_global_nfa(REGEX_SPEC)
    dfa = nfa_to_dfa(nfa_base, REGEX_SPEC)

    if len(sys.argv) < 2:
        print("Uso: python lexical.py <arquivo_fonte>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"ERRO: Arquivo '{file_path}' não encontrado.")
        sys.exit(1)

    print(analyze(source, dfa))