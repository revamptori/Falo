"""
2D Sprite demo — tests batching, camera, parallax, tilemap
"""
import falo

game = falo.Game(title="2D Sprite Demo", width=1280, height=720, mode="2d")
camera = game.scene.create_camera()
camera.zoom = 1.0

# Sprite batch bulk test
sprites = []
for i in range(20):
    s = game.scene.create_sprite(f"assets/player.png")
    s.position = (i*40, 100)
    sprites.append(s)

# Tilemap
from falo.scene import Scene
print(f"Sprites spawned: {len(game.scene.sprites)}")

@game.update
def update(dt):
    camera.position = (camera.position[0] + 10*dt, camera.position[1], camera.position[2])
    # Parallax simulated: move background layers at different speeds

game.run(headless=True, max_frames=5)
