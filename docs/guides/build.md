# Build & Export

## Config file `falo.toml`

See root `falo.toml` example.

## Targets

| Target | Output | Toolchain | Notes |
|---|---|---|---|
| windows | .exe | rustc x86_64-pc-windows-msvc + WiX optional | Portable zip + installer |
| linux | binary, .AppImage, .deb, .rpm | rustc x86_64-unknown-linux-gnu | glibc 2.31+ |
| macos | .app, .dmg | Xcode, rustc aarch64-apple-darwin | Code signing |
| android | .apk, .aab | Android SDK/NDK, Gradle, rustc aarch64-linux-android | Signing via keystore |
| ios | .ipa | Xcode, rustc aarch64-apple-ios | Provisioning profile |
| web | dist/web/ | wasm32-unknown-unknown, wasm-bindgen | WebGPU/WebGL2 fallback |

## Python bundling

* Rust-only games omit Python.
* Python games bundle interpreter (desktop: embed, mobile: asset, web: shim subset).
* `bundle_python = false` in falo.toml to force Rust-only.

## Commands

```bash
uv run main.py --executable game.exe --release --icon assets/icon.ico
uv run falo build --target windows --release
uv run falo build --target android --format apk --release
uv run falo build --target web --release
```

## Caching

Build cache at `.falo_cache/` keyed by engine version + target + profile + Python ABI.

