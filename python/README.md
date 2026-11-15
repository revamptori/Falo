# Falo Python Package

Python bindings for the Falo engine. Works in two modes:

* **Native (Rust)**: when `falo._falo` extension is compiled via `maturin develop`, heavy lifting is in Rust (rendering, physics, audio...).
* **Pure-Python fallback**: when extension not present (e.g., CI without Rust toolchain), the engine runs with Python implementations of the same API — useful for logic testing and headless builds.

## Install

```bash
pip install -e python/
# with Rust (requires Rust 1.85+)
pip install maturin
maturin develop --manifest-path Cargo.toml
```

## Quick start

```python
import falo

game = falo.Game(title="Hello", width=1280, height=720, mode="2d")
player = game.scene.create_sprite("assets/player.png")
player.position = (100, 200)

@game.update
def update(dt):
    if falo.keyboard.is_pressed("SPACE"):
        player.move(0, 10)

game.run()
```

## Build standalone

```bash
uv run main.py --executable dist/game.exe --release
uv run falo build --target windows --release
uv run falo build --target android --format apk --release
```

See `../../ARCHITECTURE.md` and `../../docs/`.
