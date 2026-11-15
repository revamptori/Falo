pub struct Editor { pub running: bool }
impl Editor {
    pub fn new() -> Self { Self { running: false } }
    pub fn run(&mut self) { self.running = true; log::info!("Editor run"); }
}
