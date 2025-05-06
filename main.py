import lexer

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


                #       call lexer ( yylex() in lex.c)
                lexer.lexer.input(data)
                print("\nTokens:\n")
                for token in lexer.lexer:       # iterate over lexer object itself to get matched tokens
                        print(f"Type: {token.type}, Value: {token.value}")

        else:
                print("Enter valid choice")
