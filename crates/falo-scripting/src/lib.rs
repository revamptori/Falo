use anyhow::Result;
pub trait ScriptHost { fn call_update(&self, dt: f32) -> Result<()>; fn call_draw(&self) -> Result<()>; }
pub struct DummyHost;
impl ScriptHost for DummyHost { fn call_update(&self, _dt: f32) -> Result<()> { Ok(()) } fn call_draw(&self) -> Result<()> { Ok(()) } }
