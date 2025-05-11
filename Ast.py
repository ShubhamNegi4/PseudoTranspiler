'''
        Lets define a base class node for our Ast , all node in our language will 
        follow this structure for consistency
        type is the type of our node , children holds important 
        nodes to make a valid grammer rule
        value is the value of node
        rest all syntactical sugar is not kept in AST

        NOTE : in this version of representation only the literals 
        have "VALUE" attribute to them 
'''
class Node:
        def __init__(self,type,children=None,value=None):
                self.type = type
                self.children = (children if children else [])
                self.value = value


'''
    assignment - SET ID TO operand
    assignment only needs the id and operand 

'''
class AssignNode(Node):
        def __init__(self,variableNode,valueNode):
                #       type  , childrens - Node() of number , string , id
                super().__init__("assigment", [variableNode,valueNode])


'''
        input_stmt - INPUT ID
        input only needs id 

'''
class InputNode(Node):
        def __init__(self, variableNode):
                super().__init__("input",[variableNode])


'''
        output_stmt - PRINT term_low
            | PRINT operand
        output only need operand or termlow
'''
class OutputNode(Node):
        def __init__(self, variableORliteralNode):
                super().__init__("output",[variableORliteralNode])


'''
        if_stmt - IF condition THEN NEWLINE statement_list else_part END IF
        is only needs the condition , statemnts , else part

'''
class IfNode(Node):
        def __init__(self,conditionNode,statementNode,elseNode):
                super().__init__("if",[conditionNode,statementNode,elseNode] 
                                if elseNode else [conditionNode,statementNode])


'''
        while_stmt - WHILE condition DO NEWLINE statement_list END WHILE
        while only needs conditions and statemets

'''
class WhileNode(Node):
        def __init__(self,conditionNode,statementNode):
                super().__init__("while",[conditionNode,statementNode])
                

'''
        condition - term_low comp_op term_low
        comp_op - EQ | NE | GT | LT | GE | LE
        term_low - term_low PLUS term_high
         | term_low MINUS term_low
         | term_high

        term_high - term_high MULTIPLY operand
          | term_high DIVIDE operand
          | term_high MOD operand
          | operand
        operators become teh value and operands are children

'''
class BinaryOperatorNode(Node):
        def __init__(self,leftNode,rightNode,value):
                super().__init__("operator",[leftNode,rightNode], value)


'''
        operand - NUMBER
                | STRING
                | ID
        this can be represented by just using Node("number",[],10)
                                              Node("string",[],"hello")
                                              Node("variable",[],"name")
'''