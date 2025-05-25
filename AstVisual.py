#                       Text Based visualization 

def dfsText(node, indent):
        # Handle lists (e.g., statement_list)
        if isinstance(node, list):
                for child in node:
                        dfsText(child, indent)
                return
    
        # Print node type and value (if any)
        value_str = f" (value: {node.value})" if node.value is not None else ""
        print("  " * indent + f"|-- {node.type}{value_str}")
        
        # Recurse on children
        for child in node.children:
                dfsText(child, indent + 1)



def visualizeText(node):
        print("AST Visualization:")
        dfsText(node, 0)




'''
                     GRAPH Based visualization 
                      grphviz is a graph visualizationb library which lets 
                      you define nodes and edges of a graph and it handles the
                      visualization
'''

from graphviz import Digraph


def visualizeGraph(ast):
        graph = Digraph(comment='AST Visualization', format='png')
    
        node_id  = 0

        # Helper to create a label for a node.
        def create_node_label(node):
                label = ''
                if isinstance(node,list):
                        label = "statement_list"
                else:
                        label = f"type : {node.type}"
                        if node.value is not None:
                                label += f"\n(value: {node.value})"
                return label
        

        # DFS traversal to add nodes and edges to the Graphviz graph
        def dfs(node):
                nonlocal node_id , graph
                if node is not None:
                        # Node can be a statement list or a token node
                        curr_id = f'node_{node_id}'
                        node_id += 1
                        graph.node(curr_id, create_node_label(node))
                        for child in (node if isinstance(node,list) else node.children):
                                child_id = dfs(child)
                                if child_id != -1 or child_id != None:
                                        graph.edge(curr_id,child_id)
                        return curr_id
                elif node is None:
                        # Handle None (e.g., empty else_part)
                        return -1
                


        # start the dfs
        dfs(ast)
        graph.render('astIMG', view=False)  # Creates ast.png afro graph object , view can be used to open it
        print(f"AST visualization saved as astIMG.png")
