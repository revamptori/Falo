from __future__ import annotations
from typing import Set, Dict, Tuple, List

class InputState:
    def __init__(self):
        self._pressed: Set[str] = set()
        self._just_pressed: Set[str] = set()
        self._just_released: Set[str] = set()
        self._mouse_pos: Tuple[float,float] = (0,0)
        self._mouse_buttons: Set[int] = set()
        self._scroll: float = 0.0

    def is_pressed(self, key: str) -> bool:
        return key.upper() in self._pressed

    def just_pressed(self, key: str) -> bool:
        return key.upper() in self._just_pressed

    def just_released(self, key: str) -> bool:
        return key.upper() in self._just_released

    def press(self, key: str):
        k = key.upper()
        if k not in self._pressed:
            self._just_pressed.add(k)
        self._pressed.add(k)

    def release(self, key: str):
        k = key.upper()
        self._pressed.discard(k)
        self._just_released.add(k)

    def update(self):
        self._just_pressed.clear()
        self._just_released.clear()
        self._scroll = 0.0

    @property
    def mouse_position(self): return self._mouse_pos
    @property
    def scroll(self): return self._scroll

class _GlobalInputProxy:
    """Module-level proxy so users can do `import falo; falo.keyboard.is_pressed(...)`"""
    def __init__(self, kind: str):
        self.kind = kind
        self._state = InputState()

    def is_pressed(self, key: str) -> bool: return self._state.is_pressed(key)
    def just_pressed(self, key: str) -> bool: return self._state.just_pressed(key)
    def just_released(self, key: str) -> bool: return self._state.just_released(key)
    def press(self, key: str): self._state.press(key)
    def release(self, key: str): self._state.release(key)
    @property
    def position(self): return self._state.mouse_position

# global singletons
keyboard = _GlobalInputProxy("keyboard")
mouse = _GlobalInputProxy("mouse")
gamepad = _GlobalInputProxy("gamepad")

# High-level actions
class InputAction:
    def __init__(self, name: str, keys: List[str]):
        self.name = name
        self.keys = [k.upper() for k in keys]

class ActionMap:
    def __init__(self):
        self.actions: Dict[str, InputAction] = {}

    def bind(self, name: str, keys: List[str]):
        self.actions[name] = InputAction(name, keys)

    def is_active(self, name: str, state: InputState) -> bool:
        a = self.actions.get(name)
        if not a: return False
        return any(state.is_pressed(k) for k in a.keys)

InputAction = InputAction
ActionMap = ActionMap
