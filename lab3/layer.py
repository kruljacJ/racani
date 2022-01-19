from abc import ABC, abstractmethod
from typing import List
import random
import math
from bullet import ShipBullet, EnemyBullet
from enemy import Enemy


class Layer(ABC):
    @abstractmethod
    def create_enemies(self) -> List[Enemy]:
        pass

    @abstractmethod
    def check_bullet(self, bullet: ShipBullet):
        pass

    @abstractmethod
    def update_layer(self) -> List[EnemyBullet]:
        pass

    @abstractmethod
    def draw_layer(self):
        pass


class CircleLayer(Layer):
    def __init__(self, min_y: int, max_y: int, num_enemy: int = 5, window_width: int = 700):
        self.num_enemy = num_enemy
        self.min_y = min_y
        self.max_y = max_y
        self.window_width = window_width
        self.dea = 5
        self.enemies = self.create_enemies()
        self.test = 0

    def create_enemies(self) -> List[Enemy]:
        enemies = []
        x = self.window_width / self.num_enemy
        for i in range(self.num_enemy):
            angle = random.uniform(0, math.pi)
            speed = random.uniform(1, 3)
            enemies.append(Enemy(x_pos=i * x + 50, y_pos=self.min_y + 10, angle=angle, speed=speed))
        return enemies

    def check_bullet(self, bullet: ShipBullet):
        if self.min_y < bullet.y_pos < self.max_y:
            for enemy in self.enemies.copy():
                if enemy.is_shoot(bullet):
                    self.enemies.remove(enemy)
                    return True
        return False

    def update_layer(self) -> List[EnemyBullet]:
        bullets = []
        for index, enemy in enumerate(self.enemies):
            enemy.update_angle(self.dea)
            enemy.move()
            bullet = enemy.shoot_ship()
            if bullet is not None:
                bullets.append(bullet)
        return bullets

    def draw_layer(self):
        for enemy in self.enemies:
            enemy.draw()


class LinearLayer(Layer):

    def __init__(self, min_y: int, max_y: int, num_enemy: int = 5, window_width: int = 700):
        self.num_enemy = num_enemy
        self.min_y = min_y
        self.max_y = max_y
        self.window_width = window_width
        self.enemies = self.create_enemies()

    def create_enemies(self) -> List[Enemy]:
        enemies = []
        x = self.window_width / self.num_enemy
        angle = random.uniform(0, math.pi * 2)
        for i in range(self.num_enemy):
            enemies.append(Enemy(x_pos=i * x + 10, y_pos=(self.max_y + self.min_y) / 2, angle=angle))
        return enemies

    def check_bullet(self, bullet: ShipBullet):
        if self.min_y < bullet.y_pos < self.max_y:
            for enemy in self.enemies.copy():
                if enemy.is_shoot(bullet):
                    self.enemies.remove(enemy)
                    return True
        return False

    def update_layer(self) -> List[EnemyBullet]:
        bullets = []
        need_change = self.enemies[0].check_walls(y_min=self.min_y, y_max=self.max_y, x_max=self.window_width)
        if need_change == '-':
            need_change = self.enemies[-1].check_walls(y_min=self.min_y, y_max=self.max_y, x_max=self.window_width)
        for index, enemy in enumerate(self.enemies):
            if need_change == 'x':
                enemy.angle = math.pi - enemy.angle
            elif need_change == 'y':
                enemy.angle *= -1
            enemy.check_angle()
            enemy.move()
            bullet = enemy.shoot_ship()
            if bullet is not None:
                bullets.append(bullet)
        return bullets

    def draw_layer(self):
        for enemy in self.enemies:
            enemy.draw()


class BossLayer(Layer):

    def __init__(self, min_y: int, max_y: int, num_enemy: int = 5, window_width: int = 700):
        self.num_enemy = num_enemy
        self.min_y = min_y
        self.max_y = max_y
        self.window_width = window_width
        self.enemies = self.create_enemies()

    def create_enemies(self) -> List[Enemy]:
        boss1 = Enemy(width=120, height=120, x_pos=50, y_pos=(self.min_y+self.max_y)/2, angle=math.radians(20), life=5)
        boss2 = Enemy(width=120, height=120, x_pos=self.window_width - 200, y_pos=(self.min_y+self.max_y)/2,
                      angle=math.radians(170), life=5)
        return [boss1, boss2]

    def check_bullet(self, bullet: ShipBullet):
        if self.min_y < bullet.y_pos < self.max_y:

            for enemy in self.enemies.copy():
                if enemy.is_shoot(bullet):

                    enemy.life -= 1
                    if enemy.life < 1:
                        self.enemies.remove(enemy)
                    return True
        return False

    def update_layer(self) -> List[EnemyBullet]:
        bullets = []
        for index, enemy in enumerate(self.enemies):
            need_change = enemy.check_walls(y_max=self.max_y, y_min=self.min_y, x_max=self.window_width)
            if need_change == 'x':
                enemy.angle = math.pi - enemy.angle
            elif need_change == 'y':
                enemy.angle *= -1
            enemy.check_angle()
            enemy.move()
            enemy.check_collision(self.enemies)
            bullet = enemy.shoot_ship()
            if bullet is not None:
                bullets.append(bullet)
        return bullets

    def draw_layer(self):
        for enemy in self.enemies:
            enemy.draw()
