from dataclasses import dataclass

@dataclass
class AnimationClip:
    name: str
    duration: float
    looped: bool = True
    frames: int = 24

class Animator:
    def __init__(self):
        self.current: str | None = None
        self.time: float = 0.0
        self.speed: float = 1.0

    def play(self, name: str):
        self.current = name
        self.time = 0.0
        print(f"[Animator] play {name}")

    def update(self, dt: float):
        self.time += dt * self.speed
