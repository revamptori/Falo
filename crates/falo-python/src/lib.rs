use pyo3::prelude::*;

/// PyO3 bindings. Real engine exposes bulk APIs to avoid per-frame Python overhead.
/// This crate is optional; Rust-only games omit it.
#[pyclass]
pub struct PyGame { pub title: String }
#[pymethods]
impl PyGame {
    #[new]
    fn new(title: String) -> Self { Self { title } }
    fn run(&self) { log::info!("PyGame run {}", self.title); }
}

#[pymodule]
fn falo_python(m: &Bound<PyModule>) -> PyResult<()> {
    m.add_class::<PyGame>()?;
    Ok(())
}
