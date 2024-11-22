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
       import_stmt = ast.Import(
           hint=ast.SubTag(
               tag=ast.Name(
                   orig_src=node.loc.orig_src,
                   name=ast.Tok.NAME.value, 
                   value="py",
                   line=0, end_line=0,
                   col_start=0, col_end=0,
                   pos_start=0, pos_end=0
               ),
               kid=[]
           ),
           
           from_loc=None,
           items=ast.SubNodeList(
               items=[ast.ModulePath(
                   path=[ast.Name(
                       orig_src=node.loc.orig_src,
                       name=ast.Tok.NAME.value,
                       value="codon",
                       line=0, end_line=0, 
                       col_start=0, col_end=0,
                       pos_start=0, pos_end=0
                   )],
                   level=0,
                   alias=None,
                   kid=[]
               )],
               delim=ast.Tok.COMMA,
               kid=[]
           ),
           is_absorb=False,
           kid=[]
       )
       node.body.insert(0, import_stmt)
       self.codon_imported = True

   # Rest of the class implementation remains the same