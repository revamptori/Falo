# Python API

```python
import falo
game = falo.Game(title, width, height, mode="2d"|"3d")
sprite = game.scene.create_sprite(path)
model = game.scene.load_model(path)
camera = game.scene.create_camera()
game.scene.spawn_batch(count)

@game.update
def update(dt): ...

@game.draw
def draw(): ...

game.run()
```

Modules: `falo.input`, `falo.assets`, `falo.physics`, `falo.audio`, `falo.animation`, `falo.particles`, `falo.ui`, `falo.network`.

Type stubs in `python/src/falo/_falo.pyi`.
