import falo
import pathlib

def test_game_creation():
    g = falo.Game(title="Test", width=800, height=600, mode="2d", headless=True)
    assert g.config.title == "Test"
    assert g.config.width == 800

def test_sprite_creation():
    g = falo.Game(title="Test2", headless=True)
    s = g.scene.create_sprite("assets/player.png")
    assert s.path == "assets/player.png"
    s.move(10, 20)
    assert s.position == (10, 20)

def test_model_loading():
    g = falo.Game(title="Test3", mode="3d", headless=True)
    m = g.scene.load_model("assets/player.glb")
    assert m.path == "assets/player.glb"
    cam = g.scene.create_camera()
    assert cam is not None

def test_input():
    kb = falo.keyboard
    kb.press("SPACE")
    assert kb.is_pressed("SPACE")
    kb.release("SPACE")
    assert not kb.is_pressed("SPACE")

def test_bulk_api():
    g = falo.Game(headless=True)
    ents = g.scene.spawn_batch(10)
    assert len(ents) == 10
    assert len(g.scene.entities) == 10

def test_build_config():
    from falo.build.config import FaloConfig
    cfg = FaloConfig(name="TestGame", version="1.2.3", default_target="windows")
    cfg.validate()
    assert cfg.name == "TestGame"

def test_assets():
    from falo.build.assets import collect_assets
    files = collect_assets(["assets/**"], ["**/*.psd"])
    # player.png should be there, source/model.blend should be excluded
    names = [f.name for f in files]
    assert "player.png" in names

def test_build_windows_artifact(tmp_path):
    # simulate build
    import sys
    from falo.build.config import FaloConfig
    from falo.build import Builder
    from pathlib import Path
    cfg = FaloConfig(name="Test", version="1.0.0", default_target="windows")
    entry = Path("main.py")
    out = tmp_path / "game.exe"
    b = Builder(config=cfg, entry=entry, output=out, cli_args=None)
    b.build()
    assert b.final_artifact.exists()
    assert b.final_artifact.stat().st_size > 0

def test_build_linux_artifact(tmp_path):
    from falo.build.config import FaloConfig
    from falo.build import Builder
    from pathlib import Path
    cfg = FaloConfig(name="Test", version="1.0.0", default_target="linux")
    entry = Path("main.py")
    out = tmp_path / "game"
    b = Builder(config=cfg, entry=entry, output=out, cli_args=None)
    b.build()
    assert b.final_artifact.exists()

def test_build_web(tmp_path):
    from falo.build.config import FaloConfig
    from falo.build import Builder
    from pathlib import Path
    cfg = FaloConfig(name="Test", version="1.0.0", default_target="web")
    entry = Path("main.py")
    out = tmp_path / "web"
    out.mkdir()
    o = out / "index.html"
    b = Builder(config=cfg, entry=entry, output=o, cli_args=None)
    b.build()
    assert (out / "index.html").exists()
