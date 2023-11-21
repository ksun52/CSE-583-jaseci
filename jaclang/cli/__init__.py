"""CLI for jaclang."""
from jaclang import jac_import as jac_import
from jaclang.jac.plugin.feature import JacFeature

cli = jac_import("cli")
cmds = jac_import("cmds")

cli.cmd_registry = cmds.cmd_reg  # type: ignore


JacFeature.pm.load_setuptools_entrypoints("jac")
