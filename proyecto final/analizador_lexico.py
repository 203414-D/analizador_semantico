import ply.lex as lex
import ply.yacc as yacc

# Lista de tokens
tokens = (
    'WHILE',
    'IF',
    'ELSE',
    'DEF',
    'IDENTIFIER',
    'REL_OP',
    'OPEN_PAREN',
    'CLOSE_PAREN',
    'COLON',
    'PRINT',
    'NUMBER',
    'QUOTATION',
    'ASSING',
    'MAS',
)

# Palabras clave reservadas
reserved = {
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'def': 'DEF',
    'print': 'PRINT'
}

# Definición de patrones para los tokens
t_REL_OP = r'>=|<=|!=|<|>|=='
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_COLON = r':'
t_QUOTATION = r'"'
t_ASSING = r'='
t_MAS = r'\+'




def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    t.type = 'NUMBER'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER') if t.value.lower() not in reserved else reserved.get(t.value.lower())
    return t

def t_error(t):
    t.type = 'ILLEGAL'
    t.value = t.value[0]
    t.lexer.skip(1)

# Ignorar espacios en blanco y tabulaciones
t_ignore = ' \t'

# Función para manejar los saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Reglas de la gramática
def p_declaration(p):
    ''' 
    declaration : WHILE operand REL_OP operand COLON PRINT OPEN_PAREN QUOTATION IDENTIFIER QUOTATION CLOSE_PAREN IDENTIFIER MAS ASSING NUMBER
                | IF operand REL_OP operand COLON PRINT OPEN_PAREN QUOTATION IDENTIFIER QUOTATION CLOSE_PAREN ELSE COLON PRINT OPEN_PAREN QUOTATION IDENTIFIER QUOTATION CLOSE_PAREN
                | DEF IDENTIFIER OPEN_PAREN IDENTIFIER CLOSE_PAREN COLON PRINT OPEN_PAREN IDENTIFIER CLOSE_PAREN IDENTIFIER OPEN_PAREN IDENTIFIER CLOSE_PAREN
                | IDENTIFIER ASSING valor 
                | declaration declaration
    '''
    if len(p) == 3:
        # Para múltiples definiciones, concatenamos los resultados
        p[0] = p[1] + '\n' + p[2]
    else:
        if p[1] == 'while':
            p[0] = "Ciclo while con condición: {} {} {} y contenido: {}".format(p[3], p[4], p[5], p[8])
        elif p[1] == 'if':
            p[0] = "Condicional: {} {} {} y contenido: {} sino: {}".format(p[3], p[4], p[5], p[8], p[11])
        elif p[1] == 'def':
            if len(p) == 8:
                p[0] = "Declaración de función: {} con parámetro: {} y contenido: {}".format(p[2], p[4], p[7])
            else:
                p[0] = "Declaración de función: {} sin parámetros y contenido: {}".format(p[2], p[6])
        else:
            p[0] = "Declaración de variable: {} {}".format(p[1], p[2])

def p_operand(p):
    '''
    operand : IDENTIFIER
            | valor
    '''
    p[0] = p[1]

def p_valor(p):
    '''
    valor : QUOTATION IDENTIFIER QUOTATION
            | NUMBER
    '''
    p[0] = p[1]

def p_error(p):
    if p:
        raise SyntaxError("Error sintáctico en la posición {}: '{}...'".format(p.lexpos, p.value))
    else:
        raise SyntaxError("Error sintáctico al final del texto")

def parse_input(input_text):
    lexer = lex.lex()
    parser = yacc.yacc()
    lexer.input(input_text)
    token_list = []
    lexeme_count = {}
    valid = False

    while True:
        tok = lexer.token()
        if not tok:
            break
        if tok.type != 'ILLEGAL':  # Ignorar tokens ilegales
            token_list.append((tok.type, tok.value))
            if tok.value in lexeme_count:
                lexeme_count[tok.value] += 1
            else:
                lexeme_count[tok.value] = 1

    try:
        result = parser.parse(input_text)
        valid = True
    except SyntaxError as e:
        print("Error sintáctico:", e)

    return token_list, lexeme_count, valid


