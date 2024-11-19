import time
from typing import Optional, Type
import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass


class GraphvizPass(Pass):
    """Graphviz Pass for visualizing Jac AST."""

    def __init__(self, input_ir: ast.AstNode, prior: Optional[Pass] = None) -> None:
        """Initialize Graphviz Pass."""
        self.output_file = "examples/viz/simple.dot"
        self.node_counter = 0
        self.node_map = {}  # Maps nodes to unique IDs for DOT
        self.dot_lines = ["digraph G {"]  # Start of the DOT format
        super().__init__(input_ir, prior)

    def enter_node(self, node: ast.AstNode) -> None:
        """Run on entering a node: collect data for visualization."""
        node_id = self.get_unique_id(node)
        node_label = self.get_node_label(node)

        # Record the node's type and name
        self.dot_lines.append(f'  {node_id} [label="{node_label}"];')

        # If the node has a parent, create an edge from parent to child
        if node.parent:
            parent_id = self.get_unique_id(node.parent)
            self.dot_lines.append(f'  {parent_id} -> {node_id};')

    def get_unique_id(self, node: ast.AstNode) -> str:
        """Generate or retrieve a unique ID for the node."""
        if node not in self.node_map:
            self.node_map[node] = f"node{self.node_counter}"
            self.node_counter += 1
        return self.node_map[node]

    def get_node_label(self, node: ast.AstNode) -> str:
        """Generate a label for the node based on its type and name."""
        # Extract the node type
        node_type = type(node).__name__

        # Attempt to extract a name if possible
        node_name = getattr(node, "name", None)
        node_name_str = node_name.value if hasattr(node_name, "value") else str(node_name)

        # Create a label for visualization
        return f"{node_type}\\n{node_name_str}" if node_name else node_type

    def after_pass(self) -> None:
        """After pass, write data to the output file."""
        # Close the DOT graph
        self.dot_lines.append("}")

        # Write to file
        with open(self.output_file, "w") as f:
            f.write("\n".join(self.dot_lines))
        print(f"AST data written to {self.output_file}.")

# Example usage
# Assuming you have an AST `ast_root` to process:
# pass_instance = GraphvizPass(input_ir=ast_root)
# pass_instance.transform(ast_root)


# visualize after running the pass: (bash)
# dot -Tpng examples/viz/simple_ast.dot -o examples/viz/simple_ast.png
