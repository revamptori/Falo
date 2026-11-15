// Criterion bench — sprite batching (requires Rust toolchain)
// Run with: cargo bench --workspace
use criterion::{Criterion, criterion_group, criterion_main};

fn bench_sprite_batch(c: &mut Criterion) {
    c.bench_function("sprite_batch 10k", |b| {
        b.iter(|| {
            // Simulated: falo_renderer_2d::SpriteBatch with 10k sprites
            let batch = 0; // placeholder
            criterion::black_box(batch);
        })
    });
}
criterion_group!(benches, bench_sprite_batch);
criterion_main!(benches);
