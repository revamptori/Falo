from pathlib import Path

def get_pipeline(name: str):
    name = name.lower()
    if name in ("windows", "win", "win64", "windows-x64", "windows-arm64"):
        from .windows import WindowsPipeline
        return WindowsPipeline()
    if name in ("linux", "linux-x64", "linux-arm64"):
        from .linux import LinuxPipeline
        return LinuxPipeline()
    if name == "linux-appimage":
        from .linux import AppImagePipeline
        return AppImagePipeline()
    if name == "linux-deb":
        from .linux import DebPipeline
        return DebPipeline()
    if name == "linux-rpm":
        from .linux import RpmPipeline
        return RpmPipeline()
    if name in ("macos", "darwin", "macos-dmg"):
        from .macos import MacOSPipeline
        return MacOSPipeline()
    if name in ("android", "apk"):
        from .android import AndroidPipeline
        return AndroidPipeline()
    if name == "android-aab":
        from .android import AABPipeline
        return AABPipeline()
    if name in ("ios", "ipa"):
        from .ios import IOSPipeline
        return IOSPipeline()
    if name == "web":
        from .web import WebPipeline
        return WebPipeline()
    # Default to Linux for unknown
    from .linux import LinuxPipeline
    return LinuxPipeline()
