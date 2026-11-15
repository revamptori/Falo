use glam::{Vec2, Vec3};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Sprite {
    pub position: Vec2,
    pub size: Vec2,
    pub rotation: f32,
    pub color: [f32; 4],
    pub texture: Option<String>,
    pub layer: i32,
}

impl Default for Sprite {
    fn default() -> Self {
        Self { position: Vec2::ZERO, size: Vec2::new(64.0, 64.0), rotation: 0.0, color: [1.0,1.0,1.0,1.0], texture: None, layer: 0 }
    }
}

pub struct SpriteBatch {
    pub sprites: Vec<Sprite>,
    pub max_batch: usize,
}
impl SpriteBatch {
    pub fn new() -> Self { Self { sprites: Vec::with_capacity(4096), max_batch: 2048 } }
    pub fn push(&mut self, s: Sprite) { self.sprites.push(s); }
    pub fn clear(&mut self) { self.sprites.clear(); }
    pub fn draw_count(&self) -> usize { (self.sprites.len() + self.max_batch - 1) / self.max_batch.max(1) }
}

/// 2D camera with zoom/rotation/smoothing/parallax.
#[derive(Debug, Clone)]
pub struct Camera2D {
    pub position: Vec2,
    pub zoom: f32,
    pub rotation: f32,
    pub smoothing: f32,
}
impl Default for Camera2D {
    fn default() -> Self { Self { position: Vec2::ZERO, zoom: 1.0, rotation: 0.0, smoothing: 0.1 } }
}
impl Camera2D {
    pub fn view_matrix(&self) -> glam::Mat4 {
        glam::Mat4::from_scale_rotation_translation(
            glam::Vec3::splat(self.zoom),
            if self.rotation != 0.0 { glam::Quat::from_rotation_z(self.rotation) } else { glam::Quat::IDENTITY },
            Vec3::new(-self.position.x, -self.position.y, 0.0)
        )
    }
}

/// Tilemap chunked.
pub struct Tilemap {
    pub tile_size: u32,
    pub width: u32,
    pub height: u32,
    pub tiles: Vec<u32>,
}
impl Tilemap {
    pub fn new(w: u32, h: u32, tile_size: u32) -> Self { Self { tile_size, width: w, height: h, tiles: vec![0; (w*h) as usize] } }
}
