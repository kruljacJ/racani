import math
import random
from pyglet import image
from pyglet.gl import *
from bullet import EnemyBullet, ShipBullet


class Enemy:
    def __init__(self, width: int = 50, height: int = 50, x_pos: float = 0, y_pos: float = 0, dx=1, angle: float = 0,
                 file_path: str = 'chicken.jpg', speed=2, life:int = 1):
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        cx = self.x_pos + self.width / 2
        cy = self.y_pos + self.height / 2
        self.r = math.sqrt((cx-self.x_pos)**2 + (cy - self.y_pos)**2)
        self.angle = angle
        self.shoot_time = random.uniform(50, 1000)
        self.last_bullet = 0
        self.dx = dx
        self.pic = image.load(file_path)
        self.texture = self.pic.get_texture()
        self.life = life
        self.bullets = []
        self.collisions_time = {}
        self.speed = speed

    def draw(self):
        glEnable(self.texture.target)  # typically target is GL_TEXTURE_2D
        glBindTexture(self.texture.target, self.texture.id)
        self.texture.blit(round(self.x_pos), round(self.y_pos), width=self.width, height=self.height)


    def is_shoot(self, bullet: ShipBullet):
        return self.x_pos < bullet.x_pos < self.x_pos + self.width and self.y_pos < bullet.y_pos < self.y_pos + self.height

    def move(self):
        self.y_pos += math.sin(self.angle) * self.speed
        self.x_pos += math.cos(self.angle) * self.speed
        self.check_angle()

    def update_angle(self, dA):
        self.angle += math.radians(dA)
        self.check_angle()

    def check_angle(self):
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi
        if self.angle < 0:
            self.angle += 2 * math.pi

    def check_walls(self, y_min, y_max, x_max):
        if self.x_pos + self.width >= x_max or self.x_pos <= 0:
            return 'x'
        if self.y_pos + self.height >= y_max or self.y_pos <= y_min:
            return 'y'
        return '-'

    def shoot_ship(self):
        if self.last_bullet >= self.shoot_time:
            bullet = EnemyBullet(x_pos=self.x_pos + self.width / 2, y_pos=self.y_pos)
            self.bullets.append(bullet)
            self.last_bullet = 0
            return bullet
        else:
            self.last_bullet += 1
            return None

    def calculate_if_collision(self, enemy):
        if enemy in self.collisions_time and self.collisions_time[enemy] < 20:
            return False
        e_cx = enemy.x_pos + enemy.width / 2
        e_cy = enemy.y_pos + enemy.height / 2
        cx = self.x_pos + self.width / 2
        cy = self.y_pos + self.height / 2
        if e_cx == cx and e_cy == cy:
            return False
        return math.sqrt((e_cx - cx) ** 2 + (e_cy - cy) ** 2) <= self.r + enemy.r

    def collision_notify(self, enemy):
        if 3 * math.pi / 4 < self.angle < 5 * math.pi / 4 or self.angle < math.pi / 2 or self.angle > 7 * math.pi / 4:
            self.angle = math.pi - self.angle
        else:
            self.angle *= -1
        if self.angle < 0:
            self.angle += math.pi * 2
        self.collisions_time[enemy] = 0

    def check_collision(self, enemies):
        for k in self.collisions_time:
            self.collisions_time[k] += 1
        for enemy in enemies:
            if self.calculate_if_collision(enemy):
                if 3 * math.pi / 4 < self.angle < 5 * math.pi / 4 or self.angle < math.pi / 4 or self.angle > 7 * math.pi / 4:
                    self.angle = math.pi - self.angle
                    enemy.collision_notify(self)
                else:
                    self.angle *= -1
                    enemy.collision_notify(self)
                self.collisions_time[enemy] = 0
        if self.angle < 0:
            self.angle += 2 * math.pi
