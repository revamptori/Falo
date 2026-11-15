from pathlib import Path
import shutil, zipfile, json
from . _common import create_zipapp

class AndroidPipeline:
    def build(self, builder, entry, output, config, assets, bundle_python, build_dir, dist_dir, verbose):
        builder.log("Android pipeline: APK (Gradle + NDK simulation)")
        if output.suffix != ".apk":
            output = output.with_suffix(".apk")
        dist_dir.mkdir(parents=True, exist_ok=True)

        # Create Gradle project skeleton
        gradle_root = build_dir / "android"
        app_dir = gradle_root / "app"
        (app_dir / "src/main").mkdir(parents=True, exist_ok=True)

        # AndroidManifest.xml
        (app_dir / "src/main/AndroidManifest.xml").write_text(f"""<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="{config.identifier}" android:versionCode="{config.android_version_code}" android:versionName="{config.version}">
    <uses-sdk android:minSdkVersion="{config.android_min_sdk}" android:targetSdkVersion="{config.android_target_sdk}" />
    <application android:label="{config.name}" android:icon="@mipmap/ic_launcher" android:requestLegacyExternalStorage="true">
        <activity android:name=".MainActivity" android:exported="true" android:screenOrientation="{config.orientation}" android:configChanges="orientation|keyboardHidden|screenSize">
            <intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter>
        </activity>
    </application>
    <uses-permission android:name="android.permission.INTERNET" />
</manifest>""")

        # build.gradle stub
        (gradle_root / "build.gradle").write_text(f"""// Falo Android build — {config.name}
apply plugin: 'com.android.application'
android {{ compileSdk {config.android_target_sdk} defaultConfig {{ applicationId "{config.identifier}" minSdk {config.android_min_sdk} targetSdk {config.android_target_sdk} versionCode {config.android_version_code} versionName "{config.version}" }} }}
dependencies {{ implementation fileTree(dir: 'libs', include: ['*.jar']) }}
""")

        # Native lib placeholder (Rust compiled for ARM64)
        jni = app_dir / "src/main/jniLibs/arm64-v8a"
        jni.mkdir(parents=True, exist_ok=True)
        (jni / "libfalo.so").write_text("# simulated Rust lib for Android ARM64\n")
        (jni / "libpython3.11.so").write_text("# bundled Python runtime stub\n" if bundle_python else "")

        # Assets
        assets_dir = app_dir / "src/main/assets"
        assets_dir.mkdir(parents=True, exist_ok=True)
        for f in assets.get("files", [])[:100]:
            try: shutil.copy2(f, assets_dir / f.name)
            except: pass
        # entry script as asset
        try:
            shutil.copy2(entry, assets_dir / "main.py")
        except: pass

        # Create APK (which is ZIP)
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as apk:
            # Android requires classes.dex; we simulate with stub
            apk.writestr("classes.dex", b"DEX_STUB_FOR_FALO")
            apk.writestr("AndroidManifest.xml", (app_dir / "src/main/AndroidManifest.xml").read_text())
            # assets
            for p in (app_dir / "src/main/assets").rglob("*"):
                if p.is_file():
                    apk.write(p, f"assets/{p.name}")
            # native libs
            for p in jni.rglob("*"):
                if p.is_file():
                    apk.write(p, f"lib/arm64-v8a/{p.name}")
            # icon placeholder
            apk.writestr("res/mipmap/ic_launcher.png", b"PNG_ICON_STUB")

        builder.log(f"  → APK {output} ({output.stat().st_size} bytes) arm64-v8a")
        builder.log(f"  → Gradle project at {gradle_root} (run ./gradlew assembleRelease for real build, SDK required)")
        # Signing note
        if not shutil.which("apksigner"):
            builder.log("  ⚠ apksigner not found — APK unsigned (debug key would be used in real pipeline)")

        builder.final_artifact = output
        return output

class AABPipeline:
    def build(self, builder, entry, output, config, assets, bundle_python, build_dir, dist_dir, verbose):
        if output.suffix != ".aab": output = output.with_suffix(".aab")
        # AAB similar to APK but bundle
        apk_pipeline = AndroidPipeline()
        # Reuse but change suffix handling
        out = apk_pipeline.build(builder, entry, output.with_suffix(".apk"), config, assets, bundle_python, build_dir, dist_dir, verbose)
        aab = output
        shutil.copy2(out, aab)
        builder.log(f"  → AAB {aab}")
        builder.final_artifact = aab
        return aab
