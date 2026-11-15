from __future__ import annotations
from pathlib import Path
import fnmatch, os, json, shutil

def collect_assets(include, exclude):
    collected = []
    # Expand globs via Path.rglob for simplicity
    for pat in include or ["assets/**"]:
        # pat like "assets/**" => base assets
        base = pat.split("**")[0].rstrip("/").rstrip("*").strip()
        if not base: base = "."
        base_path = Path(base)
        if not base_path.exists():
            # try assets dir directly
            if Path("assets").exists():
                base_path = Path("assets")
            else:
                continue
        for f in base_path.rglob("*"):
            if f.is_file():
                rel = f.as_posix()
                # exclude check
                skip = False
                for ex in exclude or []:
                    if fnmatch.fnmatch(rel, ex) or fnmatch.fnmatch(f.name, ex):
                        skip = True
                        break
                    # handle "**/*.psd" etc
                    if ex.startswith("**/") and f.name.endswith(ex[3:].replace("*","")):
                        skip=True; break
                if not skip:
                    collected.append(f)
    # deduplicate
    uniq = {}
    for p in collected: uniq[p.as_posix()] = p
    return list(uniq.values())

def build_asset_manifest(files):
    manifest = {"files": [], "total_bytes": 0}
    for f in files:
        try:
            size = f.stat().st_size
        except: size=0
        manifest["files"].append({"path": f.as_posix(), "size": size})
        manifest["total_bytes"] += size
    return manifest

def copy_assets_to(files, dest: Path):
    dest.mkdir(parents=True, exist_ok=True)
    for f in files:
        target = dest / f.name if f.parent.name=="assets" else dest / f.relative_to(Path.cwd()) if f.is_relative_to(Path.cwd()) else dest / f.name
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(f, target)
        except Exception as e:
            print(f"[assets] copy failed {f} -> {target}: {e}")
