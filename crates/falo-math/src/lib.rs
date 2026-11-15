pub use glam::*;

pub mod transform;

pub fn lerp(a: f32, b: f32, t: f32) -> f32 { a + (b - a) * t }

/// Angle helpers.
pub fn deg_to_rad(d: f32) -> f32 { d * std::f32::consts::PI / 180.0 }
pub fn rad_to_deg(r: f32) -> f32 { r * 180.0 / std::f32::consts::PI }
