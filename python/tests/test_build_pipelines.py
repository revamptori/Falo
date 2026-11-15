from pathlib import Path
from falo.build.config import FaloConfig
from falo.build import Builder
import tempfile

def _build(target, suffix):
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        cfg = FaloConfig(name="PipeTest", version="1.0.0", default_target=target)
        entry = Path("main.py")
        out = td / f"game{suffix}"
        b = Builder(config=cfg, entry=entry, output=out, cli_args=None)
        b.build()
        assert b.final_artifact.exists()
        assert b.final_artifact.stat().st_size > 0
        print(f"{target} -> {b.final_artifact}")

def test_all_pipelines():
    _build("windows", ".exe")
    _build("linux", "")
    _build("android", ".apk")
    _build("ios", ".ipa")
    _build("macos", ".app")

def test_cli_build():
    import subprocess, sys
    r = subprocess.run([sys.executable, "-m", "falo", "build", "--target", "windows", "--output", "/tmp/falo_test_cli.exe"], capture_output=True, text=True)
    assert Path("/tmp/falo_test_cli.exe").exists()

def test_executable_arg():
    import subprocess, sys
    # This tests `uv run main.py --executable game.exe` equivalent: python main.py --executable /tmp/game.exe
    r = subprocess.run([sys.executable, "main.py", "--executable", "/tmp/falo_exe_test.exe", "--headless"], capture_output=True, text=True)
    # Game.run will intercept and build then exit; should succeed
    assert Path("/tmp/falo_exe_test.exe").exists() or "artifact ready" in r.stdout or r.returncode==0
