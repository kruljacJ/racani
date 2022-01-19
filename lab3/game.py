from pyglet.gl import *
from pyglet.window import key


from layer import Layer, CircleLayer, LinearLayer, BossLayer
from space_ship import SpaceShip


win_width = 700
win_height = 700
window = pyglet.window.Window(win_width, win_height)
keyboard = {}


class Game:
    def __init__(self, layers, space_ship: SpaceShip):
        self.layers = layers
        self.enemy_bullets = []
        self.space_ship = space_ship
        self.space_ship_bullets = []


@window.event()
def on_draw():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    window.clear()
    for bullet in game.enemy_bullets:
        bullet.draw()
    for layer in game.layers:
        layer.draw_layer()

    for bullet in game.space_ship_bullets:
        bullet.draw()
    game.space_ship.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        if len(game.space_ship_bullets) < 10:
            game.space_ship_bullets.append(game.space_ship.fire())
    keyboard[symbol] = True


@window.event
def on_key_release(symbol, modifiers):
    try:
        del keyboard[symbol]
    except:
        pass


def update_scene(dummy):
    if key.A in keyboard.keys():
        game.space_ship.x_pos -= 10
    if key.D in keyboard.keys():
        game.space_ship.x_pos += 10
    if key.W in keyboard.keys():
        game.space_ship.y_pos += 10
    if key.S in keyboard.keys():
        game.space_ship.y_pos -= 10

    for layer in game.layers:
        bullets = layer.update_layer()
        if len(bullets) > 0:
            game.enemy_bullets = [*game.enemy_bullets.copy(), *bullets]

    for bullet in game.enemy_bullets.copy():
        if not bullet.update_position():
            game.enemy_bullets.remove(bullet)
        else:
            if game.space_ship.is_shoot(bullet):
                game.enemy_bullets.remove(bullet)

    for bullet in game.space_ship_bullets.copy():
        if not bullet.update_position():
            game.space_ship_bullets.remove(bullet)
        else:
            for layer in game.layers.copy():
                if layer.check_bullet(bullet):
                    game.space_ship_bullets.remove(bullet)
                    if len(layer.enemies) == 0:
                        game.layers.remove(layer)

    if not game.space_ship.isAlive() or len(game.layers) == 0:
        exit(0)


if __name__ == '__main__':
    # game = Game([CircleLayer(min_y=300, max_y=500), LinearLayer(min_y=500, max_y=700)], SpaceShip(x_pos=win_width / 2 - 25, y_pos=10))
    game = Game([LinearLayer(min_y=200, max_y=400, num_enemy=3), BossLayer(min_y=400, max_y=700)], SpaceShip(x_pos=win_width / 2 - 25, y_pos=10))
    pyglet.clock.schedule_interval(update_scene, 1 / 60.0)
    pyglet.app.run()
