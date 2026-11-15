# Troubleshooting

* **No window**: set `FALO_HEADLESS=1` or pass `--headless`
* **GPU init failed**: fallback to headless; check wgpu backend (Vulkan/Metal/DX12)
* **Android SDK missing**: pipeline generates Gradle project + unsigned APK; install Android SDK/NDK for signing
* **Xcode missing**: iOS IPA unsigned; install Xcode
* **Rust not found**: `pip install rustup` or https://rustup.rs
* **Python not bundled**: check `falo.toml` bundle_python
