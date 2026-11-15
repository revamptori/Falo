import falo
from falo.audio import AudioEngine, AudioConfig

game = falo.Game(title="Audio Demo", width=800, height=600, mode="2d")
audio = AudioEngine(AudioConfig(master_volume=0.8))
sfx = audio.play("assets/sfx.wav", volume=1.0)

@game.update
def update(dt):
    pass

game.run(headless=True, max_frames=2)
