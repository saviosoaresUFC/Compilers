import sys
from config import REGEX_SPEC, TOKEN_OUTPUT_NAME
from nfa_generator import build_global_nfa
from dfa_converter import nfa_to_dfa


def simulate_dfa(dfa, input_string):
    """Simula a execução de um DFA caractere por caractere."""
    current_state = dfa.start_state

    for char in input_string:
        if current_state in dfa.transitions and char in dfa.transitions[current_state]:
            current_state = dfa.transitions[current_state][char]
        else:
            return None

    if current_state in dfa.accept_states:
        return dfa.accept_states[current_state]
    return None


# utiliza a estrategia maximal munch
def tokenize_line(dfa, line):
    """
    Percorre a linha caractere a caractere usando a estratégia de maximal munch.
    Retorna uma lista de tokens de saída ou None em caso de erro léxico.
    """
    tokens = []
    i = 0
    n = len(line)

    while i < n:
        if line[i] in (' ', '\t'):
            i += 1
            continue

        last_valid_end = -1
        last_valid_token = None
        current_state = dfa.start_state
        
        # avança char por char sem reiniciar o DFA
        for j in range(i, n):
            char = line[j]
            
            if current_state in dfa.transitions and char in dfa.transitions[current_state]:
                current_state = dfa.transitions[current_state][char]
                
                # salva como melhor candidato até o momento
                if current_state in dfa.accept_states:
                    last_valid_end = j + 1
                    last_valid_token = dfa.accept_states[current_state]
            else:
                break

        if last_valid_token is None:
            return None

        if last_valid_token in ("ID", "INT_LITERAL"):
            if last_valid_end < n:
                next_char = line[last_valid_end]
                if next_char.isalnum() or next_char == '_':
                    return None

        if last_valid_token not in TOKEN_OUTPUT_NAME:
            return None

        tokens.append(TOKEN_OUTPUT_NAME[last_valid_token])
        i = last_valid_end

    return tokens


"""
    Recebe o código-fonte completo como string e retorna a saída do
    analisador léxico: uma linha de tokens por linha de entrada, ou
    a palavra 'ERRO' (sozinha) caso qualquer linha tenha erro léxico,
    invalidando toda a entrada.
"""
def analyze(source_code, dfa):
    output_lines = []

    for line in source_code.splitlines():
        stripped = line.strip()

        if not stripped:
            continue

        result = tokenize_line(dfa, stripped)

        if result is None:
            return "ERRO"

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