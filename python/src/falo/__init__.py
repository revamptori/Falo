"""
Falo Engine — Python API
Rust does the heavy lifting, Python provides the developer experience.
"""

from __future__ import annotations

import sys

# Try to load native extension; fall back to pure python
try:
    from . import _falo as _native  # type: ignore
    HAS_NATIVE = True
except ImportError:
    _native = None  # type: ignore
    HAS_NATIVE = False

from .app import Game
from .scene import Scene, Entity, Camera, Sprite, Model
from .input import keyboard, mouse, gamepad, InputAction, ActionMap
from .assets import AssetServer, Handle
from .math_ext import Vec2, Vec3, Vec4, Mat4
from .window import WindowConfig
from .audio import AudioEngine, Sound
from .physics import PhysicsWorld, RigidBody, Collider
from .animation import AnimationClip, Animator
from .particles import ParticleSystem, ParticleConfig
from .ui import UICanvas, Button, Label
from .network import NetworkServer, NetworkClient
from . import build as build_module

# Re-export commonly used symbols
__version__ = "0.1.0"
__all__ = [
    "Game", "Scene", "Entity", "Camera", "Sprite", "Model",
    "keyboard", "mouse", "gamepad", "InputAction", "ActionMap",
    "AssetServer", "Handle",
    "Vec2", "Vec3", "Vec4", "Mat4",
    "WindowConfig",
    "AudioEngine", "Sound",
    "PhysicsWorld", "RigidBody", "Collider",
    "AnimationClip", "Animator",
    "ParticleSystem", "ParticleConfig",
    "UICanvas", "Button", "Label",
    "NetworkServer", "NetworkClient",
    "HAS_NATIVE",
]

# Intercept --executable for build-on-run
# This allows: `uv run main.py --executable game.exe` to produce a standalone artifact
# without requiring the user's main.py to explicitly handle the flag.
# We do this by inspecting sys.argv at import time, but only acting when Game.run() is called
# via the build interceptor in app.Game._maybe_handle_build_arg().
# We also support `python -m falo build ...` via cli.py.


def _expose_engine_alias():
    """Allow `import engine as eng` as alias (spec example)."""
    if "engine" not in sys.modules:
        sys.modules["engine"] = sys.modules[__name__]

_expose_engine_alias()
