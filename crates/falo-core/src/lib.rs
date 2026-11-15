use serde::{Deserialize, Serialize};

pub mod time;
pub mod app;
pub mod plugin;

pub use time::Time;
pub use app::App;
pub use plugin::Plugin;

/// Engine version.
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EngineConfig {
    pub title: String,
    pub width: u32,
    pub height: u32,
    pub fullscreen: bool,
    pub vsync: bool,
    pub target_fps: Option<f32>,
}

impl Default for EngineConfig {
    fn default() -> Self {
        Self { title: "Falo Game".into(), width: 1280, height: 720, fullscreen: false, vsync: true, target_fps: Some(60.0) }
    }
}
