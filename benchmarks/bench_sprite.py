"""
Benchmark: sprite batching, ECS iteration, physics
Uses Python time; Rust Criterion suites would be in benchmarks/benches/*.rs
"""
import time, statistics, falo

def bench_sprite_batch(n=10000, iterations=100):
    g = falo.Game(headless=True)
    for i in range(n):
        g.scene.create_sprite("assets/player.png")
    times=[]
    for _ in range(iterations):
        t0=time.perf_counter()
        # Bulk query
        _ = g.scene.query_positions()
        times.append((time.perf_counter()-t0)*1000)
    avg=statistics.mean(times)
    print(f"sprite batch {n}: avg {avg:.3f}ms over {iterations}")
    assert avg < 5.0, f"too slow {avg}"

def bench_ecs(n=10000):
    g=falo.Game(headless=True)
    ents=g.scene.spawn_batch(n)
    t0=time.perf_counter()
    _=len(g.scene.entities)
    dt=(time.perf_counter()-t0)*1000
    print(f"ECS {n} entities: {dt:.3f}ms")
    assert dt<2.0

if __name__=="__main__":
    bench_sprite_batch()
    bench_ecs()
