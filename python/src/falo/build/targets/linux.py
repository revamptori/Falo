from pathlib import Path
import shutil, zipfile, json, subprocess, os
from . _common import create_zipapp

class LinuxPipeline:
    def build(self, builder, entry, output, config, assets, bundle_python, build_dir, dist_dir, verbose):
        builder.log("Linux pipeline: native binary + portable")
        dist_dir.mkdir(parents=True, exist_ok=True)

        # For .linux extension or no extension, treat as binary
        # Normalize: if no suffix or .linux, keep name but ensure executable
        out = output
        if out.suffix == ".linux":
            # keep as is
            pass
        elif out.suffix == "":
            # no ext → binary
            pass
        # Create zipapp
        create_zipapp(entry, out, assets, config, bundle_python, build_dir)
        builder.log(f"  → {out} ({out.stat().st_size} bytes)")

        # Desktop entry — sanitize identifier for filename
        safe_id = config.identifier.replace("/", "_").replace("\\", "_")
        desktop = dist_dir / f"{safe_id}.desktop"
        desktop.write_text(f"""[Desktop Entry]
Name={config.name}
Exec=./{out.name}
Icon={config.name.lower()}
Type=Application
Categories=Game;
""")
        builder.final_artifact = out
        return out

class AppImagePipeline:
    def build(self, builder, entry, output, config, assets, bundle_python, build_dir, dist_dir, verbose):
        builder.log("AppImage pipeline")
        base = dist_dir / f"{config.name}-{config.version}.AppImage"
        # Create base zipapp then rename to AppImage ( AppImages are squashfs + runtime; we simulate with zip + marker)
        tmp = build_dir / "appimage_temp"
        create_zipapp(entry, tmp, assets, config, bundle_python, build_dir)
        shutil.copy2(tmp, base)
        # marker header
        data = base.read_bytes()
        base.write_bytes(b"# AppImage stub\n" + data)
        base.chmod(0o755)
        builder.final_artifact = output if output.suffix==".AppImage" else base
        if output.suffix==".AppImage": shutil.copy2(base, output)
        return builder.final_artifact

class DebPipeline:
    def build(self, builder, entry, output, config, assets, bundle_python, build_dir, dist_dir, verbose):
        builder.log("Deb pipeline")
        deb = output if output.suffix==".deb" else dist_dir / f"{config.name.lower()}_{config.version}_amd64.deb"
        # Deb is ar archive with control + data; simulate with zip + control
        tmp = build_dir / "deb_stage"
        tmp.mkdir(parents=True, exist_ok=True)
        bin_path = tmp / "usr/bin" / config.name.lower()
        bin_path.parent.mkdir(parents=True, exist_ok=True)
        create_zipapp(entry, bin_path, assets, config, bundle_python, build_dir)
        bin_path.chmod(0o755)
        # control
        (tmp / "DEBIAN").mkdir(exist_ok=True)
        (tmp / "DEBIAN/control").write_text(f"Package: {config.name.lower()}\nVersion: {config.version}\nArchitecture: amd64\nMaintainer: {config.author}\nDescription: {config.name}\n")
        # simulate deb as tar+gz? just zip for test
        with zipfile.ZipFile(deb, "w", zipfile.ZIP_DEFLATED) as z:
            for p in tmp.rglob("*"):
                if p.is_file():
                    z.write(p, p.relative_to(tmp).as_posix())
        builder.final_artifact = deb
        return deb

class RpmPipeline:
    def build(self, builder, entry, output, config, assets, bundle_python, build_dir, dist_dir, verbose):
        builder.log("Rpm pipeline")
        rpm = output if output.suffix==".rpm" else dist_dir / f"{config.name.lower()}-{config.version}-1.x86_64.rpm"
        tmp = build_dir / "rpm_stage"
        tmp.mkdir(parents=True, exist_ok=True)
        bin_path = tmp / "usr/bin" / config.name.lower()
        bin_path.parent.mkdir(parents=True, exist_ok=True)
        create_zipapp(entry, bin_path, assets, config, bundle_python, build_dir)
        with zipfile.ZipFile(rpm, "w", zipfile.ZIP_DEFLATED) as z:
            for p in tmp.rglob("*"):
                if p.is_file():
                    z.write(p, p.relative_to(tmp).as_posix())
        builder.final_artifact = rpm
        return rpm
