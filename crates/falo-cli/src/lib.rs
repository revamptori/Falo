use anyhow::Result;

#[derive(Debug)]
pub struct BuildConfig {
    pub target: String,
    pub release: bool,
    pub output: String,
}

pub fn build(config: BuildConfig) -> Result<()> {
    log::info!("falo-cli build target={} release={} output={}", config.target, config.release, config.output);
    Ok(())
}
