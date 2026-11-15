use glam::{Vec3, Quat, Mat4};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Transform {
    pub translation: Vec3,
    pub rotation: Quat,
    pub scale: Vec3,
}
impl Default for Transform {
    fn default() -> Self { Self { translation: Vec3::ZERO, rotation: Quat::IDENTITY, scale: Vec3::ONE } }
}
impl Transform {
    pub fn matrix(&self) -> Mat4 { Mat4::from_scale_rotation_translation(self.scale, self.rotation, self.translation) }
    pub fn translate(&mut self, v: Vec3) { self.translation += v; }
}
