"""
Falo CLI — `falo` / `engine` command.
Supports:
  falo new my_game
  falo run [--release]
  falo build --target windows --release --format apk
  falo import-assets
  falo package
Also handles `uv run main.py --executable ...` via app.Game interceptor.
"""

from __future__ import annotations
import argparse, sys, shutil, subprocess
from pathlib import Path

def cmd_new(args):
    raw = args.name or "my_game"
    dest = Path(raw)
    name = dest.name  # base name for project metadata (handles absolute paths)
    if dest.exists():
        print(f"[falo] {dest} already exists", file=sys.stderr); return 1
    dest.mkdir(parents=True)
    # main.py template
    (dest / "main.py").write_text(f'''""" {name} — Falo game """
import falo

game = falo.Game(title="{name}", width=1280, height=720, mode="2d")

# Create a sprite
player = game.scene.create_sprite("assets/player.png")
player.position = (100, 200)

@game.update
def update(dt):
    if falo.keyboard.is_pressed("SPACE"):
        player.move(0, 10)
    # bulk example: move all sprites
    # positions = game.scene.query_positions()

# falo will handle --executable automatically via Game.run()

game.run()
''')
    # assets dir
    (dest / "assets").mkdir()
    (dest / "assets" / "README.md").write_text("# Place textures, models, audio here\n")
    # falo.toml
    (dest / "falo.toml").write_text(f'''[project]
name = "{name}"
version = "1.0.0"
entry = "main.py"

[build]
default_target = "linux"
profile = "release"
bundle_python = true
compress_assets = true

[application]
identifier = "com.example.{name.lower()}"
icon = "assets/icon.png"
orientation = "landscape"
fullscreen = true

[android]
min_sdk = 26
target_sdk = 35
version_code = 1

[windows]
console = false

[assets]
include = ["assets/**"]
exclude = ["assets/source/**", "**/*.psd"]
''')
    # pyproject
    (dest / "pyproject.toml").write_text(f'''[project]
name = "{name}"
version = "1.0.0"
dependencies = ["falo"]

[tool.falo]
default_target = "linux"
''')
    print(f"[falo] created {dest}/")
    print(f"  cd {name} && uv run main.py")
    return 0

def cmd_run(args):
    # delegate to main.py or entry
    entry = Path(args.entry or "main.py")
    if not entry.exists():
        print(f"[falo] entry not found: {entry}", file=sys.stderr); return 1
    cmd = [sys.executable, str(entry)]
    if args.release: cmd.append("--release")
    if args.headless: cmd.append("--headless")
    print(f"[falo] run: {' '.join(cmd)}")
    return subprocess.call(cmd)

def cmd_build(args):
    from .build import Builder
    from .build.config import load_config
    from .build.assets import collect_assets, build_asset_manifest
    from pathlib import Path as P

    cfg = load_config(P.cwd())
    # override
    if args.target: cfg.default_target = args.target
    if args.format: # format maps to target variant
        fmt = args.format.lower()
        if fmt == "apk": cfg.default_target = "android"
        elif fmt == "aab": cfg.default_target = "android-aab"
        elif fmt == "appimage": cfg.default_target = "linux-appimage"
        elif fmt == "deb": cfg.default_target = "linux-deb"
        elif fmt == "rpm": cfg.default_target = "linux-rpm"
        elif fmt == "app": cfg.default_target = "macos"
        elif fmt == "dmg": cfg.default_target = "macos-dmg"
    if args.release: cfg.profile = "release"
    if args.debug: cfg.profile = "debug"

    entry = P(args.entry or cfg.entry or "main.py")
    # Default output per target
    default_out = {
        "windows": "dist/game.exe",
        "linux": "dist/game",
        "linux-appimage": "dist/game.AppImage",
        "linux-deb": "dist/game.deb",
        "linux-rpm": "dist/game.rpm",
        "macos": "dist/game.app",
        "macos-dmg": "dist/game.dmg",
        "android": "dist/game.apk",
        "android-aab": "dist/game.aab",
        "ios": "dist/game.ipa",
        "web": "dist/web/index.html",
    }
    out = P(args.output or default_out.get(cfg.default_target, "dist/game"))
    # handle --executable alias
    if args.executable: out = P(args.executable)

    builder = Builder(config=cfg, entry=entry, output=out, cli_args=args)
    builder.build()
    print(f"[falo] artifact: {builder.final_artifact}")
    return 0

def main():
    parser = argparse.ArgumentParser(prog="falo", description="Falo Engine CLI")
    sub = parser.add_subparsers(dest="cmd")

    # new
    p_new = sub.add_parser("new", help="create new project")
    p_new.add_argument("name", nargs="?", help="project name")

    # run
    p_run = sub.add_parser("run", help="run game")
    p_run.add_argument("--entry", default=None)
    p_run.add_argument("--release", action="store_true")
    p_run.add_argument("--headless", action="store_true")

    # build
    p_build = sub.add_parser("build", help="build artifact")
    p_build.add_argument("--target", dest="target", default=None, help="windows|linux|macos|android|ios|web")
    p_build.add_argument("--format", default=None, help="apk, aab, appimage, deb, rpm, app, dmg")
    p_build.add_argument("--release", action="store_true")
    p_build.add_argument("--debug", action="store_true")
    p_build.add_argument("--output", default=None)
    p_build.add_argument("--executable", default=None, help="alias for --output")
    p_build.add_argument("--arch", "--architecture", dest="arch", default=None)
    p_build.add_argument("--icon", default=None)
    p_build.add_argument("--assets", nargs="*")
    p_build.add_argument("--version", default=None)
    p_build.add_argument("--clean", action="store_true")
    p_build.add_argument("--verbose", action="store_true")
    p_build.add_argument("--jobs", default=None)
    p_build.add_argument("--entry", default=None)
    p_build.add_argument("--strip", action="store_true")
    p_build.add_argument("--optimize-size", action="store_true")
    p_build.add_argument("--optimize-speed", action="store_true")

    # import-assets, package (stubs)
    p_import = sub.add_parser("import-assets", help="import assets")
    p_pack = sub.add_parser("package", help="package game")

    args = parser.parse_args()

    if args.cmd == "new": return cmd_new(args)
    if args.cmd == "run": return cmd_run(args)
    if args.cmd == "build": return cmd_build(args)
    if args.cmd == "import-assets":
        print("[falo] import-assets: scanning assets/ and generating manifest")
        from .build.assets import collect_assets
        files = collect_assets(["assets/**"], ["**/*.psd"])
        print(f"  found {len(files)} assets")
        return 0
    if args.cmd == "package":
        print("[falo] package: use `falo build`")
        return 0

    # No subcommand: maybe `uv run main.py --executable ...` fallback already handled,
    # but if user ran `falo --executable ...` directly:
    if "--executable" in sys.argv or "--output" in sys.argv:
        from .build import handle_executable_arg
        return handle_executable_arg(sys.argv)

    parser.print_help()
    return 0

if __name__ == "__main__":
    sys.exit(main())
