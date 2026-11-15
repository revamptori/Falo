# Fix: maturin develop — interpreter + linker

## Your 3 errors in order

1. `missing field package` at `/root/Falo/Cargo.toml` — ran at repo root.
   Fix: `cd python && maturin develop` (now patched on main, manifest-path points to crate).

2. `Failed to determine python platform / Skipping .venv/bin/python` — `python` symlink broken.
   Fix: `python3.11 -m venv .venv --clear` or `-i python3.11`

3. Current: `linker cc not found`
   Cause: `build-essential` (gcc + cc) not installed.
   Fix on your machine:
   ```bash
   sudo apt update && sudo apt install -y build-essential pkg-config
   # or on Fedora: sudo dnf groupinstall "Development Tools"
   # macOS: xcode-select --install
   ```

Correct command from `python/` after fix:
```bash
source ../.venv/bin/activate  # or .venv creation
maturin develop --release
# maturin auto-detects interpreter from activated venv; do NOT use `-- --interpreter`
```
