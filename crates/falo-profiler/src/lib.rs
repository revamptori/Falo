use std::time::Instant;
pub struct Profiler { pub frames: Vec<f32> }
impl Profiler {
    pub fn new() -> Self { Self { frames: Vec::with_capacity(256) } }
    pub fn begin(&self) -> Instant { Instant::now() }
    pub fn end(&mut self, start: Instant) { self.frames.push(start.elapsed().as_secs_f32()); if self.frames.len()>256 { self.frames.remove(0); } }
    pub fn avg_ms(&self) -> f32 { if self.frames.is_empty(){0.0} else { self.frames.iter().sum::<f32>() / self.frames.len() as f32 * 1000.0 } }
}
