import ply.lex as lex



'''                                    List of Token Names

this is done to tell the lexer about all the tokens our tokenizer can return to the parser
in lex.c this is generally imporetd form yy.tab.h but in PLY we define it here only

'''

tokens = [
        # Keywords
        'SET', 'TO', 'INPUT' , 'PRINT',
        'IF', 'THEN', 'ELSE', 'END', 'WHILE', 'DO',

        # Operators
        'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MOD',
        'EQ', 'NE', 'GT', 'LT', 'GE', 'LE',
        'TYPE_EQ',

        # Literals
        'NUMBER', 'STRING', 'ID',

        # Special
        'NEWLINE',
]

'''                                    SET OF RESERVED KEYWORDS

this is just for our look so that we dont need to used if statement to seprate identifiers
from reserved keywords , this is not a compulsory flow of PLY

'''
reserved  = {
        'SET': 'SET',
        'TO': 'TO',
        'INPUT': 'INPUT',
        'PRINT': 'PRINT',
        'IF': 'IF',
        'THEN': 'THEN',
        'ELSE': 'ELSE',
        'END': 'END',
        'WHILE': 'WHILE',
        'DO': 'DO'
}

'''                                    RULE SECTION

this is teh part where lexer matches a regular expression for a token in input and 
does suitable action to it

there are two types of declaration in PLY 

1 . t_PLUS      = r'\+'
                        this is equal to doing  "+"     { return PLUS; } in lex.c but 
                        since our token is already with lex writing a rule with t_TOKEN 
                        automatically tells which token to return

2 . def t_NUMBER(token):        token ha sthe matched value like yytext
    r'\d+'                      this regex is not matched here it is taken my lex and mapped to this function
    token.value = int(token.value)
    return t
                        this is equal to doing  [0-9]+ { 
                                                        yylval = atoi(yytext);
                                                        return NUMBER;
                                                } in lex.c
                        the tokens which need some pre-processing and not direct return 
                        are mentioned here


'''


# operators
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_MULTIPLY  = r'\*'
t_DIVIDE    = r'/'
t_MOD       = r'%'
t_EQ        = r'=='
t_NE        = r'!='
t_GE        = r'>='
t_LE        = r'<='
t_GT        = r'>'
t_LT        = r'<'
t_TYPE_EQ   = r'==='


# Ignored characters (spaces and tabs) [\t] {}
t_ignore = ' \t'


#identifier
def t_ID(token):
        r'[a-zA-z][a-zA-Z0-9_]*'
        if token.value.upper() in reserved:
                token.type = reserved[token.value.upper()]
        else:
                token.type = "ID"
        token.value = token.value
        return token


# string literal
def t_STRING(token):
        r'"[^"]*"'
        token.type = "STRING"
        token.value = token.value[1:-1]       # Strip quotes
        return token


# numeric literal
def t_NUMBER(token):
        r'\d+'
        token.type = "NUMBER"
        token.value = int(token.value)
        return token


# newline
def t_NEWLINE(token):
        r'\n+'
        token.lexer.lineno += len(token.value)          #in PLY eaxh token has reference to the lexer class
                                                # which is token.lexer so we can upadte lexer.lineno 
        token.value = '\n'
        return token


# error handling
def t_error(token):
        print(f"Illegal character '{token.value[0]}' at line {token.lexer.lineno}")
        token.lexer.skip(1)             #skip the faulty character ( can stop here as well but let the
                                        # lexer collect all errors , dont run parser if you get errors)
        token.lexer.errors += 1




'''
        get the tokenizer object , When this lex.lex() runs:
        PLY will: Scan the entire lexer.py module (where you wrote all the rules).
        Collect: tokens , all the t_* regex rules , t_error, t_ignore, etc.
        and Generate a working finite-state machine lexer, and store it in the object lexer.
        
'''
lexer = lex.lex()
lexer.errors = 0


