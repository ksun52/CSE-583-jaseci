from __future__ import annotations
from jaclang import jac_import as __jac_import__
import typing as _jac_typ
if _jac_typ.TYPE_CHECKING:
    import codon
else:
    codon, = __jac_import__(target='codon', base_path=__file__, lng='py', absorb=False, mdl_alias=None, items={})

def sum(a: int, b: int) -> int:
    return a + b