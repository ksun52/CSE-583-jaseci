import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.constant import Tokens as Tok
from typing import List, Set


# THIS IS OUTLINE, NEED TO CHECKo


class CodonCheckPass(Pass):
    """Adds @codon.jit decorator to eligible statically typed functions."""

    def enter_ability(self, node: ast.Ability) -> None:
        """Process each ability (function) node."""
        # Skip if function is part of an architype
        if isinstance(node.parent.parent, ast.Architype):
            print(f"found an instance of architype: {node.py_resolve_name()}")
            

        # Skip if not statically typed
        if not self.is_statically_typed(node):
            return

        # Collect information about function scope -------------------------------------
        scope_info = self.analyze_function_scope(node)
        if not scope_info['is_eligible']:
            print(f"function scope NOT eligible: {node.py_resolve_name()}")
            return
        # ------------------------------------------------------------------------------

        # Create decorator with pyvars if needed
        codon_decorator = self.create_codon_decorator(scope_info['global_refs'])
        
        # Add decorator to node
        if not node.decorators:
            node.decorators = ast.SubNodeList(
                items=[codon_decorator],
                delim=Tok.DECOR_OP,
                kid=[node.gen_token(Tok.DECOR_OP), codon_decorator]
            )
            node.add_kids_left([node.decorators])
        else:
            node.decorators.items.insert(0, codon_decorator)
            node.decorators.add_kids_left([node.gen_token(Tok.DECOR_OP), codon_decorator])

    def analyze_function_scope(self, node: ast.Ability) -> dict:
        """Analyze function scope for eligibility and collect global references."""
        result = {
            'is_eligible': True,
            'global_refs': set()
        }

        def visit(n: ast.AstNode) -> None:
            if isinstance(n, ast.Assignment):
                # Check if assignment target is non-local
                for target in n.target.items:
                    if isinstance(target, ast.AtomTrailer):
                        result['is_eligible'] = False
                        return
                    
            elif isinstance(n, ast.AtomTrailer):
                # Check for global references
                if isinstance(n.target, ast.Name):
                    # Add to global refs if it's a global name
                    if n.target.sym and n.target.sym.is_global:
                        result['global_refs'].add(n.target.value)

            # Continue traversing
            for kid in n.kid:
                visit(kid)

        # Start traversal from function body
        if node.body and isinstance(node.body, ast.SubNodeList):
            for stmt in node.body.items:
                visit(stmt)

        return result

    def is_statically_typed(self, node: ast.Ability) -> bool:
        """Check if function has complete type annotations."""
        # Check return type exists
        if not node.signature.return_type:
            return False

        # Check all parameters have type annotations
        # THIS IS NOT NEEDED
        if node.signature.params:
            for param in node.signature.params.items:
                if not param.type_tag:
                    return False

                # Verify the type is a built-in type or arch reference
                param_type = param.type_tag.tag
                if not isinstance(param_type, (ast.BuiltinType, ast.ArchRef)):
                    return False

        return True

    def create_codon_decorator(self, pyvars: Set[str] = None) -> ast.AtomTrailer:
        """Create @codon.jit decorator with optional pyvars."""
        target = ast.Name(
            orig_src=self.ir.source,
            name=Tok.NAME,
            value="codon",
            line=0, end_line=0,
            col_start=0, col_end=0,
            pos_start=0, pos_end=0
        )
        
        jit = ast.Name(
            orig_src=self.ir.source,
            name=Tok.NAME,
            value="jit",
            line=0, end_line=0,
            col_start=0, col_end=0,
            pos_start=0, pos_end=0
        )

        period = ast.Token(
            name=Tok.NAME,
            value=".",
            orig_src=self.ir.source,
            line=0, end_line=0,
            col_start=0, col_end=0,
            pos_start=0, pos_end=0
        )

        base_decorator = ast.AtomTrailer(
            target=target,
            right=jit,
            is_attr=True,
            is_null_ok=False,
            kid=[target, period, jit]
        )

        # If we have pyvars, create a function call with them
        if pyvars:
            pyvar_names = [ast.String(
                orig_src=self.ir.source,
                name=Tok.STRING,
                value=f'"{var}"',
                line=0, end_line=0,
                col_start=0, col_end=0,
                pos_start=0, pos_end=0
            ) for var in pyvars]

            params = ast.SubNodeList(
                items=pyvar_names,
                delim=Tok.COMMA,
                kid=pyvar_names  # Simplified, might need proper token separation
            )

            return ast.FuncCall(
                target=base_decorator,
                params=params,
                genai_call=None,
                kid=[base_decorator, params]
            )

        return base_decorator