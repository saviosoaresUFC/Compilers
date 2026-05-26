STRING_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 +-*/=><();_!@#$%&?| \t\n"

REGEX_SPEC = [
    ("NUM", "num"),
    ("TEXT", "text"),
    ("BOOL", "bool"),
    ("SHOW", "show"),
    ("TRUE", "true"),
    ("FALSE", "false"),
    ("OP_EQ", "=="),
    ("OP_ASSIGN_OR_EQ", "="),
    ("OP_ADD", "+"),
    ("OP_SUB", "-"),
    ("OP_MULT", "*"),
    ("OP_DIV", "/"),
    ("OP_GT", ">"),
    ("OP_LT", "<"),
    ("LPAREN", "("),
    ("RPAREN", ")"),
    ("SEMICOLON", ";"),
    ("INT_LITERAL", "[0-9]+"),
    ("ID", "letter(letter|digit|_)*"),
    ("STRING", "\"(any_char_except_quote)*\"")
]