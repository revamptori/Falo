use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UiStyle { pub bg: [f32;4], pub fg: [f32;4], pub font_size: f32 }
impl Default for UiStyle { fn default() -> Self { Self { bg: [0.1,0.1,0.1,1.0], fg: [1.0,1.0,1.0,1.0], font_size: 14.0 } } }

pub enum Widget { Panel { children: Vec<Widget> }, Button { label: String, on_click: Option<String> }, Label { text: String }, Slider { value: f32, min: f32, max: f32 }, Progress { value: f32 } }

pub struct UiCanvas { pub widgets: Vec<Widget>, pub style: UiStyle }
impl UiCanvas {
    pub fn new() -> Self { Self { widgets: vec![], style: UiStyle::default() } }
    pub fn add(&mut self, w: Widget) { self.widgets.push(w); }
}
