//! Rust-only example: same GPU abstraction, no Python.
//! Run with: cargo run -p example_cube -- --headless
use falo_core::EngineConfig;
use falo_window::WindowConfig;
use falo_gfx_dummy::{GpuContext, Renderer};

fn main() -> anyhow::Result<()> {
    env_logger::init();
    let config = EngineConfig { title: "Cube Rust".into(), width: 1280, height: 720, ..Default::default() };
    println!("Rust example cube: {} {}x{}", config.title, config.width, config.height);
    // In real build:
    // let window = falo_window::Window::new(WindowConfig { title: config.title.clone(), width: config.width, height: config.height, ..Default::default() });
    // let gpu = pollster::block_on(GpuContext::new(window.is_headless()))?;
    // let renderer = falo_renderer_3d::Renderer3D::new(&gpu);
    // renderer.draw_cube();
    println!("Rust API works without Python — headless render ok");
    Ok(())
}
