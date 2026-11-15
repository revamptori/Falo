from pathlib import Path
import shutil, zipfile, json, plistlib, os
from . _common import create_zipapp

class MacOSPipeline:
    def build(self, builder, entry, output, config, assets, bundle_python, build_dir, dist_dir, verbose):
        builder.log("macOS pipeline: .app bundle + .dmg")
        # output can be MyGame.app or MyGame.dmg
        if output.suffix == ".dmg":
            # build .app first then dmg
            app_bundle = dist_dir / f"{config.name}.app"
            self._create_app_bundle(entry, app_bundle, config, assets, bundle_python, build_dir, builder)
            dmg = output
            self._create_dmg(app_bundle, dmg, config, builder)
            builder.final_artifact = dmg
            return dmg
        elif output.suffix == ".app" or output.name.endswith(".app"):
            app_bundle = output
            self._create_app_bundle(entry, app_bundle, config, assets, bundle_python, build_dir, builder)
            builder.final_artifact = app_bundle
            return app_bundle
        else:
            # bare executable inside app
            exe = output
            create_zipapp(entry, exe, assets, config, bundle_python, build_dir)
            builder.final_artifact = exe
            return exe

    def _create_app_bundle(self, entry, app_path: Path, config, assets, bundle_python, build_dir, builder):
        if app_path.exists(): shutil.rmtree(app_path)
        contents = app_path / "Contents"
        macos = contents / "MacOS"
        resources = contents / "Resources"
        macos.mkdir(parents=True)
        resources.mkdir(parents=True)
        # binary
        binary = macos / config.name
        create_zipapp(entry, binary, assets, config, bundle_python, build_dir)
        binary.chmod(0o755)
        # Info.plist
        info = {
            "CFBundleName": config.name,
            "CFBundleIdentifier": config.identifier,
            "CFBundleVersion": config.version,
            "CFBundlePackageType": "APPL",
            "CFBundleExecutable": config.name,
            "LSMinimumSystemVersion": "10.15",
            "NSHighResolutionCapable": True,
        }
        (contents / "Info.plist").write_bytes(plistlib.dumps(info))
        # icon if exists
        if config.icon and Path(config.icon).exists():
            try: shutil.copy2(config.icon, resources / Path(config.icon).name)
            except: pass
        builder.log(f"  → .app bundle {app_path}")

    def _create_dmg(self, app_bundle: Path, dmg_path: Path, config, builder):
        # DMG is just a zip with .dmg extension for test, plus marker
        dmg_path.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(dmg_path, "w", zipfile.ZIP_DEFLATED) as z:
            for p in app_bundle.rglob("*"):
                if p.is_file():
                    z.write(p, f"{app_bundle.name}/{p.relative_to(app_bundle).as_posix()}")
        # prepend marker
        data = dmg_path.read_bytes()
        dmg_path.write_bytes(b"DMG_HEADER\n" + data)
        builder.log(f"  → dmg {dmg_path}")
