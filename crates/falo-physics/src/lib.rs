use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum BodyType { Static, Dynamic, Kinematic }

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RigidBody { pub body_type: BodyType, pub mass: f32, pub gravity: [f32; 3] }
impl Default for RigidBody { fn default() -> Self { Self { body_type: BodyType::Dynamic, mass: 1.0, gravity: [0.0, -9.81, 0.0] } } }

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum Collider { Box { size: [f32; 3] }, Sphere { radius: f32 }, Capsule { height: f32, radius: f32 }, Circle { radius: f32 }, Polygon { vertices: Vec<[f32;2]> } }

pub struct PhysicsWorld {
    pub gravity: [f32; 3],
    pub fixed_dt: f32,
    pub body_count: usize,
}
impl PhysicsWorld {
    pub fn new(gravity: [f32;3]) -> Self { Self { gravity, fixed_dt: 1.0/60.0, body_count: 0 } }
    pub fn step(&mut self, dt: f32) { log::trace!("PhysicsWorld step dt={} bodies={}", dt, self.body_count); }
    pub fn raycast(&self, origin: [f32;3], dir: [f32;3]) -> Option<f32> { let _ = (origin, dir); None }
}
