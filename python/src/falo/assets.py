from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Dict, Any, Optional
from pathlib import Path

class Handle:
    def __init__(self, id: int, path: str, kind: str):
        self.id = id
        self.path = path
        self.kind = kind
    def __repr__(self): return f"Handle({self.kind}:{self.id} {self.path})"

class AssetServer:
    def __init__(self, hot_reload: bool = False):
        self.hot_reload = hot_reload
        self._next = 1
        self._handles: Dict[int, Handle] = {}
        self._states: Dict[int, str] = {}

    def load(self, path: str, kind: str = "auto") -> Handle:
        h = Handle(self._next, path, kind)
        self._next += 1
        # immediate ready if exists, else loading
        exists = Path(path).exists()
        self._states[h.id] = "Ready" if exists else "Loading"
        self._handles[h.id] = h
        print(f"[AssetServer] load {path} -> {h} ({self._states[h.id]})")
        if not exists:
            print(f"  ⚠ asset missing on disk: {path}")
        return h

    def state(self, handle: Handle) -> str:
        return self._states.get(handle.id, "Failed")

# global default
default_server = AssetServer()
