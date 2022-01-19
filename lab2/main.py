import logging
import random

from numpy.linalg import norm
import numpy as np
from pyglet.gl import *
from pyglet import image, shapes
from pyglet.window import key

logging.basicConfig(level=logging.DEBUG)
window = pyglet.window.Window()
window.config.alpha_size = 1
bees = []
camera_position = (0.0, 0.0, 2.0)
lookAt = (0.0, 0.0, 0.0)
upVector = (0.0, 0.0, 1.0)
x = 0
y = 0
z = -20
rot_y = 0


class MyTexture:
    def __init__(self, width: int = 2, height: int = 2, x_pos: float = 0, y_pos: float = 0, z_pos: float = 0,
                 live_time: float = 60,
                 file_path: str = 'bee_1.jpg'):
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        self.pic = image.load(file_path)
        self.texture = self.pic.get_texture()
        self.angle = 0
        self.size = 1
        self.live_time = live_time
        self.draw_texture = True

    def draw(self):
        if self.live_time > 0:
            if self.calculate_distance():
                glEnable(self.texture.target)  # typically target is GL_TEXTURE_2D
                glBindTexture(self.texture.target, self.texture.id)
                '''
                matrix = (gl.GLfloat * 16)()
                gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX, matrix)
                matrix = np.reshape(matrix, (4, 4))
                right = np.array([matrix[0][0], matrix[1][0], matrix[2][0]])
                up= np.array([matrix[0][1], matrix[1][1], matrix[2][1]])
                pos = np.array([self.x_pos, self.y_pos, self.z_pos])
                pos = pos + right*np.array([-0.5, -0.5, 0]) + up * np.array([0.5, -0.5, 0])
                '''
                #glColor3f(1, 1, 1)
                self.texture.blit(self.x_pos, self.y_pos, self.z_pos, width=self.width, height=self.height)
            else:
                glPointSize(4)
                #glColor3f(1, 0, 0)
                glBegin(GL_POINTS)
                glVertex3f(self.x_pos + 1, self.y_pos + 1, self.z_pos)
                glEnd()

    def isAlive(self):
        self.live_time -= 1
        return self.live_time > 0

    def calculate_distance(self):
        global x, y, z
        distance = ((self.x_pos - x) ** 2 + (self.y_pos - y) ** 2 + (self.z_pos - z) ** 2) ** 0.5
        if distance > 20:
            return False
        else:
            return True


@window.event()
def on_draw():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    pos = [x, y, z]
    glTranslatef(*pos)
    glRotatef(rot_y, 0, 1, 0)
    for bee in bees:
        bee.draw()


@window.event
def on_key_press(symbol, modifiers):
    global x, y, z, rot_y
    if symbol == key.UP:
        z += 1
    if symbol == key.DOWN:
        z -= 1
    if symbol == key.A:
        x -= 1
    if symbol == key.D:
        x += 1
    if symbol == key.W:
        y += 1
    if symbol == key.S:
        y -= 1
    if symbol == key.E:
        rot_y += 5
    if symbol == key.Q:
        rot_y -= 5


def create_bees():
    for i in range(0, 50):
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        z = random.uniform(-10, 10)
        live = random.uniform(300, 1200)
        bees.append(MyTexture(x_pos=x, y_pos=y, z_pos=z, live_time=live))


def update_scene(dummy):
    for bee in bees:
        if not bee.isAlive():
            bees.remove(bee)


if __name__ == '__main__':
    create_bees()
    pyglet.clock.schedule_interval(update_scene, 1 / 60.0)
    pyglet.app.run()
