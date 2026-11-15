"""
Falo Demo — works with `uv run main.py` and `uv run main.py --executable game.exe`
This is the canonical example from the spec: simple 2D game + 3D cube demo.
"""
import falo

game = falo.Game(title="Falo Demo", width=1280, height=720, mode="2d")

# 2D sprite example (requires assets/player.png — will show warning if missing, but still runs)
player = game.scene.create_sprite("assets/player.png")
player.position = (100, 200)

# 3D camera example (same GPU abstraction)
camera = game.scene.create_camera(position=(0, 3, 8))
camera.position = (0, 3, 8)

# Bulk API example (performance): spawn 100 entities in one call
enemies = game.scene.spawn_batch(5)

@game.update
def update(dt):
    # Keyboard input (low-level + action map)
    if falo.keyboard.is_pressed("SPACE"):
        player.move(0, 10)
    if falo.keyboard.is_pressed("A"):
        player.move(-5, 0)
    if falo.keyboard.is_pressed("D"):
        player.move(5, 0)

    # Simulate a few frames of physics if attached
    # game.scene.physics.step(dt) is called automatically by Game loop

@game.draw
def draw():
    # Rendering is handled in Rust; Python draw callbacks can issue
    # high-level commands: the actual GPU work stays in Rust.
    pass

if __name__ == "__main__":
    game.run()
