use glam::{Vec3, Mat4};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Mesh {
    pub vertices: Vec<[f32; 3]>,
    pub indices: Vec<u32>,
    pub normals: Vec<[f32; 3]>,
    pub uvs: Vec<[f32; 2]>,
}

impl Mesh {
    pub fn cube(size: f32) -> Self {
        let s = size * 0.5;
        let vertices = vec![
            [-s,-s,-s],[s,-s,-s],[s,s,-s],[-s,s,-s],
            [-s,-s,s],[s,-s,s],[s,s,s],[-s,s,s],
        ];
        let indices = vec![0,1,2,2,3,0, 4,5,6,6,7,4, 0,4,7,7,3,0, 1,5,6,6,2,1, 3,2,6,6,7,3, 0,1,5,5,4,0];
        let normals = vec![[0.0,0.0,-1.0]; 8];
        let uvs = vec![[0.0,0.0]; 8];
        Self { vertices, indices, normals, uvs }
    }
    pub fn triangle_count(&self) -> usize { self.indices.len() / 3 }
}

#[derive(Debug, Clone)]
pub struct PbrMaterial {
    pub base_color: [f32; 4],
    pub metallic: f32,
    pub roughness: f32,
    pub emissive: [f32; 3],
}
impl Default for PbrMaterial {
    fn default() -> Self { Self { base_color: [1.0,1.0,1.0,1.0], metallic: 0.0, roughness: 0.5, emissive: [0.0;3] } }
}

#[derive(Debug, Clone)]
pub enum Light {
    Directional { direction: Vec3, color: Vec3, intensity: f32 },
    Point { position: Vec3, color: Vec3, intensity: f32, range: f32 },
    Spot { position: Vec3, direction: Vec3, color: Vec3, intensity: f32, cutoff: f32 },
}

#[derive(Debug, Clone)]
pub struct Camera3D {
    pub position: Vec3,
    pub target: Vec3,
    pub fov: f32,
    pub aspect: f32,
    pub near: f32,
    pub far: f32,
}
impl Default for Camera3D {
    fn default() -> Self { Self { position: Vec3::new(0.0,3.0,8.0), target: Vec3::ZERO, fov: 45_f32.to_radians(), aspect: 16.0/9.0, near: 0.1, far: 1000.0 } }
}
impl Camera3D {
    pub fn view_matrix(&self) -> Mat4 { Mat4::look_at_rh(self.position, self.target, Vec3::Y) }
    pub fn proj_matrix(&self) -> Mat4 { Mat4::perspective_rh(self.fov, self.aspect, self.near, self.far) }
}

/// Shadow map config
#[derive(Debug, Clone)]
pub struct ShadowConfig {
    pub enabled: bool,
    pub resolution: u32,
    pub cascades: usize,
}
impl Default for ShadowConfig { fn default() -> Self { Self { enabled: true, resolution: 2048, cascades: 4 } } }
