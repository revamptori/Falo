use serde::{Deserialize, Serialize};
use falo_ecs::{Entity, World};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Transform {
    pub position: [f32; 3],
    pub rotation: [f32; 3],
    pub scale: [f32; 3],
}
impl Default for Transform { fn default() -> Self { Self { position: [0.0;3], rotation: [0.0;3], scale: [1.0;3] } } }

#[derive(Debug, Serialize, Deserialize)]
pub struct Scene {
    pub name: String,
    pub entities: Vec<SceneEntity>,
}
#[derive(Debug, Serialize, Deserialize)]
pub struct SceneEntity { pub id: u64, pub name: String, pub transform: Transform, pub prefab: Option<String> }

impl Scene {
    pub fn new(name: &str) -> Self { Self { name: name.into(), entities: vec![] } }
    pub fn to_ron(&self) -> String { ron::to_string(self).unwrap_or_default() }
    pub fn from_ron(s: &str) -> Result<Self, ron::Error> { ron::from_str(s) }
}

pub struct SceneManager { pub active: Option<Scene> }
impl SceneManager {
    pub fn new() -> Self { Self { active: None } }
    pub fn load(&mut self, scene: Scene) { self.active = Some(scene); }
}
