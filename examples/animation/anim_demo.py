from falo import Game
import falo
from falo.animation import AnimationClip, Animator

game = falo.Game(title="Animation Demo", width=800, height=600, mode="2d")
clip = AnimationClip(name="walk", duration=1.5, looped=True)
anim = Animator()
anim.play("walk")

@game.update
def update(dt):
    anim.update(dt)
    print(f"anim time={anim.time:.2f} clip={anim.current}")

game.run(headless=True, max_frames=3)
