import falo

def test_import_alias():
    import sys
    assert "engine" in sys.modules
    import engine
    assert engine.Game is falo.Game

def test_game_decorators():
    g = falo.Game(headless=True)
    called = {}
    @g.update
    def upd(dt): called['upd']=True
    @g.draw
    def dr(): called['dr']=True
    g.run(max_frames=1, headless=True)
    assert called['upd']
    assert called['dr']

def test_physics():
    from falo.physics import PhysicsWorld, RigidBody, Collider
    w = PhysicsWorld()
    b = RigidBody()
    w.add_body(b, Collider())
    w.step(0.016)
    assert len(w.bodies)==1

def test_audio():
    from falo.audio import AudioEngine
    a = AudioEngine()
    s = a.play("assets/sfx.wav")
    assert s.playing
