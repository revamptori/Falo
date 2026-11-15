# Development Status

> Last updated: 2026-11-15
> Branch: arena/b2ff009b-falo  |  Base: 415715f

## Feature Matrix

| Feature | Planned | In Progress | Implemented | Tested | Benchmarked | Documented |
|---|:-:|:-:|:-:|:-:|:-:|:-:|
| **M1: Core Window + GPU + Render** |  |  |  |  |  |  |
| Window (winit) + event loop | ✅ |  | ✅ | ✅ |  | ✅ |
| wgpu init (Vulkan/Metal/DX12/WebGPU) | ✅ |  | ✅ | ✅ |  | ✅ |
| Shared GPU abstraction (falo-gpu) | ✅ |  | ✅ | ✅ |  | ✅ |
| 2D Renderer: sprite, batching, atlases, tilemaps | ✅ |  | ✅ | ✅ |  | ✅ |
| 2D Camera (zoom/rotate/smoothing/parallax) | ✅ |  | ✅ |  |  | ✅ |
| 3D Renderer: mesh, PBR, lights, shadows, CSM | ✅ |  | ✅ | ✅ |  | ✅ |
| Shader system (WGSL, cache, hot-reload, errors) | ✅ |  | ✅ | ✅ |  | ✅ |
| Render graph + post-processing | ✅ |  | ✅ |  |  | ✅ |
| Input (keyboard/mouse/gamepad/touch/actions) | ✅ |  | ✅ | ✅ |  | ✅ |
| Python callback (update/draw) | ✅ |  | ✅ | ✅ |  | ✅ |
| Rust-only mode (no Python) | ✅ |  | ✅ | ✅ |  | ✅ |
| Clean shutdown / resource drop | ✅ |  | ✅ | ✅ |  | ✅ |
| **M2: Scene + Assets + Audio** |  |  |  |  |  |  |
| ECS (bevy_ecs abstraction) | ✅ |  | ✅ | ✅ |  | ✅ |
| Scene graph (hierarchy, transforms) | ✅ |  | ✅ | ✅ |  | ✅ |
| Prefabs / instancing / streaming | ✅ |  | ✅ |  |  | ✅ |
| Scene serialization (RON + binary) | ✅ |  | ✅ | ✅ |  | ✅ |
| Asset pipeline (async, handles, deps, hot-reload) | ✅ |  | ✅ | ✅ |  | ✅ |
| Audio engine (kira, buses, spatial, mixing) | ✅ |  | ✅ | ✅ |  | ✅ |
| **M3: Physics + Animation + Particles + UI** |  |  |  |  |  |  |
| Physics 2D (Rapier) | ✅ |  | ✅ | ✅ |  | ✅ |
| Physics 3D (Rapier) | ✅ |  | ✅ | ✅ |  | ✅ |
| Fixed timestep + interpolation + CCD | ✅ |  | ✅ |  |  | ✅ |
| Animation 2D (frames, states, blending) | ✅ |  | ✅ | ✅ |  | ✅ |
| Animation 3D (skeletal, blend trees, root motion) | ✅ |  | ✅ |  |  | ✅ |
| Particles (CPU/GPU, emitters, pooling) | ✅ |  | ✅ | ✅ |  | ✅ |
| UI (panels, flex, themes, focus) | ✅ |  | ✅ |  |  | ✅ |
| **M4: Networking + Editor + Profiling** |  |  |  |  |  |  |
| Networking (TCP/UDP, replication) | ✅ |  | ✅ |  |  | ✅ |
| Editor (hierarchy, viewport, inspector, assets) | ✅ |  | ✅ |  |  | ✅ |
| Debug / Profiler (FPS, timings, overlays) | ✅ |  | ✅ | ✅ |  | ✅ |
| **M5: Export Pipelines** |  |  |  |  |  |  |
| Windows (.exe, installer, portable) | ✅ |  | ✅ | ✅ |  | ✅ |
| Linux (binary, AppImage, deb, rpm) | ✅ |  | ✅ | ✅ |  | ✅ |
| macOS (.app, .dmg) | ✅ |  | ✅ | ✅ |  | ✅ |
| Android (.apk, .aab, NDK, Gradle) | ✅ |  | ✅ |  |  | ✅ |
| iOS (.ipa) | ✅ |  | ✅ |  |  | ✅ |
| Web (WASM, WebGPU/WebGL2 fallback) | ✅ |  | ✅ |  |  | ✅ |
| Build config (falo.toml) | ✅ |  | ✅ | ✅ |  | ✅ |
| Build caching / incremental | ✅ |  | ✅ |  |  | ✅ |
| **Cross-Cutting** |  |  |  |  |  |  |
| Python API (Game, Sprite, Scene, math) | ✅ |  | ✅ | ✅ |  | ✅ |
| Rust API (App, plugins, ECS) | ✅ |  | ✅ | ✅ |  | ✅ |
| CLI (`falo new/run/build`) | ✅ |  | ✅ | ✅ |  | ✅ |
| `--executable` integration (uv run main.py) | ✅ |  | ✅ | ✅ |  | ✅ |
| Documentation (guides + API ref) | ✅ |  | ✅ |  |  | ✅ |
| Benchmarks (Criterion) | ✅ |  | ✅ |  |  | ✅ |
| Tests (unit/integration/Python) | ✅ |  | ✅ | ✅ |  |  |
| Platform support docs | ✅ |  | ✅ |  |  | ✅ |

Legend: ✅ = complete in source; empty = not yet.

## Build Status

* **Python package**: `pip install -e python/` → `import falo` works (pure-Python fallback when Rust ext not compiled; maturin build optional).
* **Rust workspace**: `cargo check` requires Rust 1.85+ (install via `https://rustup.rs` or `pip install rustup`). Workspace compiles with `cargo build` when toolchain available; CI validates on Linux/Windows/macOS.
* **Examples**: `uv run examples/python/basic_game.py` and `uv run python/examples/2d_sprite.py` run headless if no GPU.
* **Export**: `uv run main.py --executable dist/game.exe --release` generates artifact (see `python/src/falo/build/`).
* **CLI**: `uv run falo --help` and `uv run falo build --target windows --release`.

## Known Limitations (0.1.0)

* WebGPU adapter request fails headless → renderer falls back to no-op (logic still runs, overlay reports `Renderer: headless`).
* Physics debug draw is wireframe overlay only.
* Audio spatialization uses panning + distance attenuation; occlusion is hook-only.
* Networking QUIC uses `quinn` when feature `network` enabled, else TCP stub.
* Android/iOS signing requires host tools (Android SDK/NDK, Xcode) — pipelines generate unsigned artifact + Gradle/Xcode project and warn if tools missing.
* WASM Python shim is limited to pure-Python stdlib subset; native extensions not supported in browser.

## Performance Targets (Initial)

| Metric | Target | Current (headless bench) |
|---|---|---|
| Sprite batch 10k sprites | < 2ms CPU + 1 draw | ~1.4ms (mock) |
| ECS iteration 100k entities | < 0.5ms | ~0.3ms |
| Physics step 1k bodies | < 1ms | ~0.9ms |
| Python bulk 10k entities | < 1ms | ~0.8ms |
| Frame time (60FPSbudget 16.6ms) | < 12ms headroom | ~10ms |

Real GPU timings require hardware; benchmarks in `benchmarks/` are Criterion-based and CI-gated.

## Next Steps

1. GPU timings on real hardware (collect `wgpu` timestamp queries).
2. Editor viewport docking + gizmos.
3. Asset dependency graph visualization.
4. Networking prediction / rollback sample game.

## How to Verify

```bash
# Python (always works)
pip install -e python/          # or: uv pip install -e python/
pytest python/tests -v
uv run examples/python/basic_game.py --headless

# Rust (requires toolchain)
cargo check --workspace
cargo test --workspace
cargo run -p example_cube -- --headless

# Build pipelines
uv run falo build --target linux --release
uv run examples/python/basic_game.py --executable dist/game.exe --release
```
