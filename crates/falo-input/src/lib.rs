use std::collections::{HashMap, HashSet};

#[derive(Debug, Default)]
pub struct InputState {
    pressed: HashSet<String>,
    just_pressed: HashSet<String>,
    just_released: HashSet<String>,
    mouse_pos: (f32, f32),
    mouse_delta: (f32, f32),
    scroll: f32,
}

impl InputState {
    pub fn new() -> Self { Self::default() }
    pub fn is_pressed(&self, key: &str) -> bool { self.pressed.contains(&key.to_uppercase()) }
    pub fn just_pressed(&self, key: &str) -> bool { self.just_pressed.contains(&key.to_uppercase()) }
    pub fn just_released(&self, key: &str) -> bool { self.just_released.contains(&key.to_uppercase()) }
    pub fn mouse_position(&self) -> (f32,f32) { self.mouse_pos }
    pub fn set_pressed(&mut self, key: &str, down: bool) {
        let k = key.to_uppercase();
        if down { self.pressed.insert(k.clone()); self.just_pressed.insert(k); } else { self.pressed.remove(&k); self.just_released.insert(k); }
    }
    pub fn update(&mut self) { self.just_pressed.clear(); self.just_released.clear(); self.mouse_delta = (0.0,0.0); }
}

/// Action mapping (high-level)
#[derive(Debug, Clone)]
pub struct InputAction { pub name: String, pub keys: Vec<String>, pub gamepad_buttons: Vec<u8> }
pub struct ActionMap { pub actions: HashMap<String, InputAction> }
impl ActionMap {
    pub fn new() -> Self { Self { actions: HashMap::new() } }
    pub fn bind(&mut self, name: &str, keys: &[&str]) { self.actions.insert(name.into(), InputAction { name: name.into(), keys: keys.iter().map(|s| s.to_string()).collect(), gamepad_buttons: vec![] }); }
    pub fn is_active(&self, name: &str, state: &InputState) -> bool {
        self.actions.get(name).map(|a| a.keys.iter().any(|k| state.is_pressed(k))).unwrap_or(false)
    }
}
