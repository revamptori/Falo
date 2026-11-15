# Falo Editor

Standalone editor using the same runtime (egui/wgpu).

```bash
cargo run -p falo-editor
```

Features: project mgmt, hierarchy, 2D/3D viewport, inspector, asset browser, material editor, play/pause/step, profiler.

Editor deps do not bloat runtime (`falo-editor` is leaf crate).
