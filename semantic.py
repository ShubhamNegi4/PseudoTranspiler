#       custom class to represent semantic errors 
class SemanticError(Exception):
        def __init__(self, message):
                self.message = message
                super().__init__(self.message)


#       checks for undeclared variables and scope of variables        
def DelarationAndScope(node,SymbolTable):
        # Handle lists (e.g., statement_list)
        if isinstance(node, list):

                for child in node:
                        DelarationAndScope(child,SymbolTable)
                return
        
        #       check for scope and declaration
        elif node.type == "input":

                #       INPUT ID: Declare the variable
                child = node.children[0]
                #       it declared just reinitialized else declared
                if child.value not in SymbolTable:
                      SymbolTable.add(child.value)
                return
        
        elif node.type == "output":

                #       PRINT term_low: Check the expression
                child = node.children[0]
                #       variables used here should be declared
                DelarationAndScope(child,SymbolTable)
                return
                
        elif node.type == "assignment":

                #       SET ID TO term_low:
                variable = node.children[0]
                expression = node.children[1]
                #        it declared just reinitialized else declared
                if variable.value not in SymbolTable:
                      SymbolTable.add(variable.value)
                #        variables used here should be declared
                DelarationAndScope(expression,SymbolTable)
                return
        
        elif node.type == "variable":
               if node.value not in SymbolTable:
                      raise SemanticError(f"{node.value} variable not declared")
        
        elif node.type == 'number' or node.type == "string":
                #       ignore the literals they need not to be defined
                return
        
        # Recurse on children
        for child in node.children:
                #       if it is any other type like operator , if , while
                #       etc then just check th evariables
                DelarationAndScope(child,SymbolTable)


'''
        NOTE : since INPUT x is of type unknown , we introduced
        the === operator hence the type of input is kept "STRING"
        initially but later if it is chceked for integer ( x === 1)
        we change it to integer
'''

def TypeChecks(node,SymbolTable):
        # Handle lists (e.g., statement_list)
        if isinstance(node, list):

                for child in node:
                        TypeChecks(child,SymbolTable)
                return None
        
        #       declaration part of variable
        if node.type == "input":

                #       INPUT ID: Declare the variable as string for now
                child = node.children[0]
                if child.value not in SymbolTable:
                      SymbolTable[child.value] = "string"
                return None
        
        elif node.type == "assignment":

                #       SET ID TO term_low: the type has to be type of term_low
                variable = node.children[0]
                expression = node.children[1]
                #        it declared just reinitialized else declared
                if variable.value not in SymbolTable:
                      SymbolTable[variable.value] = TypeChecks(expression,SymbolTable)
                return None
        
        elif node.type == "output":

                #       PRINT term_low: Check the expression
                child = node.children[0]
                #       variables used here should be declared
                TypeChecks(child,SymbolTable)
                return None
        
        elif node.type == "string":

                return "string"
        elif node.type == "number":

                return "number"
        elif node.type == "variable":

                '''       since we already checked for decleration 
                          and handled dynamic type our variable here has to have a type
                '''
                return SymbolTable[node.value]
        
        #       the actual type chcek at the opeara
        # tors
        elif node.type == "operator":

                leftChild = node.children[0]
                rightChild = node.children[1]

                # the type change mentioned at NOTE
                if node.value == "===":
                        #       left child will always be a variable
                        SymbolTable[leftChild.value] = rightChild.type
                else:
                        # get the types
                        leftType = TypeChecks(leftChild,SymbolTable)
                        rightType = TypeChecks(rightChild,SymbolTable)

                        if leftType != rightType:
                                raise SemanticError(f"Type mismatch : {leftType} {node.value} {rightType}")

                        return leftType


        
         # Recurse on children
        for child in node.children:
                #       if it is any other type like if , while
                #       etc then just check th evariables
                TypeChecks(child,SymbolTable)
        return None


        


def SemanticAnalysis(ast):
        try:
                # 1. check for undeclared variables
                SymbolTable = set()
                DelarationAndScope(ast,SymbolTable)

                # 2. check for scope of variables 
                SymbolTable = {}
                TypeChecks(ast,SymbolTable)

                return True
        except SemanticError as e:
                print(f"Caught custom error: {e}")
                return False
