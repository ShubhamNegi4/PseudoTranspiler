# PseudoTranspiler
🔧 Converts pseudocode to Python using compiler design principles.


## APPROACH : 
1.	Input  : We begin with a well-defined grammar and syntax for our pseudocode language (inspired by common educational styles like pseudocode) which will be inputed from terminal / file / web app
2.	 Lexical Analysis : Using this grammar, we will implement a lexical analyzer using Python’s re module or libraries like PLY.lex (Python Lex-Yacc) to tokenize the input into well defined tokens of the language. 
3.	Syntax Analysis :These tokens will be passed to a parser built with PLY.yacc or a custom parser ( top down or bottom up) that constructs an Abstract Syntax Tree (AST) representing the structure of the pseudocode.
4.	Semantic Analysis  :The semantic analyzer will traverse the AST to perform type checks, scope validation, and other logical validations using symbol tables. 
5.	Code Generation : Once verified, the code generation phase will translate the AST into clean, equivalent Python code using a template-based or tree-walk approac

## SYSTEM ARCHITECTURE
![Arch](arch.png)

## PSEUDOCODE STANDARD 
this portion will keep on updating after new features till this point we have : 
1. Variables
	Declaration and Assignment:
        Syntax:
                SET x TO 10
                SET y TO x + 5
        Input: 
                INPUT <variable> 
        OUTPUT:
                PRINT <expression>
       
       
2. Conditionals
        If-Else Statement:
        Syntax:
                IF <condition> THEN
                <statements>
                ELSE
                <statement>
                END IF
        (if else ladder will do it later)


3. Iteratives 
        Syntax:
                WHILE <condition> DO
                <statements>
                END WHILE
        (for loop will do it later)

4. Expressions & Operators:
Structure: <term> <operator> <term> or single <term>
Terms: Variables, numbers, strings (in quotes)

Arithmetic: PLUS, MINUS, MULTIPLY, DIVIDE , MOD
Comparison: EQ, NE, GT, LT, GE, LE


