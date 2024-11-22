import time
from typing import Optional, Type
import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.constant import Tokens as Tok


class CodonDecoratorPass(Pass):
    """Adds @codon.jit decorator to statically typed functions."""

    def enter_ability(self, node: ast.Ability) -> None:
        """Process each ability node."""
        if self.is_statically_typed(node):
            print("in codon generator")
            codon_decorator = self.create_codon_decorator()
            print("made codon decorator")
            if not node.decorators:
                print("adding codon decorator")
                node.decorators = ast.SubNodeList(
                    items=[codon_decorator],
                    delim=Tok.DECOR_OP, 
                    kid=[node.gen_token(Tok.DECOR_OP), codon_decorator]
                )
                print(node.decorators)
                node.add_kids_left([node.decorators])
            else:
                node.decorators.items.append(codon_decorator)
                node.decorators.add_kids_left([codon_decorator])

    def is_statically_typed(self, node: ast.Ability) -> bool:
        """Check if function has full type annotations."""
        # Check return type exists
        # TODO: REMOVE THIS TO MAKE STATIC CHECK FUNCTION
        return True
    
        if not node.signature.return_type:
            return False

        # Check all parameters have type annotations
        if node.signature.params:
            for param in node.signature.params.items:
                if not param.type_tag:
                    return False
                
                # Get the actual type from the annotation
                param_type = param.type_tag.tag
                if not isinstance(param_type, (ast.BuiltinType, ast.ArchRef)):
                    return False

        return True


    def create_codon_decorator(self) -> ast.AtomTrailer:
        """Create @codon.jit decorator."""
        target=ast.Name(
                orig_src=self.ir.source,
                name=Tok.NAME,
                value="codon",
                line=0, end_line=0,
                col_start=0, col_end=0,
                pos_start=0, pos_end=0
            )
        right=ast.Name(
                orig_src=self.ir.source, 
                name=Tok.NAME,
                value="jit",
                line=0, end_line=0,
                col_start=0, col_end=0,
                pos_start=0, pos_end=0
            )
        period=ast.Token(
                name=Tok.NAME,
                value=".",
                orig_src=self.ir.source,
                line=0, end_line=0,
                col_start=0, col_end=0,
                pos_start=0, pos_end=0
            )
        return ast.AtomTrailer(
            target=target,
            right=right,
            is_attr=True,
            is_null_ok=False,
            kid=[target, period, right]
            # TODO: Make the attr and kid stuff is correct
        )