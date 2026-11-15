from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Any
import os

@dataclass
class Sprite:
    path: str
    position: Tuple[float, float] = (0.0, 0.0)
    rotation: float = 0.0
    scale: Tuple[float, float] = (1.0, 1.0)
    color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    layer: int = 0
    visible: bool = True

    def move(self, dx: float, dy: float):
        self.position = (self.position[0] + dx, self.position[1] + dy)

@dataclass
class Model:
    path: str
    position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    scale: Tuple[float, float, float] = (1.0, 1.0, 1.0)

@dataclass
class Camera:
    position: Tuple[float, float, float] = (0.0, 3.0, 8.0)
    target: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    fov: float = 45.0
    near: float = 0.1
    far: float = 1000.0
    # 2D
    zoom: float = 1.0
    rotation: float = 0.0

    def look_at(self, pos, target=None):
        self.position = tuple(pos) if len(pos)==3 else (pos[0], pos[1], self.position[2])
        if target: self.target = tuple(target)

@dataclass
class Entity:
    id: int
    name: str
    transform: Dict[str, Any] = field(default_factory=dict)
    components: Dict[str, Any] = field(default_factory=dict)

    def add_component(self, key, value):
        self.components[key] = value

class Scene:
    def __init__(self, mode: str = "2d", width: int = 1280, height: int = 720):
        self.mode = mode
        self.width = width
        self.height = height
        self.sprites: List[Sprite] = []
        self.models: List[Model] = []
        self.entities: List[Entity] = []
        self.cameras: List[Camera] = []
        self._next_id = 1
        # physics placeholder
        self.physics = None
        self.active_camera: Optional[Camera] = None

    # Sprite API
    def create_sprite(self, path: str, position=(0,0)) -> Sprite:
        s = Sprite(path=path, position=position)
        self.sprites.append(s)
        return s

    def load_model(self, path: str) -> Model:
        m = Model(path=path)
        self.models.append(m)
        return m

    def create_camera(self, **kwargs) -> Camera:
        c = Camera(**kwargs)
        self.cameras.append(c)
        self.active_camera = c
        return c

    def create_entity(self, name: str = "Entity") -> Entity:
        e = Entity(id=self._next_id, name=name)
        self._next_id += 1
        self.entities.append(e)
        return e

    def spawn_batch(self, count: int, prototype: Optional[Entity] = None) -> List[Entity]:
        batch = []
        for i in range(count):
            e = self.create_entity(name=f"{prototype.name if prototype else 'Entity'}_{i}")
            batch.append(e)
        return batch

    # Bulk API for performance (avoid per-entity python calls)
    def query_positions(self) -> List[Tuple[float,float]]:
        return [s.position for s in self.sprites]

    def set_positions_bulk(self, positions: List[Tuple[float,float]]):
        for s, pos in zip(self.sprites, positions):
            s.position = tuple(pos)

    # Serialization
    def to_dict(self):
        return {"mode": self.mode, "sprites": [s.__dict__ for s in self.sprites], "models": [m.__dict__ for m in self.models]}

    def load(self, path: str):
        # load gltf or image verification
        if not os.path.exists(path):
            print(f"[Falo::Scene] asset not found: {path}")
        return path
