import time
from typing import Optional, Type
import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.constant import Tokens as Tok

class CodonImportPass(Pass):
    """Adds @codon.jit decorator and codon import."""

    def before_pass(self) -> None:
        """Add codon import before processing."""
        self.codon_imported = False

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
        
        self.codon_imported = True
