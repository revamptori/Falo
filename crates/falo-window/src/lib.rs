use winit::event::{ElementState, KeyEvent, MouseButton, WindowEvent};
use winit::keyboard::{KeyCode, PhysicalKey};

#[derive(Debug, Clone)]
pub struct WindowConfig {
    pub title: String,
    pub width: u32,
    pub height: u32,
    pub resizable: bool,
    pub fullscreen: bool,
}
impl Default for WindowConfig {
    fn default() -> Self { Self { title: "Falo".into(), width: 1280, height: 720, resizable: true, fullscreen: false } }
}

/// Thin wrapper around winit window + event pump.
/// In headless mode (no display), `is_headless()` returns true and no window is created.
pub struct Window {
    config: WindowConfig,
    headless: bool,
}

impl Window {
    pub fn new(config: WindowConfig) -> Self {
        // Detect headless: no DISPLAY on Linux and not Windows/macOS
        let headless = std::env::var("FALO_HEADLESS").is_ok()
            || (cfg!(target_os = "linux") && std::env::var("DISPLAY").is_err() && std::env::var("WAYLAND_DISPLAY").is_err());
        log::info!("Window::new title={} {}x{} headless={}", config.title, config.width, config.height, headless);
        Self { config, headless }
    }
    pub fn is_headless(&self) -> bool { self.headless }
    pub fn size(&self) -> (u32, u32) { (self.config.width, self.config.height) }
}
