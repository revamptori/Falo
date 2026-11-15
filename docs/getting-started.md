# Getting Started

## Install

```bash
pip install -e python/
# For Rust acceleration:
# install Rust 1.85+ https://rustup.rs
maturin develop
```

## Hello triangle

```python
import falo
game = falo.Game(title="Hello", width=1280, height=720, mode="2d")
sprite = game.scene.create_sprite("assets/player.png")
game.run()
```

## Build standalone

```bash
uv run main.py --executable dist/game.exe --release
uv run falo build --target linux --release
uv run falo build --target android --format apk --release
uv run falo build --target web --release
```

See guides/build.md for all targets.

## Rust-only

```toml
[dependencies]
falo-core = { path = "crates/falo-core" }
falo-renderer = { path = "crates/falo-renderer" }
```

```rust
use falo_core::{App, EngineConfig};
fn main() {
  let mut app = App::new(EngineConfig::default());
  app.run();
}
```

