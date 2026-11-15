# Falo Engine — Architecture

> Version 0.1.0  |  Status: Active Development  |  Rust 1.85+ (MSRV)  |  Python 3.9+

## 1. Philosophy

**RUST DOES THE HEAVY LIFTING. PYTHON PROVIDES THE DEVELOPER EXPERIENCE.**

Every hot path — rendering, physics, audio mixing, animation, particles, asset decoding, ECS scheduling, culling, networking — executes in Rust. Python is an optional scripting layer that orchestrates high-level gameplay via bulk, cache-friendly APIs. The GIL is released during long-running native work; no Python references are held in audio callbacks; the boundary is crossed in batches, not per-particle.

```
┌─────────────────────────────────────────────────────┐
│                  Python Game Script                 │
│   Game, Scene, Entities, Events, UI, Input Actions  │
├──────────────────────┬──────────────────────────────┤
│  PyO3 Bridge (falo-python)  │  Native Rust Game    │
│  Type stubs, bulk ops, GIL release, error mapping  │
├──────────────────────┴──────────────────────────────┤
│  Engine Runtime (falo-runtime)                      │
│  GameLoop, Scheduler, Time, fixed-timestep, plugins │
├─────────────────────────────────────────────────────┤
│  Core Modules (all Rust-native)                     │
│  Renderer │ Physics │ Audio │ Assets │ ECS │ Scene │
│  Animation│ Particles│ UI │ Input │ Network │ Math │
├─────────────────────────────────────────────────────┤
│  Platform Abstraction (falo-window, falo-gpu)       │
│  winit + wgpu (Vulkan/Metal/DX12/WebGPU)            │
└─────────────────────────────────────────────────────┘
```

## 2. Workspace Layout

```
Falo/
├── Cargo.toml                  # Workspace root, shared dependencies, profiles
├── crates/
│   ├── falo-core/              # Time, logging, plugin trait, app builder
│   ├── falo-math/              # glam re-export + engine math helpers
│   ├── falo-window/            # winit wrapper, window config, events
│   ├── falo-gpu/               # wgpu device, queues, resource caching
│   ├── falo-renderer/          # Render graph, passes, GPU resource mgmt
│   ├── falo-renderer-2d/       # Sprites, tilemaps, batching, 2D lighting
│   ├── falo-renderer-3d/       # Meshes, PBR, lights, shadows, skybox
│   ├── falo-input/             # Keyboard, mouse, gamepad, action map
│   ├── falo-ecs/               # ECS abstraction over bevy_ecs
│   ├── falo-scene/             # Scene graph, transforms, prefabs, streaming
│   ├── falo-assets/            # Handles, async loading, hot-reload, cache
│   ├── falo-audio/             # Kira backend, buses, spatial audio
│   ├── falo-physics/           # Rapier2D/3D integration, fixed step
│   ├── falo-animation/         # Clips, state machines, blending, events
│   ├── falo-particles/         # CPU & GPU emitters, pooling
│   ├── falo-ui/                # Retained UI, flex layout, theming
│   ├── falo-network/           # TCP/UDP, replication, prediction hooks
│   ├── falo-serialization/     # RON + serde, scene format
│   ├── falo-debug/             # FPS, draw-call stats, overlays
│   ├── falo-profiler/          # CPU/GPU timings, Tracy integration
│   ├── falo-scripting/         # Script host trait (Python + future Lua)
│   ├── falo-python/            # PyO3 bindings, bulk APIs, GIL discipline
│   ├── falo-editor/            # Editor app (egui/wgpu), separate binary
│   └── falo-cli/               # Build, export, packaging pipelines
├── python/
│   ├── pyproject.toml
│   └── src/falo/
│       ├── __init__.py         # Public Python API (Game, Sprite, Scene…)
│       ├── _falo.pyi           # Type stubs
│       ├── app.py              # Game class, main loop
│       ├── input.py            # Keyboard, Mouse, Gamepad
│       ├── assets.py           # Asset handles
│       ├── scene.py            # Scene, Entity, Camera
│       ├── math_ext.py         # Vec2/3 wrappers
│       ├── build/              # Export pipelines
│       └── cli.py              # `falo build` + --executable handling
├── editor/                     # Editor frontend
├── examples/                   # Rust + Python examples
├── benchmarks/                 # Criterion suites
├── tests/                      # Integration tests
└── docs/                       # Guides + API reference
```

### Dependency Rules

* `falo-core` has no renderer/physics dependencies.
* `falo-gpu` owns `wgpu` Device/Queue; no crate creates its own.
* `falo-renderer` depends on `falo-gpu` and `falo-assets`; 2D/3D crates depend on it.
* `falo-scene` depends on `falo-ecs` + `falo-math`; not the reverse.
* `falo-python` is leaf; nothing depends on it. Rust-only games omit it.
* `falo-editor` is leaf; runtime crates never depend on editor.
* Circular dependencies are forbidden; enforced via workspace `cargo deny`.

## 3. Technology Selection (Pinned)

| Concern | Crate | Version | Rationale |
|---|---|---|---|
| windowing | `winit` | 0.30 | Active, cross-platform, web support |
| graphics | `wgpu` | 0.20+ | Vulkan/Metal/DX12/WebGPU unified |
| math | `glam` | 0.28 | SIMD, Bevy-compatible |
| ECS | `bevy_ecs` | 0.14 | Mature, parallel, change detection |
| physics 2D/3D | `rapier2d`, `rapier3d` | 0.23 | Deterministic, maintained |
| audio | `kira` | 0.9 | Streaming, buses, low-latency |
| serialization | `serde`, `ron`, `rmp-serde` | - | Human + binary scene formats |
| images | `image` | 0.25 | PNG/JPEG/WebP/HDR |
| glTF | `gltf` | 1.4 | Standard model pipeline |
| compression | `lz4_flex`, `zstd` | - | Asset packaging |
| Python | `pyo3` 0.22 | `maturin` 1.7 | Stable, GIL control |
| UI (editor) | `egui` | 0.28 | Retained, wgpu backend |
| networking | `quinn`, `tokio` (optional) | - | UDP reliable/unreliable |

All versions pinned in workspace `Cargo.toml` `[workspace.dependencies]`.

## 4. Runtime & Game Loop

```
startup() -> load assets (async) -> enter GameLoop
GameLoop (60Hz default, configurable):
  ┌─ accumulator += dt
  ├─ while accumulator >= fixed_dt:
  │    ├─ input.process()
  │    ├─ physics.step(fixed_dt)     // Rapier, interpolation
  │    ├─ scripts.update()
  │    └─ accumulator -= fixed_dt
  ├─ animation.evaluate(alpha)
  ├─ particles.simulate(dt)
  ├─ ecs.schedule.run()
  ├─ culling + render_graph.execute()
  └─ audio.mix()
```

* Fixed-timestep physics for determinism; variable rendering with interpolation.
* `falo-core::App` is plugin-based: `App::new().add_plugin(RendererPlugin).add_plugin(PhysicsPlugin).run()`.

## 5. Rendering

### GPU Abstraction (`falo-gpu`)
Owns `Instance`, `Adapter`, `Device`, `Queue`, `Surface`. Provides:
* Resource caches (Buffer, Texture, Sampler, BindGroup) with LRU eviction.
* Staging belt, command encoder pooling.
* Feature detection + fallback (WebGL2 on web, no compute).

### Render Graph (`falo-renderer`)
DAG of `RenderPass` nodes (shadow → opaque → transparent → post → UI). Each pass declares resources; graph does culling, sorting, submission in one encoder per frame. Post-processing is chain of fullscreen passes (bloom, AO, color grading, vignette).

### 2D (`falo-renderer-2d`)
* Sprite batching by material → single draw per atlas page.
* Texture atlases (auto-packing), sprite sheets, tilemaps (chunked, frustum-culling).
* Cameras with zoom/rotation/smoothing; parallax; layers; blend modes.
* 2D lighting + normal maps + shadows via signed-distance.

### 3D (`falo-renderer-3d`)
* PBR (metallic-roughness), directional/point/spot lights, IBL/HDR, tone mapping.
* Shadow mapping + CSM for directional lights.
* Instanced & batched draws; frustum + occlusion culling; LOD; vegetation instancing.
* Skeletal skinning + morph targets on GPU.

### Shaders
WGSL only. `falo-renderer::ShaderCache` validates, naga-compiles, hot-reloads on file change (dev), errors reported with line/col.

## 6. Scene & Transforms

Hierarchical scene graph stored as ECS entities with `Transform` (local) → `GlobalTransform` propagated topologically. Dirty-flag propagation avoids full traversal when static. Prefabs are serialized entity subtrees with overrides; instancing is cheap clone + handle dedup.

Scenes are `RON` files + binary `rmp` for runtime. Streaming via `SceneLoader` async task; references resolved by `AssetHandles`.

## 7. Physics

Rapier integration, one `PhysicsWorld` per scene (2D or 3D, not mixed per entity). Components: `RigidBody`, `Collider`, `Joint`, `CharacterController`. Systems: broadphase (SAP), narrowphase, solver, CCD, sleeping. Fixed step + interpolation. Debug draw via `falo-debug`.

## 8. Audio

`falo-audio` owns `kira::AudioManager`. Buses (master → music/sfx) with volume/pitch/filters. Spatial audio: 3D attenuation, panning, occlusion hooks. All mixing in Rust; Python only enqueues `play(sound, volume, spatial)`.

## 9. ECS

Thin wrapper over `bevy_ecs`:

```rust
World::new();
world.spawn((Transform::default(), SpriteBundle { .. }));
world.query::<(&Transform, &mut Velocity)>().par_iter();
world.resource_mut::<Time>().delta_seconds();
```

Exposes `Commands` (deferred), `Events`, `Resources`, `Schedule` (staged, parallel). Python sees `Scene.create_entity()` that returns handle; bulk ops: `scene.spawn_batch(count, components)`.

## 10. Python Bridge

* PyO3 `#[pyclass]` only for handles (Entity, AssetHandle), not per-particle data.
* Bulk APIs: `scene.query_positions(ids) -> np.ndarray` not `entity.position` in loop.
* Errors: Rust `anyhow` → Python `FaloError` with context.
* GIL: `py.allow_threads(|| heavy_work())`; never hold Py reference in audio thread.
* Type stubs `python/src/falo/_falo.pyi` for autocomplete.
* Rust-only games: `cargo add falo-core` without `falo-python` feature.

## 11. Assets

`AssetServer` with `Handle<T>` (generational index). States: Loading → Ready | Failed. Async via `tokio`-lite or `smol` pool; main thread only inserts ready assets. Dependency tracking (material → texture). Hot reload (dev): file watcher → reimport → patch handles. Packaging: manifest `assets.manifest` + compressed blobs; loading from zip in exported builds.

Supported: PNG/JPEG/WebP/HDR, glTF/GLB, WAV/OGG/FLAC, TTF/OTF, WGSL, RON scenes.

## 12. Animation & Particles

Animation: clip sampling in Rust, state machine with transitions/blend trees, root motion extraction, events fire as ECS events.

Particles: emitters are components; simulation is compute-like batch in Rust (SoA, pooling). Python only configures `ParticleSystem { rate, lifetime, velocity, color_curve }`.

## 13. UI

Retained widgets (`Panel`, `Button`, `Slider`…) with flex layout, anchors, theme, focus. Rendering is 2D pass (screen-space). Input routing: UI consumes events before gameplay. Editor UI is separate (egui) to keep runtime light.

## 14. Networking

Optional `falo-network` crate: Quinn (QUIC/UDP) + TCP fallback. Concepts: `Replicated` component, `NetworkServer`/`NetworkClient` resources, reliable vs unreliable channels, snapshot interpolation, prediction hooks, bandwidth stats. Not in default features.

## 15. Editor & CLI

Editor (`falo-editor` binary): winit + egui + engine runtime embedded → hierarchy, viewport (2D/3D), inspector, asset browser, play/pause/step, profiler overlay. Uses same scene format.

CLI (`falo-cli`): `falo new`, `falo run`, `falo build --target windows|linux|macos|android|ios|web`. Backed by `python/src/falo/build/` pipelines (same code invoked via `Game --executable`). Build cache keyed by engine version + target + features + Python ABI.

## 16. Export / Packaging

* **Desktop** (Windows exe, Linux binary/AppImage/deb/rpm, macOS .app/dmg): compile Rust with target toolchain, bundle `assets.pak` + Python runtime if needed, code-sign where configured.
* **Mobile** (APK/AAB, IPA): Gradle/Xcode project gen, NDK cross-compile, lifecycle (pause/resume), touch.
* **Web** (WASM): `wasm-bindgen` + WebGPU → WebGL2 fallback, HTML launcher, asset fetch, audio via WebAudio.

Rust-only builds omit Python runtime; hybrid builds embed CPython (desktop/mobile) or use wasi-python shim (web, limited).

## 17. Performance & Memory

* Release profile: `opt-level=3`, `lto=thin`, `codegen-units=1`, `panic=abort`.
* Pools: particles, decals, command buffers; SoA for hot loops; no per-frame alloc in audio/render hot paths.
* Caches bounded (LRU); handles generational to prevent use-after-free.
* Benchmarks: Criterion suites for sprite batch, mesh instancing, ECS iteration, physics step, Python bulk calls; tracked in `benchmarks/`.

## 18. Security & Safety

* `unsafe` only with `// SAFETY:` comment; no `unsafe` in Python bridge for memory reinterpretation.
* Asset parsers validate before GPU upload; shader errors don't crash.
* Networking: message size caps, decompression bomb limits.

## 19. Testing Strategy

Unit (each crate) + integration (`tests/`) + Python binding (`python/tests/`) + rendering golden (headless wgpu) + stress (10k entities). CI on Linux/Windows/macOS; WASM smoke test.

## 20. Roadmap (see DEVELOPMENT_STATUS.md)

M1: window + GPU + 2D sprite + 3D cube + input + Python callback + clean shutdown (same GPU abstraction).
M2: scene/prefab + assets async + audio.
M3: physics + animation + particles + UI.
M4: networking + editor + profiler.
M5: export pipelines (desktop → mobile → web) + docs.
