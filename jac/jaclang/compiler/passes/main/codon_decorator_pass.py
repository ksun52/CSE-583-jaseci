import time
from typing import Optional, Type, Set
import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.constant import Tokens as Tok


class CodonDecoratorPass(Pass):
    """Adds @codon.jit decorator to statically typed functions."""

    def before_pass(self) -> None:
        """Initialize collections for global references."""
        self.module_globals: Set[str] = set()  # Track all global names in module

    def enter_module(self, node: ast.Module) -> None:
        """Add import:py codon statement."""
        tag=ast.Name(
                    orig_src=self.ir.source,
                    name=ast.Tok.NAME, 
                    value="py",
                    line=0, end_line=0,
                    col_start=0, col_end=0,
                    pos_start=0, pos_end=0
                )

        codon=ast.Name(
                    orig_src=self.ir.source,
                    name=Tok.NAME,
                    value="codon",
                    line=0, end_line=0, 
                    col_start=0, col_end=0,
                    pos_start=0, pos_end=0
                )

        modulePath=ast.ModulePath(
                    path=[codon],
                    level=0,
                    alias=None,
                    kid=[codon]
                )

        subnodeList=ast.SubNodeList(
                items=[modulePath],
                delim=Tok.COMMA,
                kid=[modulePath]
            )

        subtag=ast.SubTag(
                tag=tag,
                kid=[node.gen_token(Tok.COLON), tag]
            )

        semi = ast.Semi(
            orig_src=self.ir.source,
            name=Tok.SEMI,
            value=";",
            line=0, end_line=0,
            col_start=0, col_end=0,
            pos_start=0, pos_end=0
        )

        import_stmt = ast.Import(
            hint=subtag,
            from_loc=None,
            items=subnodeList,
            is_absorb=False,
            kid=[node.gen_token(Tok.KW_IMPORT), subtag, subnodeList, semi]
        )

        node.body.insert(0, import_stmt)
        node.add_kids_left([import_stmt])

        """Collect all global names defined in the module."""
        for item in node.body:
            if isinstance(item, ast.GlobalVars):
                # Add global variable names
                for assignment in item.assignments.items:
                    if isinstance(assignment.target, ast.SubNodeList):
                        for target in assignment.target.items:
                            if isinstance(target, ast.Name):
                                self.module_globals.add(target.value)
            elif isinstance(item, ast.Ability):
                # Add global function names
                if isinstance(item.name_ref, ast.Name):
                    self.module_globals.add(item.name_ref.value)


    def enter_ability(self, node: ast.Ability) -> None:
        """Process each ability node."""
        # Skip if function is part of an architype
        if isinstance(node.parent.parent, ast.Architype):
            return
        
        # Collect information about function scope -------------------------------------
        # Analyze scope
        scope_info = self.analyze_function_scope(node)
        if not scope_info['is_eligible']:
            return
        # ------------------------------------------------------------------------------

        if scope_info['global_refs']:
            codon_decorator = self.create_codon_decorator(scope_info['global_refs'])
        else:
            codon_decorator = self.create_codon_decorator()

        if not node.decorators:

            node.decorators = ast.SubNodeList(
                items=[codon_decorator], # adds to py file
                delim=Tok.DECOR_OP, 
                kid=[node.gen_token(Tok.DECOR_OP), codon_decorator] #
            )

            node.add_kids_left([node.decorators]) # add decorators to tree
        else:
            node.decorators.items.insert(0, codon_decorator)
            node.decorators.add_kids_left([node.gen_token(Tok.DECOR_OP), codon_decorator])


    def analyze_function_scope(self, node: ast.Ability) -> dict:
        """Analyze function scope to find all external references."""
        result = {
            'is_eligible': True,
            'global_refs': set(),
            'writes_nonlocal': False
        }

        def visit(n: ast.AstNode) -> None:
            if isinstance(n, ast.Assignment):
                # Check if assignment modifies anything non-local
                for target in n.kid:
                    if isinstance(target, ast.AtomTrailer):
                        result['writes_nonlocal'] = True
                        return
                    if isinstance(target, ast.SubNodeList):
                        for target_child in target.kid:
                            if isinstance(target_child, ast.Name) and target_child.value in self.module_globals:
                                result['writes_nonlocal'] = True
                                return
                    
            # ADD GLOBAL ASSIGNMENT

            elif isinstance(n, ast.Name):
                # Track global names used
                if n.value in self.module_globals:
                    result['global_refs'].add(n.value)
                # Check if it's an imported name
                elif n.sym and n.sym.decl and isinstance(n.sym.decl, ast.ModuleItem):
                    result['global_refs'].add(n.value)

            elif isinstance(n, ast.AtomTrailer):
                # Handle module attribute access (e.g., math.sqrt)
                if isinstance(n.target, ast.Name):
                    if n.target.sym and n.target.sym.decl and isinstance(n.target.sym.decl, (ast.ModulePath, ast.ModuleItem)):
                        result['global_refs'].add(n.target.value)
                    elif n.target.value in self.module_globals:
                        result['global_refs'].add(n.target.value)

            # Recurse through children
            for kid in n.kid:
                visit(kid)

        # Analyze function body
        if node.body and isinstance(node.body, ast.SubNodeList):
            for stmt in node.body.items:
                visit(stmt)

        # If function writes to non-local variables, mark as ineligible
        if result['writes_nonlocal']:
            result['is_eligible'] = False

        return result


    def create_codon_decorator(self, pyvars: Set[str] =None) -> ast.AtomTrailer:
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
        
        atomTrailer=ast.AtomTrailer(
                target=target,
                right=right,
                is_attr=True,
                is_null_ok=False,
                kid=[target, period, right]
            )
        if not pyvars:
            return atomTrailer
        
        pyvar_strings = [
            ast.MultiString(
                strings=[ast.String(
                    orig_src=self.ir.source,
                    name=Tok.STRING,
                    value=f'"{var}"',
                    line=0, end_line=0,
                    col_start=0, col_end=0,
                    pos_start=0, pos_end=0
                )],
                kid=[ast.String(
                    orig_src=self.ir.source,
                    name=Tok.STRING,
                    value=f'"{var}"',
                    line=0, end_line=0,
                    col_start=0, col_end=0,
                    pos_start=0, pos_end=0
                )]
            ) for var in sorted(pyvars)  # Sort for consistent ordering
        ]
        pyvar_strings_commas = []
        for var in pyvar_strings:
            pyvar_strings_commas.append(var)
            
        # Create the parameters list
        params = ast.SubNodeList(
            items=pyvar_strings_commas,
            delim=Tok.COMMA,
            kid=pyvar_strings_commas
        )

        left_bracket = ast.Token(
            name=ast.Tok.LSQUARE,
            value="[",
            orig_src=self.ir.source,
            line=0, end_line=0,
            col_start=0, col_end=0,
            pos_start=0, pos_end=0
        )

        right_bracket = ast.Token(
            name=ast.Tok.RSQUARE,
            value="]",
            orig_src=self.ir.source,
            line=0, end_line=0,
            col_start=0, col_end=0,
            pos_start=0, pos_end=0
        )

        # Create the ListVal
        list_val = ast.ListVal(
            values=params,
            kid=[left_bracket, params, right_bracket]
        )

        pyvars_name =ast.Name(
            orig_src=self.ir.source, 
            name=Tok.NAME,
            value="pyvars",
            line=0, end_line=0,
            col_start=0, col_end=0,
            pos_start=0, pos_end=0
        )

        # Create the equals token
        equals_token = ast.Token(
            name=ast.Tok.EQ,
            value="=",
            orig_src=self.ir.source,
            line=0, end_line=0,
            col_start=0, col_end=0,
            pos_start=0, pos_end=0
        )

        kw_pair = ast.KWPair(
            key=pyvars_name,
            value=list_val,
            kid=[pyvars_name, equals_token, list_val]
        )

        kw_pair = ast.SubNodeList(
            items=[kw_pair],
            delim=None,
            kid=[kw_pair]
        )
        
        open_paren = ast.Token(
            name=ast.Tok.LPAREN,
            value="(",
            orig_src=self.ir.source,
            line=0, end_line=0,
            col_start=0, col_end=0,
            pos_start=0, pos_end=0
        )

        close_paren = ast.Token(
            name=ast.Tok.RPAREN,
            value=")",
            orig_src=self.ir.source,
            line=0, end_line=0,
            col_start=0, col_end=0,
            pos_start=0, pos_end=0
        )

        func_call = ast.FuncCall(
            target=atomTrailer,
            params=kw_pair,
            genai_call=None,
            kid=[atomTrailer, open_paren, kw_pair, close_paren]
        )

        return func_call