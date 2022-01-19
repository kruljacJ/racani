from pyglet import image
from pyglet.gl import *
from abc import ABC, abstractmethod


class Bullet(ABC):
    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update_position(self) -> bool:
        pass


class ShipBullet(Bullet):
    def __init__(self, x_pos: float = 0, y_pos: float = 0, bullet_speed: float = 7.0, win_height: int = 700):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.bullet_speed = bullet_speed
        self.win_height = win_height
        self.texture = image.load('laser.jpg').get_texture()

    def draw(self):
        glEnable(self.texture.target)  # typically target is GL_TEXTURE_2D
        glBindTexture(self.texture.target, self.texture.id)
        self.texture.blit(round(self.x_pos), round(self.y_pos), width=10, height=15)

    def update_position(self):
        self.y_pos += self.bullet_speed
        if self.y_pos > self.win_height:
            return False
        return True


class EnemyBullet(Bullet):
    def __init__(self, x_pos: float = 0, y_pos: float = 0, bullet_speed: float = 3.0):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.bullet_speed = bullet_speed
        self.texture = image.load('egg.png').get_texture()

    def draw(self):
        glEnable(self.texture.target)  # typically target is GL_TEXTURE_2D
        glBindTexture(self.texture.target, self.texture.id)
        self.texture.blit(round(self.x_pos), round(self.y_pos), width=10, height=15)

    def update_position(self):
        self.y_pos -= self.bullet_speed
        if self.y_pos <= 0:
            return False
        return True
