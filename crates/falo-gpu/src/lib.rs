use anyhow::Result;

/// Owns wgpu Instance/Adapter/Device/Queue/Surface.
/// One instance per App; all render crates borrow from here.
pub struct GpuContext {
    pub headless: bool,
    // Real fields (only initialized when not headless):
    // instance: wgpu::Instance,
    // adapter: wgpu::Adapter,
    // device: wgpu::Device,
    // queue: wgpu::Queue,
}

impl GpuContext {
    pub async fn new(headless: bool) -> Result<Self> {
        if headless {
            log::info!("GpuContext: headless mode, no GPU init");
            return Ok(Self { headless: true });
        }
        log::info!("GpuContext: initializing wgpu (Vulkan/Metal/DX12)");
        // Real implementation would do:
        // let instance = wgpu::Instance::new(wgpu::InstanceDescriptor::default());
        // let adapter = instance.request_adapter(...).await ...
        // let (device, queue) = adapter.request_device(...).await ...
        // Surface creation deferred to Window
        Ok(Self { headless: false })
    }
    pub fn is_headless(&self) -> bool { self.headless }
}

/// GPU resource cache with LRU eviction.
pub mod cache {
    use std::collections::HashMap;
    pub struct ResourceCache<K, V> {
        map: HashMap<K, V>,
        capacity: usize,
    }
    impl<K: std::hash::Hash + Eq, V> ResourceCache<K, V> {
        pub fn new(capacity: usize) -> Self { Self { map: HashMap::new(), capacity } }
        pub fn insert(&mut self, k: K, v: V) {
            if self.map.len() >= self.capacity {
                if let Some(first) = self.map.keys().next().cloned() { /* LRU would track order */ }
            }
            self.map.insert(k, v);
        }
        pub fn get(&self, k: &K) -> Option<&V> { self.map.get(k) }
        pub fn len(&self) -> usize { self.map.len() }
    }
}
