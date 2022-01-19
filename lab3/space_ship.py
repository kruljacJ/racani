from pyglet import image
from pyglet.gl import *
from bullet import ShipBullet, EnemyBullet


class SpaceShip:
    def __init__(self, width: int = 50, height: int = 50, x_pos: float = 0, y_pos: float = 0,
                 file_path: str = 'ship.jpg'):
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.pic = image.load(file_path)
        self.texture = self.pic.get_texture()
        self.live = 3
        self.bullets = []

    def draw(self):
        glEnable(self.texture.target)  # typically target is GL_TEXTURE_2D
        glBindTexture(self.texture.target, self.texture.id)
        self.texture.blit(self.x_pos, self.y_pos, width=self.width, height=self.height)

    def isAlive(self):
        return self.live > 0

    def fire(self):
        return ShipBullet(x_pos=self.x_pos + self.width / 2 - 5, y_pos=self.y_pos + self.height, win_height=700)

    def is_shoot(self, bullet: EnemyBullet):
        if self.x_pos < bullet.x_pos < self.x_pos + self.width and self.y_pos < bullet.y_pos < self.y_pos + self.height:
            self.live -= 1
            return True
        return False
