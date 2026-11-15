#[derive(Debug, Default)]
pub struct DebugStats {
    pub fps: f32,
    pub frame_time_ms: f32,
    pub draw_calls: u32,
    pub triangles: u32,
    pub entities: u32,
    pub physics_bodies: u32,
}
impl DebugStats {
    pub fn new() -> Self { Self::default() }
    pub fn update(&mut self, dt: f32) { self.frame_time_ms = dt * 1000.0; self.fps = if dt>0.0 {1.0/dt} else {0.0}; }
}
pub fn draw_debug_overlay(stats: &DebugStats) { log::debug!("DEBUG overlay fps={:.1} dc={} tris={}", stats.fps, stats.draw_calls, stats.triangles); }
