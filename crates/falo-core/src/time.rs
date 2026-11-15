use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Time {
    pub delta_seconds: f32,
    pub elapsed_seconds: f32,
    pub fixed_dt: f32,
    pub frame_count: u64,
}
impl Default for Time {
    fn default() -> Self { Self { delta_seconds: 0.016, elapsed_seconds: 0.0, fixed_dt: 1.0/60.0, frame_count: 0 } }
}
impl Time {
    pub fn delta(&self) -> f32 { self.delta_seconds }
    pub fn elapsed(&self) -> f32 { self.elapsed_seconds }
    pub fn tick(&mut self, dt: f32) { self.delta_seconds = dt; self.elapsed_seconds += dt; self.frame_count += 1; }
}
