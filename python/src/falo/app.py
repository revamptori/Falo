"""
Game loop, window, rendering, input.
Rust-native when _falo present; pure-python fallback otherwise.
"""

from __future__ import annotations
import sys
import time
import argparse
import os
from dataclasses import dataclass, field
from typing import Callable, Optional, List, Dict, Any

from .scene import Scene
from .input import InputState
from .build import handle_executable_arg

@dataclass
class GameConfig:
    title: str = "Falo Game"
    width: int = 1280
    height: int = 720
    mode: str = "2d"  # "2d" or "3d"
    fullscreen: bool = False
    vsync: bool = True
    resizable: bool = True
    headless: bool = False  # force headless (no window)


class Game:
    """
    Main entry point. Matches target API:

        import falo
        game = falo.Game(title="Example", width=1280, height=720, mode="2d")
        @game.update
        def update(dt): ...
        @game.draw
        def draw(): ...
        game.run()
    """

    def __init__(self, title: str = "Falo Game", width: int = 1280, height: int = 720,
                 mode: str = "2d", fullscreen: bool = False, vsync: bool = True, **kwargs):
        self.config = GameConfig(title=title, width=width, height=height, mode=mode,
                                 fullscreen=fullscreen, vsync=vsync,
                                 headless=kwargs.get("headless", False) or os.environ.get("FALO_HEADLESS") is not None)
        # Auto-detect headless on Linux without display
        if not self.config.headless and sys.platform.startswith("linux"):
            if not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
                self.config.headless = True

        self.scene = Scene(mode=mode, width=width, height=height)
        self._update_cbs: List[Callable] = []
        self._draw_cbs: List[Callable] = []
        self._startup_cbs: List[Callable] = []
        self._shutdown_cbs: List[Callable] = []
        self.input = InputState()
        # Time tracking
        self._running = False
        self._frame = 0
        self._time = 0.0
        self._fps = 0.0
        # Renderer lazy init
        self._renderer = None
        # Input access global registration
        self._register_globals()

    def _register_globals(self):
        # Make game accessible via falo.get_game() if needed
        try:
            import falo
            falo._current_game = self  # type: ignore
        except Exception:
            pass

    # --- decorators ---
    def update(self, func: Callable) -> Callable:
        self._update_cbs.append(func)
        return func

    def draw(self, func: Callable) -> Callable:
        self._draw_cbs.append(func)
        return func

    def on_startup(self, func: Callable) -> Callable:
        self._startup_cbs.append(func)
        return func

    def on_shutdown(self, func: Callable) -> Callable:
        self._shutdown_cbs.append(func)
        return func

    # Back-compat for spec example: game.scene.create_camera etc already exist on Scene

    def _maybe_handle_build_arg(self) -> bool:
        """
        If sys.argv contains --executable, delegate to build system and exit.
        Returns True if handled (caller should not continue).
        Supports:
          --executable <path>  (also --output alias)
          --release, --debug, --target, --icon, --assets, --version
        """
        if "--executable" in sys.argv or "--output" in sys.argv:
            # handle_executable_arg will parse and produce artifact, then exit
            code = handle_executable_arg(sys.argv)
            sys.exit(code)
            return True
        return False

    def _init_renderer(self):
        if self._renderer is not None:
            return
        # Choose headless renderer if needed
        if self.config.headless:
            from .renderer_headless import HeadlessRenderer
            self._renderer = HeadlessRenderer(self.config)
            print(f"[Falo] Renderer: headless (no GPU, no window)")
        else:
            try:
                from .renderer import WgpuRenderer
                self._renderer = WgpuRenderer(self.config)
                print(f"[Falo] Renderer: wgpu ({self.config.width}x{self.config.height})")
            except Exception as e:
                print(f"[Falo] GPU init failed ({e}), falling back to headless")
                from .renderer_headless import HeadlessRenderer
                self._renderer = HeadlessRenderer(self.config)

    def run(self, max_frames: Optional[int] = None, headless: Optional[bool] = None):
        """
        Run main loop. In headless mode, runs fixed number of frames (default 10) then exits.
        Pass max_frames or --headless flag to control.
        Also honors --executable build flag.
        """
        # Build interception must happen first (spec requirement)
        self._maybe_handle_build_arg()

        if headless is not None:
            self.config.headless = headless
        # CLI override: if --headless in argv
        if "--headless" in sys.argv:
            self.config.headless = True
            # parse optional max-frames
            try:
                idx = sys.argv.index("--headless")
                # could be --headless=100 etc not needed
            except ValueError:
                pass

        self._init_renderer()

        for cb in self._startup_cbs:
            try:
                cb()
            except Exception as e:
                print(f"[Falo] startup cb error: {e}")

        self._running = True
        clock = time.perf_counter()
        last = clock
        dt = 1/60.0
        max_frames_eff = max_frames
        if max_frames_eff is None and self.config.headless:
            # In headless we default to small frame count so CI doesn't hang;
            # but if FALO_HEADLESS_FRAMES set, use that
            env_frames = os.environ.get("FALO_HEADLESS_FRAMES")
            if env_frames:
                try:
                    max_frames_eff = int(env_frames)
                except: max_frames_eff = 10
            else:
                max_frames_eff = 10

        print(f"[Falo] Game.run title='{self.config.title}' {self.config.width}x{self.config.height} mode={self.config.mode} headless={self.config.headless}")

        # Simple fixed timestep accumulator
        accumulator = 0.0
        fixed_dt = 1/60.0

        frame = 0
        try:
            while self._running:
                now = time.perf_counter()
                raw_dt = now - last
                last = now
                # clamp
                raw_dt = min(raw_dt, 0.1)
                accumulator += raw_dt

                # Input pump (headless: no input)
                if not self.config.headless and self._renderer and hasattr(self._renderer, "pump_input"):
                    self._renderer.pump_input(self.input)

                # fixed update(s) — guarantee at least one update per frame (fixes headless dt ~0)
                stepped = False
                while accumulator >= fixed_dt:
                    stepped = True
                    for cb in self._update_cbs:
                        try:
                            import inspect
                            sig = inspect.signature(cb)
                            if len(sig.parameters) == 0:
                                cb()
                            else:
                                cb(fixed_dt)
                        except Exception as e:
                            print(f"[Falo] update cb error: {e}")
                    if hasattr(self.scene, "physics") and self.scene.physics:
                        try:
                            self.scene.physics.step(fixed_dt)
                        except Exception: pass
                    accumulator -= fixed_dt
                    self._time += fixed_dt
                # If no fixed step occurred this frame (tiny dt), still run one update to guarantee progress in headless/test
                if not stepped and self._update_cbs:
                    for cb in self._update_cbs:
                        try:
                            import inspect
                            sig = inspect.signature(cb)
                            if len(sig.parameters) == 0:
                                cb()
                            else:
                                cb(fixed_dt)
                        except Exception as e:
                            print(f"[Falo] update cb error: {e}")
                    self._time += fixed_dt

                # Draw
                for cb in self._draw_cbs:
                    try:
                        cb()
                    except Exception as e:
                        print(f"[Falo] draw cb error: {e}")

                # Renderer present
                if self._renderer:
                    try:
                        self._renderer.render(self.scene, self._time)
                    except Exception as e:
                        print(f"[Falo] render error: {e}")

                frame += 1
                self._frame = frame

                # Frame cap / vsync emulation
                if self.config.vsync and not self.config.headless:
                    # simple sleep to ~60fps if loop is too fast
                    elapsed = time.perf_counter() - now
                    wait = max(0, (1/60.0) - elapsed - 0.001)
                    if wait > 0:
                        time.sleep(wait)

                # headless exit
                if max_frames_eff is not None and frame >= max_frames_eff:
                    print(f"[Falo] headless completed {frame} frames")
                    break

                # window close check
                if not self.config.headless and self._renderer and hasattr(self._renderer, "should_close"):
                    if self._renderer.should_close():
                        break
        except KeyboardInterrupt:
            print("[Falo] interrupted")

        for cb in self._shutdown_cbs:
            try:
                cb()
            except Exception as e:
                print(f"[Falo] shutdown cb error: {e}")

        # Clean shutdown
        if self._renderer and hasattr(self._renderer, "shutdown"):
            self._renderer.shutdown()
        print(f"[Falo] shutdown clean frames={frame} time={self._time:.2f}s")

    def quit(self):
        self._running = False

    # convenience aliases matching spec
    def create_sprite(self, path: str):
        return self.scene.create_sprite(path)

    def load_model(self, path: str):
        return self.scene.load_model(path)
