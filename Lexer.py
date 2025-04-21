import ply.lex as lex

# Reserved keywords
reserved = {
    'SET': 'SET',
    'TO': 'TO',
    'PRINT': 'PRINT',
    'INPUT': 'INPUT',
    'IF': 'IF',
    'THEN': 'THEN',
    'ELSE': 'ELSE',
    'END': 'END',
    'WHILE': 'WHILE',
    'DO': 'DO',
    'EQ': 'EQ',
    'NE': 'NE',
    'GT': 'GT',
    'LT': 'LT',
    'GE': 'GE',
    'LE': 'LE',
    'PLUS': 'PLUS',
    'MINUS': 'MINUS',
    'MULTIPLY': 'MULTIPLY',
    'DIVIDE': 'DIVIDE',
    'MOD': 'MOD',
}

# List of token names
tokens = [
    'NUMBER', 'STRING', 'ID',
] + list(set(reserved.values()))

# Ignored characters (spaces and tabs)
t_ignore = ' \t'

# Token definitions
def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value.strip('"')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.upper(), 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character:", t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Main

if __name__ == "__main__":
    print("Enter your pseudocode (end with a blank line):")

    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    data = "\n".join(lines)
    lexer.input(data)

    print("\nTokens:\n")
    for tok in lexer:
        print(f"Type: {tok.type}, Value: {tok.value}")