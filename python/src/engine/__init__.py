"""Shim for `import engine as eng` — re-exports falo."""
from falo import *
from falo import __version__
import falo as _falo_mod
import sys
# Ensure `import engine` gives same module as falo
sys.modules["engine"] = sys.modules[__name__]
