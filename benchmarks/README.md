# Benchmarks

Run with:

```bash
uv run benchmarks/bench_sprite.py
cargo bench --workspace  # when Rust toolchain present
```

Measures:
- Sprite batch 10k sprites
- ECS query 100k entities
- Physics step 1k bodies
- Python bulk ops

Results are logged and compared against targets in DEVELOPMENT_STATUS.md.
Never fabricate results — run on target hardware.
