pub use bevy_ecs::prelude::*;

#[derive(Resource, Debug, Clone)]
pub struct EcsStats { pub entity_count: usize, pub system_count: usize }

pub fn create_world() -> World { let mut w = World::new(); w.insert_resource(EcsStats { entity_count: 0, system_count: 0 }); w }

/// Bulk operations for Python bridge - avoid per-entity Python calls.
pub mod bulk {
    use super::*;
    pub fn spawn_batch(world: &mut World, count: usize) -> Vec<Entity> {
        let mut entities = Vec::with_capacity(count);
        for _ in 0..count { entities.push(world.spawn_empty().id()); }
        entities
    }
}
