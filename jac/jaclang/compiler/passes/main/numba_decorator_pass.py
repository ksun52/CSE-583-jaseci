import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.constant import Tokens as Tok


class NumbaDecoratorPass(Pass):
    """
    Adds @numba.jit decorator to all functions and adds numba import to file.
    The numba decorator will jit functions automatically when applicable.
    """

    def enter_module(self, node: ast.Module) -> None:
        """Add import:py numba; statement."""

        tag=ast.Name(
                    orig_src=self.ir.source,
                    name=ast.Tok.NAME, 
                    value="py",
                    line=0, end_line=0,
                    col_start=0, col_end=0,
                    pos_start=0, pos_end=0
                )

        numba=ast.Name(
                    orig_src=self.ir.source,
                    name=Tok.NAME,
                    value="numba",
                    line=0, end_line=0, 
                    col_start=0, col_end=0,
                    pos_start=0, pos_end=0
                )

        modulePath=ast.ModulePath(
                    path=[numba],
                    level=0,
                    alias=None,
                    kid=[numba]
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


    def enter_ability(self, node: ast.Ability) -> None:
        """Process each ability node."""
        numba_decorator = self.create_numba_decorator()

        if not node.decorators:
            node.decorators = ast.SubNodeList(
                items=[numba_decorator],
                delim=Tok.DECOR_OP, 
                kid=[node.gen_token(Tok.DECOR_OP), numba_decorator]
            )

            node.add_kids_left([node.decorators]) # add decorators to tree
        else:
            node.decorators.items.insert(0, numba_decorator)
            node.decorators.add_kids_left([node.gen_token(Tok.DECOR_OP), numba_decorator])


    def create_numba_decorator(self) -> ast.AtomTrailer:
        """Create @numba.jit decorator."""
        target=ast.Name(
                orig_src=self.ir.source,
                name=Tok.NAME,
                value="numba",
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
        return  ast.AtomTrailer(
            target=target,
            right=right,
            is_attr=True,
            is_null_ok=False,
            kid=[target, period, right]
        )
