from __future__ import annotations
from dataclasses import dataclass

@dataclass
class AudioConfig:
    master_volume: float = 1.0
    music_volume: float = 1.0
    sfx_volume: float = 1.0

class Sound:
    def __init__(self, path: str, looping: bool = False, volume: float = 1.0):
        self.path = path
        self.looping = looping
        self.volume = volume
        self.playing = False
    def play(self):
        self.playing = True
        print(f"[Audio] play {self.path} vol={self.volume} looping={self.looping}")
    def stop(self):
        self.playing = False

class AudioEngine:
    def __init__(self, config: AudioConfig = None):
        self.config = config or AudioConfig()
        print(f"[AudioEngine] init master={self.config.master_volume}")
    def play(self, path: str, volume: float = 1.0, looping: bool = False) -> Sound:
        s = Sound(path, looping, volume * self.config.master_volume)
        s.play()
        return s
    def set_master_volume(self, v: float):
        self.config.master_volume = max(0.0, min(1.0, v))
