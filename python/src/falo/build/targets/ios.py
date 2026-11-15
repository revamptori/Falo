from pathlib import Path
import zipfile, shutil, plistlib

class IOSPipeline:
    def build(self, builder, entry, output, config, assets, bundle_python, build_dir, dist_dir, verbose):
        builder.log("iOS pipeline: IPA")
        if output.suffix != ".ipa": output = output.with_suffix(".ipa")
        dist_dir.mkdir(parents=True, exist_ok=True)

        # Xcode project skeleton
        xcode_root = build_dir / "ios"
        (xcode_root / "Payload").mkdir(parents=True, exist_ok=True)
        app_name = f"{config.name}.app"
        app_bundle = xcode_root / "Payload" / app_name
        app_bundle.mkdir(parents=True, exist_ok=True)

        # Info.plist
        info = {
            "CFBundleName": config.name,
            "CFBundleIdentifier": config.identifier,
            "CFBundleVersion": config.version,
            "CFBundleExecutable": config.name,
            "UISupportedInterfaceOrientations": [config.orientation],
        }
        (app_bundle / "Info.plist").write_bytes(plistlib.dumps(info))

        # Binary stub (zipapp)
        from . _common import create_zipapp
        binary = app_bundle / config.name
        create_zipapp(entry, binary, assets, config, bundle_python, build_dir)

        # Assets inside bundle
        for f in assets.get("files", [])[:50]:
            try: shutil.copy2(f, app_bundle / f.name)
            except: pass

        # Entitlements
        (app_bundle / f"{config.name}.entitlements").write_text(f"""<?xml version="1.0"?><dict><key>application-identifier</key><string>{config.identifier}</string></dict>""")

        # Create IPA (ZIP of Payload)
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as ipa:
            for p in (xcode_root / "Payload").rglob("*"):
                if p.is_file():
                    ipa.write(p, p.relative_to(xcode_root).as_posix())

        builder.log(f"  → IPA {output} ({output.stat().st_size} bytes) — signing requires Apple Developer cert + Xcode")
        if shutil.which("xcodebuild") is None:
            builder.log("  ⚠ xcodebuild not found — IPA unsigned, install Xcode for signing")

        builder.final_artifact = output
        return output
