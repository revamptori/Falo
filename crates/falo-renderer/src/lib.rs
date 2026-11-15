use anyhow::Result;

/// Render graph DAG.
pub mod graph {
    #[derive(Debug)]
    pub struct RenderPass { pub name: String, pub enabled: bool }
    pub struct RenderGraph { pub passes: Vec<RenderPass> }
    impl RenderGraph {
        pub fn new() -> Self { Self { passes: vec![] } }
        pub fn add_pass(&mut self, name: &str) { self.passes.push(RenderPass { name: name.into(), enabled: true }); }
        pub fn execute(&self) { log::trace!("RenderGraph execute {} passes", self.passes.len()); }
    }
}

pub mod shader {
    use anyhow::Result;
    pub struct ShaderCache { pub hot_reload: bool }
    impl ShaderCache {
        pub fn new(hot_reload: bool) -> Self { Self { hot_reload } }
        pub fn compile_wgsl(&self, src: &str) -> Result<()> {
            // Validate via naga
            log::debug!("Compiling WGSL {} bytes", src.len());
            Ok(())
        }
    }
}

/// Common renderer plugin.
pub struct RendererPlugin;
impl RendererPlugin {
    pub fn new() -> Self { Self }
}
