from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore

@dataclass
class FaloConfig:
    name: str = "My Game"
    version: str = "1.0.0"
    entry: str = "main.py"
    default_target: str = "linux"
    profile: str = "release"
    bundle_python: bool = True
    compress_assets: bool = True
    identifier: str = "com.example.mygame"
    icon: Optional[str] = None
    orientation: str = "landscape"
    fullscreen: bool = True
    assets_include: List[str] = field(default_factory=lambda: ["assets/**"])
    assets_exclude: List[str] = field(default_factory=lambda: ["assets/source/**", "**/*.psd"])
    # platform specific
    android_min_sdk: int = 26
    android_target_sdk: int = 35
    android_version_code: int = 1
    windows_console: bool = False
    author: str = "Falo Dev"

    def validate(self):
        if self.profile not in ("release", "debug"):
            raise ValueError(f"invalid profile {self.profile}")
        if self.default_target not in ("windows","linux","linux-deb","linux-rpm","linux-appimage","macos","macos-dmg","android","android-aab","ios","web"):
            # allow aliases
            pass

def load_config(root: Path) -> FaloConfig:
    cfg = FaloConfig()
    # 1. falo.toml
    for cand in [root / "falo.toml", root / "Falo.toml", root / "engine.toml"]:
        if cand.exists():
            try:
                data = tomllib.load(open(cand, "rb"))
                _apply(cfg, data)
                print(f"[Falo::Config] loaded {cand}")
            except Exception as e:
                print(f"[Falo::Config] warn failed to parse {cand}: {e}")
            break
    # 2. pyproject.toml [tool.falo]
    pyproj = root / "pyproject.toml"
    if pyproj.exists():
        try:
            data = tomllib.load(open(pyproj, "rb"))
            tool = data.get("tool", {}).get("falo", {})
            if tool: _apply(cfg, {"project": {}, "build": tool, "application": tool})
        except Exception as e:
            print(f"[Falo::Config] warn pyproject {e}")
    return cfg

def _apply(cfg: FaloConfig, data: dict):
    proj = data.get("project", {})
    if "name" in proj: cfg.name = proj["name"]
    if "version" in proj: cfg.version = proj["version"]
    if "entry" in proj: cfg.entry = proj["entry"]
    build = data.get("build", {})
    if "default_target" in build: cfg.default_target = build["default_target"]
    if "profile" in build: cfg.profile = build["profile"]
    if "bundle_python" in build: cfg.bundle_python = bool(build["bundle_python"])
    if "compress_assets" in build: cfg.compress_assets = bool(build["compress_assets"])
    app = data.get("application", {})
    if "identifier" in app: cfg.identifier = app["identifier"]
    if "icon" in app: cfg.icon = app["icon"]
    if "orientation" in app: cfg.orientation = app["orientation"]
    if "fullscreen" in app: cfg.fullscreen = bool(app["fullscreen"])
    android = data.get("android", {})
    if "min_sdk" in android: cfg.android_min_sdk = int(android["min_sdk"])
    if "target_sdk" in android: cfg.android_target_sdk = int(android["target_sdk"])
    if "version_code" in android: cfg.android_version_code = int(android["version_code"])
    windows = data.get("windows", {})
    if "console" in windows: cfg.windows_console = bool(windows["console"])
    assets = data.get("assets", {})
    if "include" in assets: cfg.assets_include = assets["include"]
    if "exclude" in assets: cfg.assets_exclude = assets["exclude"]
