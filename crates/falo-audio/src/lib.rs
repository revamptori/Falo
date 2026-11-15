use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AudioConfig { pub master_volume: f32, pub music_volume: f32, pub sfx_volume: f32 }
impl Default for AudioConfig { fn default() -> Self { Self { master_volume: 1.0, music_volume: 1.0, sfx_volume: 1.0 } } }

pub struct AudioEngine { pub config: AudioConfig, pub headless: bool }
impl AudioEngine {
    pub fn new(config: AudioConfig) -> Self {
        let headless = std::env::var("FALO_HEADLESS").is_ok();
        log::info!("AudioEngine new headless={} master_vol={}", headless, config.master_volume);
        Self { config, headless }
    }
    pub fn play(&self, path: &str, volume: f32, looping: bool) { log::debug!("Audio play {} vol={} looping={} headless={}", path, volume, looping, self.headless); }
    pub fn set_master_volume(&mut self, v: f32) { self.config.master_volume = v.clamp(0.0, 1.0); }
}
