use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnimationClip { pub name: String, pub duration: f32, pub looped: bool, pub frames: usize }
impl AnimationClip { pub fn new(name: &str, duration: f32) -> Self { Self { name: name.into(), duration, looped: true, frames: 24 } } }

pub struct Animator {
    pub current: Option<String>,
    pub time: f32,
    pub speed: f32,
    pub blending: f32,
}
impl Animator {
    pub fn new() -> Self { Self { current: None, time: 0.0, speed: 1.0, blending: 0.0 } }
    pub fn play(&mut self, name: &str) { self.current = Some(name.into()); self.time = 0.0; }
    pub fn update(&mut self, dt: f32) { self.time += dt * self.speed; }
}

/// Blend tree node
pub enum BlendNode { Clip(String, f32), Blend2(Box<BlendNode>, Box<BlendNode>, f32) }
