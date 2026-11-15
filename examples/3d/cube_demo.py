"""
3D Cube demo — PBR cube, lights, camera, same GPU abstraction as 2D
"""
import falo

game = falo.Game(title="3D Cube Demo", width=1920, height=1080, mode="3d")

# Load model (cube mesh)
cube = game.scene.load_model("assets/player.glb")
cube.position = (0, 0, 0)

# Camera
cam = game.scene.create_camera(position=(0, 3, 8), target=(0,0,0))

# Simulate Rust 3D renderer: log PBR material
print(f"3D mesh loaded: {cube.path} at {cube.position}")
print(f"Camera fov={cam.fov} pos={cam.position}")

@game.update
def update(dt):
    # Rotate cube
    cube.rotation = (cube.rotation[0], cube.rotation[1] + 45*dt, cube.rotation[2])

game.run(headless=True, max_frames=5)
