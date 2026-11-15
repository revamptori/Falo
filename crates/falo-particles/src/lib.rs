use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ParticleConfig {
    pub rate: f32,
    pub lifetime: f32,
    pub velocity: [f32;3],
    pub gravity: [f32;3],
    pub color_start: [f32;4],
    pub color_end: [f32;4],
    pub size_start: f32,
    pub size_end: f32,
}

impl Default for ParticleConfig { fn default() -> Self { Self { rate: 100.0, lifetime: 2.0, velocity: [0.0,5.0,0.0], gravity: [0.0,-9.81,0.0], color_start: [1.0,1.0,1.0,1.0], color_end: [1.0,1.0,1.0,0.0], size_start: 1.0, size_end: 0.0 } } }

pub struct ParticleSystem {
    pub config: ParticleConfig,
    pub alive: usize,
    pub max_particles: usize,
}
impl ParticleSystem {
    pub fn new(config: ParticleConfig) -> Self { Self { config, alive: 0, max_particles: 10000 } }
    pub fn emit(&mut self, count: usize) { self.alive = (self.alive + count).min(self.max_particles); }
    pub fn update(&mut self, dt: f32) { let _ = dt; }
    pub fn burst(&mut self, count: usize) { self.emit(count); }
}
