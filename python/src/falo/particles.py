from dataclasses import dataclass

@dataclass
class ParticleConfig:
    rate: float = 100.0
    lifetime: float = 2.0
    velocity: tuple = (0,5,0)
    gravity: tuple = (0,-9.81,0)
    color_start: tuple = (1,1,1,1)
    color_end: tuple = (1,1,1,0)
    size_start: float = 1.0
    size_end: float = 0.0

class ParticleSystem:
    def __init__(self, config: ParticleConfig = None):
        self.config = config or ParticleConfig()
        self.alive = 0
        self.max_particles = 10000

    def emit(self, count: int):
        self.alive = min(self.alive + count, self.max_particles)

    def burst(self, count: int): self.emit(count)

    def update(self, dt: float): pass
