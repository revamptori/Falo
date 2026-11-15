use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum NetworkMessage { Reliable(Vec<u8>), Unreliable(Vec<u8>), Event(String) }

pub struct NetworkServer { pub port: u16, pub clients: usize }
impl NetworkServer {
    pub fn new(port: u16) -> Self { Self { port, clients: 0 } }
    pub fn start(&self) { log::info!("NetworkServer start port {}", self.port); }
}

pub struct NetworkClient { pub addr: String }
impl NetworkClient {
    pub fn connect(addr: &str) -> Self { log::info!("NetworkClient connect {}", addr); Self { addr: addr.into() } }
}
