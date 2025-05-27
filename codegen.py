def utility(s,indentation):
        return ' '*indentation + s

#       this dfs traverses the ast nodes and creates equivalent python code
def dfs(node,Pycode,indentation):

        # Handle lists (e.g., statement_list)
        if isinstance(node, list):

                #       start code gen with same indentation
                for child in node:
                        dfs(child,Pycode,indentation)
                return None
        
        elif node.type == "input":

                #       INPUT ID: just add the equal python code
                child = node.children[0]
                s = f'{child.value} = input()'
                Pycode.append(utility(s,indentation))
                return None
        
        elif node.type == "output":

                #       PRINT term_low: add the equal python code recuursively
                child = node.children[0]
                expression = dfs(child,Pycode,indentation).lstrip()
                s = f'print({expression})'
                Pycode.append(utility(s,indentation))
                return None
        
        elif node.type == "assignment":

                #       SET ID TO term_low:
                variable = node.children[0]
                child = node.children[1]

                #       add the equal python code recuursively
                expression = dfs(child,Pycode,indentation).lstrip()
                s = f'{variable.value} = {expression}'
                
                Pycode.append(utility(s,indentation))
                return None
        
        elif node.type == "string":

                s = f'"{node.value}"'
                return s
        
        elif node.type == "number" or node.type == "variable":

                s = f'{node.value}'
                return s
        
        elif node.type == "while":

                #       while_stmt - WHILE condition DO NEWLINE statement_list END
                condition = node.children[0]
                expression = node.children[1]

                #       generate initial condition line
                cond = dfs(condition,Pycode,indentation).lstrip()
                s = f'while {cond}:'
                Pycode.append(utility(s, indentation))
                
                 #       generate the body of if
                dfs(expression, Pycode, indentation + 4)
                return None
        
        elif node.type == "if":

                # if_stmt - IF condition THEN NEWLINE statement_list else_part END
                condition = node.children[0]
                expression = node.children[1]

                #       generate initial condition line
                cond = dfs(condition, Pycode, indentation)
                if isinstance(cond,list):

                        #       ass extra conversion to integer
                        s = f'if {cond[1]}:'
                        Pycode.append(utility(s, indentation))
                        s = f'{cond[0]} = int({cond[0]})'
                        Pycode.append(utility(s, indentation + 4))
                else:

                        s = f'if {cond}:'
                        Pycode.append(utility(s, indentation))

                
                 #       generate the body of if
                dfs(expression, Pycode, indentation + 4)

                if len(node.children) == 3:
                        s = f'else:'
                        Pycode.append(utility(s, indentation))

                        #       generate the body of else 
                        else_part = node.children[2]
                        dfs(else_part, Pycode, indentation + 4)
                return None
        
        else:
                #       operators
                if node.value == "===":

                        #       deal with type conversion
                        #       term op temp
                        leftChild = node.children[0]
                        rightChild = node.children[1]

                        #       generate both th expressions
                        leftexpression = dfs(leftChild, Pycode, indentation).lstrip()
                        rightexpression = dfs(rightChild, Pycode, indentation).lstrip()
                        op = node.value

                        return [leftChild.value , f'isdigit({leftexpression})']
                
                else:

                        #       term op temp
                        leftChild = node.children[0]
                        rightChild = node.children[1]

                        #       generate both th expressions
                        leftexpression = dfs(leftChild, Pycode, indentation)
                        rightexpression = dfs(rightChild, Pycode, indentation)
                        op = node.value

                        return f'({leftexpression} {op} {rightexpression})'







def CodeGenerator(ast):
        Pycode = []
        dfs(ast,Pycode,0)
        return '\n'.join(Pycode)


  