class HeadlessRenderer:
    def __init__(self, config):
        self.config = config
        self._frame = 0
        print(f"[Falo::Headless] no window, no GPU — logic-only")

    def pump_input(self, input_state): pass
    def render(self, scene, t):
        self._frame += 1
        if self._frame % 10 == 0:
            print(f"[Falo::Headless] frame {self._frame} t={t:.2f} sprites={len(scene.sprites)} models={len(scene.models)}")
    def should_close(self): return False
    def shutdown(self): print("[Falo::Headless] shutdown")
