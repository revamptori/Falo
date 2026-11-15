from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class RigidBody:
    mass: float = 1.0
    body_type: str = "dynamic"  # static, dynamic, kinematic
    gravity: Tuple[float,float,float] = (0, -9.81, 0)
    velocity: Tuple[float,float,float] = (0,0,0)

@dataclass
class Collider:
    kind: str = "box"  # box, sphere, capsule, circle, polygon, convex, mesh
    size: Tuple[float,float,float] = (1,1,1)
    radius: float = 0.5

class PhysicsWorld:
    def __init__(self, gravity=(0, -9.81, 0), fixed_dt=1/60.0):
        self.gravity = gravity
        self.fixed_dt = fixed_dt
        self.bodies: List[RigidBody] = []
        print(f"[Physics] world gravity={gravity}")

    def add_body(self, body: RigidBody, collider: Collider):
        self.bodies.append(body)
        print(f"[Physics] add body type={body.body_type} collider={collider.kind}")

    def step(self, dt: float):
        # naive integration placeholder
        for b in self.bodies:
            if b.body_type == "dynamic":
                # apply gravity
                b.velocity = (b.velocity[0] + self.gravity[0]*dt,
                              b.velocity[1] + self.gravity[1]*dt,
                              b.velocity[2] + self.gravity[2]*dt)

    def raycast(self, origin, direction, max_dist=100.0):
        return None
