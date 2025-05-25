import lexer
import parser
import AstVisual
import semantic


if __name__ == "__main__":

        print("Enter\n 1. TO input from terminal\n 2. To input from file")
        print("Enter your pseudocode (end with a blank line):")
        choice = input()

        if choice == '1' or choice == '2':
                data = ""

                if choice == '1':
                        print("Enter your pseudocode (end with a blank line):")
                        lines = []
                        while True:
                                line = input()
                                if line.strip() == "":
                                        break
                                lines.append(line)
                        data = "\n".join(lines)
                else:
                        try:
                                with open('input.txt', 'r') as file:
                                        data = file.read()
                        except FileNotFoundError:
                                print("Make an input.txt file (exact name required)")
                                exit()


                #       call the lexer
                lexer.lexer.input(data)
                print('*********************************************************')
                print("\nTokens : Each token has a type , value , lex no : think of it as row no , lexpos : think of it as column no\n")
                for token in lexer.lexer:       # iterate over lexer object itself to get matched tokens
                        print(f"Type: {token.type}")
                        print("        Value:",end=" ")
                        if token.value == '\n':
                                print("newline")
                        else:
                                print(token.value)
                        print(f"        line no: {token.lineno}")
                        print(f"        lexpos: {token.lexpos}")

                if lexer.lexer.errors > 0:
                        exit(1)

                #       call the parser
                print('*********************************************************')
                try:
                        ast = parser.parser.parse(data,lexer = lexer.lexer)
                except  Exception as e:
                        print("Caught an error:", e)
                        exit()

                print("AST:")
                AstVisual.visualizeText(ast)
                AstVisual.visualizeGraph(ast)

                #       call the semantic analyzer
                if semantic.SemanticAnalysis(ast):
                        print("AST is Semantically correct")
                else:
                        print("AST is Semantically not correct")
                        exit()


        else:
                print("Enter valid choice")
