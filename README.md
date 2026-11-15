# Falo — Production-Grade Rust Game Engine with First-Class Python

> Rust does the heavy lifting. Python provides the developer experience.

Falo is a modular 2D/3D engine: **wgpu** rendering (WGSL), **Rapier** physics, **Kira** audio, **bevy_ecs**, **PyO3** bindings, and a **multi-platform export** system that turns `uv run main.py --executable game.exe` into a standalone artifact.

## Quick Start

```bash
pip install -e python/          # pure-python fallback; no Rust required
# Optional: Rust acceleration (1.85+)
# https://rustup.rs
pip install maturin && maturin develop

uv run main.py                  # runs demo (headless if no display)
uv run main.py --headless       # force headless
uv run main.py --executable dist/game.exe --release  # Windows exe
```

```python
import falo

game = falo.Game(title="Example", width=1280, height=720, mode="2d")
player = game.scene.create_sprite("assets/player.png")
player.position = (100, 200)

@game.update
def update(dt):
    if falo.keyboard.is_pressed("SPACE"):
        player.move(0, 10)

game.run()
```

3D:

```python
import falo
game = falo.Game(title="3D", width=1920, height=1080, mode="3d")
player = game.scene.load_model("assets/player.glb")
camera = game.scene.create_camera()
camera.position = (0, 3, 8)
game.run()
```

## Build & Export

```bash
uv run falo build --target windows --release          # .exe + portable zip
uv run falo build --target linux --release            # binary
uv run falo build --target linux --format appimage     # AppImage
uv run falo build --target linux --format deb --release
uv run falo build --target macos --release            # .app
uv run falo build --target macos --format dmg         # .dmg
uv run falo build --target android --format apk --release  # .apk
uv run falo build --target ios --release              # .ipa
uv run falo build --target web --release              # WASM + HTML

# Shorthand (same underlying pipeline):
uv run main.py --executable game.exe
uv run main.py --executable game.apk
uv run main.py --executable game.linux
uv run main.py --executable game.app
uv run main.py --executable game.ipa
```

Config via `falo.toml` (see root). Python runtime bundled only when needed; Rust-only games omit it.

## Workspace

```
Cargo.toml (workspace)
crates/falo-*/          # 23 crates: core, math, window, gpu, renderer*, input, ecs, scene, assets, audio, physics...
python/src/falo/        # Python package (Game, Scene, build pipelines)
editor/                 # Standalone editor (egui/wgpu)
examples/               # 2D, 3D, physics, audio, networking, Rust
benchmarks/             # Criterion + Python benches
docs/                   # Guides
```

See `ARCHITECTURE.md` for design and dependency rationale, `DEVELOPMENT_STATUS.md` for feature matrix.

## Features

- **Rendering**: wgpu + WGSL, 2D sprite batching/tilemaps/2D lighting, 3D PBR/IBL/CSM/HDR/tone-mapping, post-processing, hot-reload
- **Physics**: Rapier 2D/3D, fixed timestep, CCD, joints, character controller, debug draw
- **Animation**: clips, state machines, blend trees, root motion, events
- **Particles**: CPU/GPU emitters, pooling
- **Audio**: buses, spatial, mixing in Rust (Kira)
- **ECS**: bevy_ecs abstraction, parallel, bulk Python ops
- **Scene**: hierarchy, prefabs, streaming, RON + binary
- **Assets**: async, handles, caching, hot-reload, packaging
- **UI**: retained, flex, theming
- **Networking**: QUIC/TCP, replication, prediction hooks (optional)
- **Editor**: hierarchy, viewport, inspector, asset browser, profiler
- **Platforms**: Windows, Linux, macOS, Android, iOS, Web (WASM/WebGPU→WebGL2)

## Testing

```bash
pytest python/tests -v
uv run examples/python/basic_game.py --headless
uv run benchmarks/bench_sprite.py
cargo test --workspace  # requires Rust
cargo check --workspace
```

## Performance Targets

| Metric | Target |
|---|---|
| 10k sprites batch | <2ms |
| 100k ECS iter | <0.5ms |
| 1k physics bodies | <1ms |

## License

MIT OR Apache-2.0
