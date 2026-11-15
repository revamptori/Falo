"""
Placeholder for real wgpu renderer. In pure-python fallback, this mimics the interface.
When Rust extension is present, this would delegate to native.
"""
class WgpuRenderer:
    def __init__(self, config):
        self.config = config
        self._frame = 0
        self._should_close = False
        # In a real implementation we would init winit + wgpu here.
        # For fallback we just log.
        print(f"[Falo::WgpuRenderer] init (fallback stub) {config.title}")

    def pump_input(self, input_state):
        pass

    def render(self, scene, t):
        self._frame += 1
        # Real would: acquire surface, encode passes, submit
        if self._frame % 60 == 0:
            print(f"[Falo::WgpuRenderer] frame {self._frame} sprites={len(scene.sprites)} models={len(scene.models)} t={t:.2f}")

    def should_close(self): return self._should_close
    def shutdown(self): print("[Falo::WgpuRenderer] shutdown")
