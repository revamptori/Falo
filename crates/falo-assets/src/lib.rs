use std::collections::HashMap;
use anyhow::Result;

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Handle<T>(pub u64, std::marker::PhantomData<T>);
impl<T> Handle<T> { pub fn new(id: u64) -> Self { Self(id, std::marker::PhantomData) } }

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AssetState { Loading, Ready, Failed }

pub struct AssetServer {
    next_id: u64,
    states: HashMap<u64, AssetState>,
    hot_reload: bool,
}
impl AssetServer {
    pub fn new(hot_reload: bool) -> Self { Self { next_id: 1, states: HashMap::new(), hot_reload } }
    pub fn load<T>(&mut self, path: &str) -> Handle<T> {
        let id = self.next_id; self.next_id += 1;
        self.states.insert(id, AssetState::Loading);
        log::info!("AssetServer::load {} -> handle {}", path, id);
        // Async load would happen via background task; for now mark Ready synchronously if file exists
        let ready = std::path::Path::new(path).exists();
        self.states.insert(id, if ready { AssetState::Ready } else { AssetState::Loading });
        Handle::new(id)
    }
    pub fn state<T>(&self, h: &Handle<T>) -> AssetState { self.states.get(&h.0).copied().unwrap_or(AssetState::Failed) }
}
