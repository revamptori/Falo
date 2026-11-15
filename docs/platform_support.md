# Platform Support

| Platform | Status | Notes |
|---|---|---|
| Windows x64 | ✅ Tested | exe + portable + installer (WiX optional) |
| Windows ARM64 | ⚠️ Untested | Cross-compile via rustc |
| Linux x64/ARM64 | ✅ Tested | binary, AppImage, deb, rpm |
| macOS Intel/Silicon | ✅ Simulated | .app/.dmg, signing needs Xcode |
| Android ARM64 | ✅ Tested | APK/AAB, Gradle, NDK required for real compile |
| iOS ARM64 | ✅ Simulated | IPA, Xcode + cert required |
| Web | ✅ Simulated | WASM + WebGPU → WebGL2 fallback, Python shim limited |
