import numpy as np
import sys
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
cameraPositon = (1.0, 1.0, 2.0)
lookAt = (0.0, 0.0, 0.0)
upVector = (0.0, 1.0, 0.0)
width = 1200
height = 780
window = pyglet.window.Window(width, height)
t_global = 0.0
i_global = 0

points = []
polygons = []
control_points = []
B = np.array([[-1.0 / 6, 1.0 / 2, -1.0 / 2, 1.0 / 6],
              [1.0 / 2, -1.0, 1.0 / 2, 0.0],
              [-1.0 / 2, 0.0, 1.0 / 2, 0.0],
              [1.0 / 6, 4.0 / 6, 1.0 / 6, 0.0]])

dB = np.array([[-1.0 / 2, 3.0 / 2, -3.0 / 2, 1.0 / 2],
               [1.0, -5.0 / 2, 2.0, -1.0 / 2],
               [-1.0 / 2, 0.0, 1.0 / 2, 0.0],
               [0.0, 1.0, 0.0, 0.0]])


def load_object(name):
    object_file = open(name)
    for line in object_file:
        if line.startswith('v'):
            split_line = line.split()
            points.append([float(split_line[1]), float(split_line[2]), float(split_line[3])])
        if line.startswith('f'):
            split_line = line.split()
            polygons.append([int(split_line[1]), int(split_line[2]), int(split_line[3])])
    object_file.close()


def load_control_points(name):
    control_point_file = open(name)
    x_min_b = 1000.0
    y_min_b = 1000.0
    z_min_b = 1000.0

    x_max_b = -1000.0
    y_max_b = -1000.0
    z_max_b = -1000.0
    for line in control_point_file:
        split_line = line.split()
        x = float(split_line[0])
        y = float(split_line[1])
        z = float(split_line[2])
        control_points.append([x, y, z])
        x_min_b = min(x, x_min_b)
        y_min_b = min(y, y_min_b)
        z_min_b = min(z, z_min_b)
        x_max_b = max(x, x_max_b)
        y_max_b = max(y, y_max_b)
        z_max_b = max(z, z_max_b)
    control_point_file.close()

    scale_b = max(x_max_b - x_min_b, y_max_b - y_min_b, z_max_b - z_min_b)
    return scale_b


def calculate_tangent(t, R):
    T = np.array([3 * pow(t, 2), 2 * t, 1, 0])
    return (T @ B) @ R


def calculate_normal(t, R):
    T = np.array([6 * t, 2, 0, 0])
    p_dd = T @ B @ R
    return  p_dd


def calculate_binormal(t, R):
    return calculate_tangent(t, R) @ calculate_normal(t, R)


def calculate_aix(e):
    s = np.array([0.0, 0.0, 1.0])
    return np.cross(s, e)


def calculate_angle(e):
    s = np.array([0.0, 0.0, 1.0])
    return np.rad2deg(np.arccos((np.dot(s, e)) / (np.linalg.norm(s) * np.linalg.norm(e))))


def calculate_segment(t, R):
    T = np.array([pow(t, 3), pow(t, 2), t, 1])
    return (T @ B) @ R

def rotationDCM(t, R):
    w = calculate_tangent(t, R)
    u = calculate_normal(t, R)
    print(u)
    v = calculate_binormal(t, R)
    print(u)
    rot_mat = np.array([[w[0], u[0], v[0]], [w[1], u[1], v[1]], [w[2], u[2], v[2]]])
    return np.invert(rot_mat)

def draw_curve(scale_b):
    glBegin(GL_LINE_STRIP)
    for i in range(0, len(control_points) - 3):
        R = np.array([control_points[i], control_points[i + 1], control_points[i + 2], control_points[i + 3]])
        for j in range(0, 20):
            t = j / 20
            curve = calculate_segment(t, R)
            tan = calculate_tangent(t, R)
            glVertex3f(curve[0] / scale_b, curve[1] / scale_b, curve[2] / scale_b)
            #glVertex3f((curve[0] + tan[0]) / scale_b, (curve[1] + tan[1]) / scale_b, (curve[2] + tan[2]) / scale_b)
    glEnd()


def draw_tan(dot, tan):
    glBegin(GL_LINE_STRIP)
    glVertex3f(dot[0] / scale_b, dot[1] / scale_b, dot[2] / scale_b)
    glVertex3f((dot[0] + tan[0]) / scale_b, (dot[1] + tan[1]) / scale_b, (dot[2] + tan[2]) / scale_b)
    glEnd()


def draw_object():
    glBegin(GL_TRIANGLES)
    for poly in polygons:
        for point in poly:
            glColor3f(1.0, 0.0, 0.0)
            glVertex3f(points[point - 1][0], points[point - 1][1], points[point - 1][2])
    glEnd()


def update_object(x, dt):
    global t_global
    global i_global
    t_global += 0.05
    if 1 <= t_global:
        i_global += 1
        t_global = 0
    if i_global >= len(control_points) - 3:
        i_global = 0


def draw_axis(aix):
    print(aix)
    glColor3f(1.0, 1.0, 0)
    glBegin(GL_LINE_STRIP)
    glVertex3f(0, 0, 0)
    glVertex3f(aix[0], 0, 0)
    glEnd()
    glBegin(GL_LINE_STRIP)
    glVertex3f(0, 0, 0)
    glVertex3f(0, aix[1], 0)
    glEnd()
    glBegin(GL_LINE_STRIP)
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, aix[2])
    glEnd()

def dcm_rotation(scale_b):
    R = np.array([control_points[i_global], control_points[i_global + 1], control_points[i_global + 2],
                  control_points[i_global + 3]])
    vertex = calculate_segment(t_global, R)
    glLoadIdentity()
    glTranslatef(vertex[0] / scale_b, vertex[1] / scale_b, vertex[2] / scale_b)
    glMultMatrixf(rotationDCM(t_global, R))
    draw_object()

@window.event
def on_draw():
    global width
    global height
    global t_global
    R = np.array([control_points[i_global], control_points[i_global + 1], control_points[i_global + 2],
                  control_points[i_global + 3]])
    vertex = calculate_segment(t_global, R)
    tan = calculate_tangent(t_global, R)
    aix = calculate_aix(tan)
    fi = calculate_angle(tan)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(75, float(width) / float(height), 0.05, 1000)
    gluLookAt(cameraPositon[0], cameraPositon[1], cameraPositon[2],
              lookAt[0], lookAt[1], lookAt[2],
              upVector[0], upVector[1], upVector[2])
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw_curve(scale_b)
    glTranslatef(vertex[0] / scale_b, vertex[1] / scale_b, vertex[2] / scale_b)
    glScalef(1 / 5, 1 / 5, 1 / 5)
    glRotatef(fi, aix[0], aix[1], aix[2])
    draw_object()
    
    R = np.array([control_points[i_global], control_points[i_global + 1], control_points[i_global + 2],
                  control_points[i_global + 3]])
    vertex = calculate_segment(t_global, R)
    tan = calculate_tangent(t_global, R)
    aix = calculate_aix(tan)
    fi = calculate_angle(tan)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, float(width) / float(height), 0.5, 8.0)
    gluLookAt(cameraPositon[0], cameraPositon[1], cameraPositon[2],
              lookAt[0], lookAt[1], lookAt[2],
              upVector[0], upVector[1], upVector[2])
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    draw_curve(scale_b)
    #draw_tan(vertex, tan)
    glTranslatef(vertex[0] / scale_b, vertex[1] / scale_b, vertex[2] / scale_b)
    glScalef(1 / 6, 1 / 6, 1 / 6)
    glRotatef(fi, aix[0], aix[1], aix[2])
    #draw_axis(aix)
    draw_object()



if __name__ == '__main__':
    load_object('474.obj')
    scale_b = load_control_points('b_spline.obj')
    pyglet.clock.schedule(update_object, 1 / 100.0)
    pyglet.app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
