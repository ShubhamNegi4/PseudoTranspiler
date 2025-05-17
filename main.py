import lexer
import parser
import AstVisual

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


                #       call the parser
                print('*********************************************************')
                ast = parser.parser.parse(data,lexer = lexer.lexer)
                print("AST:")
                AstVisual.visualizeText(ast)
                AstVisual.visualizeGraph(ast)



        else:
                print("Enter valid choice")
