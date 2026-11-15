pub trait Plugin: Send + Sync {
    fn name(&self) -> &str;
    fn build(&self);
}
