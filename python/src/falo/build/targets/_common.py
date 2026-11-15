from __future__ import annotations
import zipfile, shutil, subprocess, sys, os, json
from pathlib import Path

# Helper to create a self-executing Python zipapp (executable)
def create_zipapp(entry: Path, output: Path, assets: dict, config, bundle_python: bool, build_dir: Path):
    """
    Create a zipapp that can be executed with `python output` or directly if chmod +x.
    This is the base for desktop artifacts; Windows wraps it with PE stub simulation.
    """
    output.parent.mkdir(parents=True, exist_ok=True)
    # Staging dir
    stage = build_dir / "stage"
    if stage.exists(): shutil.rmtree(stage)
    stage.mkdir(parents=True)

    # Copy entry as __main__.py
    stage_main = stage / "__main__.py"
    # We embed a launcher that handles assets from within zip
    entry_code = entry.read_text(encoding="utf-8", errors="ignore") if entry.exists() else 'print("no entry")'
    # Create wrapper __main__.py that sets up paths and runs entry
    wrapper = f'''# Falo bundled app — {config.name} {config.version}
import sys, os
from pathlib import Path
# Ensure assets are discoverable
os.environ["FALO_BUNDLED"] = "1"
# Run user code
{entry_code}
'''
    stage_main.write_text(wrapper)

    # Copy falo runtime (pure python) into bundle for standalone
    # We copy python/src/falo into stage/falo
    falo_src = Path(__file__).resolve().parents[2]  # python/src/falo
    if falo_src.exists():
        import shutil as _shutil
        dest_falo = stage / "falo"
        _shutil.copytree(falo_src, dest_falo, dirs_exist_ok=True)
        # Remove build targets cache to save size? keep

    # Copy assets
    assets_dest = stage / "assets"
    assets_dest.mkdir(parents=True, exist_ok=True)
    for f in assets.get("files", [])[:1000]:  # limit
        try:
            target = assets_dest / f.name
            # preserve relative if under assets/
            if "assets" in f.parts:
                # keep subdirectory
                rel = Path(*f.parts[f.parts.index("assets")+1:])
                target = assets_dest / rel
                target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)
        except Exception as e:
            print(f"[zipapp] asset copy failed {f}: {e}")

    # manifest
    (stage / "falo_manifest.json").write_text(json.dumps({
        "name": config.name,
        "version": config.version,
        "identifier": config.identifier,
        "target": config.default_target,
        "entry": entry.name,
        "bundle_python": bundle_python,
        "assets": [p.as_posix() for p in assets.get("files", [])],
    }, indent=2))

    # Create zipapp with shebang
    # Use python -m zipapp creation manually for control
    # We'll create a zip file then prepend shebang
    tmp_zip = build_dir / "tmp.zip"
    with zipfile.ZipFile(tmp_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for p in stage.rglob("*"):
            if p.is_file():
                arc = p.relative_to(stage).as_posix()
                z.write(p, arc)
    # Prepend shebang for Unix executability
    shebang = b"#!/usr/bin/env python3\n"
    with open(tmp_zip, "rb") as f: zip_data = f.read()
    with open(output, "wb") as out:
        out.write(shebang)
        out.write(zip_data)
    output.chmod(0o755)
    return output

def ensure_dist_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)
    return p
