#       custom class to represent semantic errors 
class SemanticError(Exception):
        def __init__(self, message):
                self.message = message
                super().__init__(self.message)


#       checks for undeclared variables and scope of variables        
def DelarationAndScope(node,symtab):
        # Handle lists (e.g., statement_list)
        if isinstance(node, list):
                for child in node:
                        DelarationAndScope(child,symtab)
                return
        #       cheek for scope and declaration
        elif node.type == "input":
                child = node.children[0]
                if child.value not in symtab:
                      symtab.add(child.value)
                return
        
        elif node.type == "output":
                child = node.children[0]
                if child.type == "variable" and child.value not in symtab:
                      raise SemanticError(f"{child.value} variable not declared")
                
        elif node.type == "assignment":
                child = node.children[0]
                if child.value not in symtab:
                      symtab.add(child.value)
        
        elif node.type == "variable":
               if node.value not in symtab:
                      raise SemanticError(f"{node.value} variable not declared")
        
        # Recurse on children
        i = (0 if node.type != "assignment" else 1)
        while i < len(node.children):
                DelarationAndScope(node.children[i],symtab)
                i += 1

        


def SemanticAnalysis(ast):
        try:
                # 1. check for undeclared variables
                # 2. check for scope of variables 
                DelarationAndScope(ast,set())
                return True
        except SemanticError as e:
                print(f"Caught custom error: {e}")
                return False
