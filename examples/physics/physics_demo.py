from falo import Game
import falo
from falo.physics import PhysicsWorld, RigidBody, Collider

game = falo.Game(title="Physics Demo", width=800, height=600, mode="2d")
world = PhysicsWorld(gravity=(0, -9.81, 0))
game.scene.physics = world

# Box collider
body = RigidBody(mass=1.0, body_type="dynamic")
world.add_body(body, Collider(kind="box", size=(1,1,1)))

@game.update
def update(dt):
    world.step(dt)
    print(f"physics bodies={len(world.bodies)} gravity={world.gravity}")

game.run(headless=True, max_frames=3)
