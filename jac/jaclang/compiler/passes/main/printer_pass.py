import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.semtable import SemInfo, SemRegistry
from jaclang.runtimelib.utils import get_sem_scope
from jaclang.settings import settings


class PrinterPass(Pass):
    """Printer Pass for Jac AST."""

    def enter_node(self, node: ast.AstNode) -> None:
        """Run on entering node."""
        self.log_info(f"Entering: {node.__class__.__name__}: {node.loc}")
        super().enter_node(node)

    def exit_node(self, node: ast.AstNode) -> None:
        """Run on exiting node."""
        super().exit_node(node)
        self.log_info(f"Exiting: {node.__class__.__name__}: {node.loc}")