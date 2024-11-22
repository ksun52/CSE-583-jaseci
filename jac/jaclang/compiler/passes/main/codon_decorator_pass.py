import time
from typing import Optional, Type
import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.constant import Tokens as Tok



"""THIS IS THE CODE JAYANAKA WROTE"""

class CodonPass(Pass):
    """Graphviz Pass for visualizing Jac AST."""

    def __init__(self, input_ir: ast.AstNode, prior: Optional[Pass] = None) -> None:
        """Initialize Graphviz Pass."""
        self.output_file = "examples/viz/function_2decs_ast.dot"
        self.node_counter = 0
        self.node_map = {}  # Maps nodes to unique IDs for DOT
        self.dot_lines = ["digraph G {"]  # Start of the DOT format
        super().__init__(input_ir, prior)
        self.is_ability = False


    def enter_ability(self, node: ast.Ability) -> None:
        """Enter ability."""
        # node.decorators
        self.is_ability = True
        print('here')
        dec = ast.Name(orig_src = self.ir.source,
                        name = Tok.NAME,
                        value = 'codon',
                        line = 0,
                        end_line= 0,
                        col_start= 0,
                        col_end=0,
                        pos_start=0,
                        pos_end=0,
                    )
        if node.decorators:
            pass
            # node.decorators.items.append(dec)
            # node.add_kids_left([node.decorators])
        else:
            # create a new list with the decorator
            node.decorators = ast.SubNodeList(items=[dec], delim=Tok.DECOR_OP, kid=[dec])
            print('there')
            node.add_kids_left([node.decorators])
    
    def exit_module(self, node: ast.Module) -> None:
        """Exit module."""
        if self.is_ability:
            pass
            #add import
        # node.decorators
            

# Example usage
# Assuming you have an AST `ast_root` to process:
# pass_instance = GraphvizPass(input_ir=ast_root)
# pass_instance.transform(ast_root)


# visualize after running the pass: (bash)
# dot -Tpng examples/viz/function_2decs_ast.dot -o examples/viz/function_2decs_ast.png
