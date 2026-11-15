import falo

game = falo.Game(title="Basic 2D", width=800, height=600, mode="2d")
sprite = game.scene.create_sprite("assets/player.png")
sprite.position = (400, 300)

@game.update
def update(dt):
    if falo.keyboard.is_pressed("LEFT"):
        sprite.move(-100*dt, 0)
    if falo.keyboard.is_pressed("RIGHT"):
        sprite.move(100*dt, 0)

game.run()
