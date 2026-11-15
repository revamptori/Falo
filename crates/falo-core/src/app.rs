use crate::{EngineConfig, plugin::Plugin};

pub struct App {
    pub config: EngineConfig,
    plugins: Vec<Box<dyn Plugin>>,
    running: bool,
}
impl App {
    pub fn new(config: EngineConfig) -> Self { Self { config, plugins: vec![], running: false } }
    pub fn add_plugin<P: Plugin + 'static>(&mut self, p: P) -> &mut Self { self.plugins.push(Box::new(p)); self }
    pub fn run(&mut self) {
        for p in &self.plugins { p.build(); }
        self.running = true;
        log::info!("App run {} {}x{}", self.config.title, self.config.width, self.config.height);
        // Real loop would be winit event loop here
        self.running = false;
    }
}
