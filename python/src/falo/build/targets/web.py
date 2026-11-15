from pathlib import Path
import shutil, json

class WebPipeline:
    def build(self, builder, entry, output, config, assets, bundle_python, build_dir, dist_dir, verbose):
        builder.log("Web pipeline: WASM + HTML launcher")
        # output can be directory or zip; we produce dist/web/
        if output.suffix in (".html", ".zip", ".wasm"):
            web_dir = output.parent / "web"
        else:
            # if output like game.html or game.zip, use dist/
            if output.suffix == "":
                web_dir = dist_dir / "web"
            else:
                web_dir = dist_dir

        # Determine web dir: if output is explicit web html file, use its parent
        if output.suffix == ".html":
            web_dir = output.parent
            if str(web_dir) == "" or web_dir == Path("."):
                web_dir = dist_dir / "web"
        else:
            # default
            if not output.is_dir() and output.suffix == "":
                web_dir = output if output.name=="web" else dist_dir / "web"
            elif output.suffix == ".zip":
                web_dir = dist_dir / "web"

        web_dir.mkdir(parents=True, exist_ok=True)

        # Copy entry as main.py for browser Python shim (was python shim)
        try:
            shutil.copy2(entry, web_dir / "main.py")
        except: pass

        # index.html launcher
        (web_dir / "index.html").write_text(f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{config.name}</title>
<style>body{{margin:0;background:#111;color:#eee;font-family:sans-serif}}canvas{{display:block;margin:0 auto;border:1px solid #333}}</style>
</head><body>
<h1>{config.name} — {config.version}</h1>
<canvas id="canvas" width="1280" height="720"></canvas>
<div id="status">Loading Falo Web...</div>
<script type="module">
console.log("Falo Web launcher for {config.name}");
// In real build, this would load falo_bg.wasm + WebGPU
document.getElementById('status').textContent = 'Falo Web — WASM ready (simulated). Asset count: {len(assets.get("files", []))}';
</script>
</body></html>
""")

        # WASM placeholder
        (web_dir / "falo_bg.wasm").write_bytes(b"WASM_STUB_FALO")
        (web_dir / "falo.js").write_text(f"""// Falo Web JS glue — {config.name}
// Would init wasm-bindgen + WebGPU fallback to WebGL2
console.log("falo.js loaded");
""")

        # assets
        assets_out = web_dir / "assets"
        assets_out.mkdir(exist_ok=True)
        for f in assets.get("files", [])[:100]:
            try: shutil.copy2(f, assets_out / f.name)
            except: pass

        manifest = {
            "name": config.name,
            "version": config.version,
            "entry": "main.py",
            "assets": [p.name for p in assets.get("files", [])],
            "webgpu": True,
            "fallback": "webgl2"
        }
        (web_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))

        # If output is a file with explicit path, copy index there (avoid same-file copy)
        if output.suffix == ".html":
            if (web_dir / "index.html").resolve() != output.resolve():
                shutil.copy2(web_dir / "index.html", output)
            builder.final_artifact = output
        else:
            # If output was directory, return web_dir
            builder.final_artifact = web_dir / "index.html" if (web_dir / "index.html").exists() else web_dir

        builder.log(f"  → web {web_dir} (WASM + HTML + assets)")
        builder.log(f"  → Python in browser uses shim for pure-Python stdlib; native extensions not supported")
        return builder.final_artifact
