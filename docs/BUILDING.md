# Building Falo — Troubleshooting maturin

## Quick start (correct directory)

```bash
git clone https://github.com/revamptori/Falo.git
cd Falo
python3.11 -m venv .venv
source .venv/bin/activate
pip install maturin

# WRONG (at repo root → workspace has no [package]):
# maturin develop

# RIGHT (from python/ dir, manifest-path now fixed to crate):
cd python
maturin develop --release
python -c "import falo; print(falo.HAS_NATIVE)"
```

If your venv's `python` symlink is broken (`Skipping /root/Falo/.venv/bin/python: could not determine version`):

```bash
python3.11 -m venv .venv --clear
# or
maturin develop -i python3.11
# NOT `maturin develop -- --interpreter` (that forwards to cargo)
```

## Prerequisite: C linker

Error `linker cc not found` means `build-essential` missing:

```bash
sudo apt update && sudo apt install -y build-essential pkg-config libasound2-dev
# Fedora: sudo dnf groupinstall "Development Tools"
# macOS: xcode-select --install
```

## Warnings you can ignore

- `unused workspace dependency ...` — workspace defines deps for all 24 crates, but `maturin develop` only builds `falo-python`, so others appear unused. Harmless.
- `build-backend is not set to maturin` — `python/pyproject.toml` uses `setuptools` for pure-Python fallback (`pip install -e python/` without Rust). `maturin develop` still reads `[tool.maturin]` correctly.
