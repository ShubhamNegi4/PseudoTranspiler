import ply.yacc as yacc

'''     
        tokens are required to cross check if the grammer rules defines 
        are is using valid tokens or not hence tokens are always uppercase
        this is equalent to writing  %token NUMBER STRING ID ... in yacc.c

'''
from lexer import tokens

'''     SIDE NOTE : 
        The lex.lex() already made the lexer object ready to take input and make then into 
        corresponsing tokens . 

        This is because the parser works on tokens and direct values 
        example " 4 * 5 " needs to be converted to " ID MULTIPY ID " to be made grammer
        
        Hence the actual calling of parser takes data and teh tokenizer
        (Ast = parser.parse(data, lexer=lexer.lexer))

        HOW to write grammer in python : 


'''
import Ast

'''
        The operators used in grammer need to define their associativity and precedence
        in this section thi is equal to writing                 in yacc.c
                                                %left '+' '-'
                                                %left '*' '/'

'''

# Precedence rules
precedence = (
        # altough this first rule's "ASSOCIATIVITY" is pretty useless 
        ('left', 'EQ', 'NE', 'GT', 'LT', 'GE', 'LE'),  # Lowest precedence
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE', 'MOD'),         # Highest precedence
)


start = "program"       # define start symbol 

'''
        The actual rules of grammer are defined in this 
        
        Syntax : 

                def p_expr_plus(p):
                        "expr : expr PLUS term"
                        p[0] = p[1] + p[3]

                this is similar to 
                expr : expr PLUS term { $$ = $1 + $3; } in yacc.c

        ----> the name of the function can be anything as long as it follows teh naming convention
        of p_something_related_to_grammer_rule_it_is_for

        ----> the parser generates a parsing table in the memory using the grammer we are giving it
        then using that table stack starts implementation , when teh actual reduce happens
        teh result / Ast is created 

        ----> when the reducing is happening the parser sends a list of objects (tokens if we dont use Ast else Ast) 
        that matches the rule to ve reduced and we access the lhs and rhs using list[0]  = list[1] + list[2] for example

'''

#grammer for start symbol
def p_program(p):
    'program : statement_list'
    p[0] = p[1]


#grammer for statemnt list
def p_statement_list(p):
    '''statement_list : statement NEWLINE statement_list
                      | statement NEWLINE'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
        #       just make a statement list
    else:
        p[0] = [p[1]]


#grammer for statement
def p_statement(p):
    '''statement : assignment
                 | input_stmt
                 | output_stmt
                 | if_stmt
                 | while_stmt'''
    p[0] = p[1]


#grammer for assignment
def p_assignment(p):
        'assignment : SET ID TO term_low'
        variable = Ast.Node("variable", value=p[2])
        p[0] = Ast.AssignNode(variable, p[4])
        #   variableNode , valueNode


#grammer for output
def p_input_stmt(p):
        'input_stmt : INPUT ID'
        variableNode = Ast.Node('variable',value=p[2])
        p[0] = Ast.InputNode(variableNode)
        #       variableORliteralNode


#grammer for output
def p_output_stmt(p):
        '''output_stmt : PRINT term_low
        '''
        p[0] = Ast.OutputNode(p[2])
        #       variableORliteralNode



#grammer for if part
def p_if_stmt(p):
       '''if_stmt : IF condition THEN NEWLINE statement_list else_part END
       ''' 
       p[0] = Ast.IfNode(p[2],p[5],p[6])
       #        condition , statemnts , else part



#grammer for else part
def p_else_part(p):
        '''else_part : ELSE NEWLINE statement_list
                | 
        '''
        p[0] = p[3] if len(p)>1 else None



#grammer for while
def p_while_stmt(p):
        '''while_stmt : WHILE condition DO NEWLINE statement_list END
        '''
        p[0] = Ast.WhileNode(p[2],p[5])
        #       conditionnode , statementnode


#grammer for condition
def p_condition(p):
        '''condition : term_low comp_op term_low
        '''
        p[0] = Ast.BinaryOperatorNode(p[1],p[3],p[2])
        #   leftnode , rightnode , value  




#grammer for comp_op
def p_comp_op(p):
        '''comp_op : EQ
                | NE 
                | GT 
                | LT 
                | GE 
                | LE
                | TYPE_EQ
        '''
        p[0] = p[1]


#grammer for term_low
def p_term_low(p):
        '''term_low : term_low PLUS term_high
                | term_low MINUS term_high
                | term_high
        '''
        if len(p) == 4:
                p[0] = Ast.BinaryOperatorNode(p[1],p[3],p[2])
                #   leftnode , rightnode , value  
        else:
                p[0] = p[1]


# grammer for term_high
def p_term_high(p):
        '''term_high : term_high MULTIPLY operand
                | term_high DIVIDE operand
                | term_high MOD operand
                | operand
        '''
        if len(p) == 4:
                p[0] = Ast.BinaryOperatorNode(p[1],p[3],p[2])
                #   leftnode , rightnode , value    
        else:
                p[0] = p[1]


# grammer for operand
def p_operand(p):
        '''operand : NUMBER
                | STRING
                | ID
        '''
        if p.slice[1].type == 'NUMBER':
                p[0] = Ast.Node('number',value = p[1])
        elif p.slice[1].type == 'STRING':
                p[0] = Ast.Node('string',value = p[1])
        else:
                p[0] = Ast.Node('variable',value = p[1])
                #       type , value





# When parser sees an input it can't reduce or shift based on the grammar,it calls p_error:
def p_error(p):
        if p:
                print(f"Syntax error at token '{p.value}'")
        else:
                print("Unknown Syntax error")
        
        raise SyntaxError("Invalid syntax in custom parser")



parser = yacc.yacc()