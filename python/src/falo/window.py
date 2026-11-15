from dataclasses import dataclass

@dataclass
class WindowConfig:
    title: str = "Falo Game"
    width: int = 1280
    height: int = 720
    resizable: bool = True
    fullscreen: bool = False
    vsync: bool = True
