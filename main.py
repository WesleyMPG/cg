from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Parser import Parser
import colors, draw

W, H = 1280, 720
FOV_Y = 75

ortho = False
cam_x, cam_y, cam_z = 60, 37, 94
center_x, center_y, center_z = 5, 0, 0
def setup_cam():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    n = 80
    if ortho:
        glOrtho(-n, n, -n, n, 0, 500)
    else:
        gluPerspective(FOV_Y, W/H, 0.001, 1000)


def setup_lights():
    ambient_light = [.2, .2, .2, 1]
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_light)
    glShadeModel(GL_SMOOTH)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [.1, .1, .1, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_POSITION, [20, 50, 10])



def keyboard(key, x, y):
    global cam_x, cam_y, cam_z, ortho, toggleDoor,\
        center_x, center_y, center_z
    right = 120
    front = 160
    top = 100
    if key == b't':
        cam_x, cam_y, cam_z = 0.0000001, top, 0
    elif key == b'T':
        cam_x, cam_y, cam_z = 0.0000001, -top, 0
    elif key == b'l':
        cam_x, cam_y, cam_z = -right, 0, 0
    elif key == b'r':
        cam_x, cam_y, cam_z = right, 0, 0
    elif key == b'f':
        cam_x, cam_y, cam_z = 0, 0, front
    elif key == b'b':
        cam_x, cam_y, cam_z = 0, 0, -front
    elif key == b'n':
        cam_x, cam_y, cam_z = 2, 7, 7
    elif key == b'o':
        ortho = not ortho
        setup_cam()
    elif key == b'y':
        cam_y += 1
    elif key == b'Y':
        cam_y -= 1
    elif key == b'z':
        cam_z += 1
    elif key == b'Z':
        cam_z -= 1
    elif key == b'x':
        cam_x += 1
    elif key == b'X':
        cam_x -= 1
    elif key == b'8':
        center_y += 1
    elif key == b'2':
        center_y -= 1
    elif key == b'4':
        center_x -= 1
    elif key == b'6':
        center_x += 1
    elif key == b'3':
        center_z += 1
    elif key == b'1':
        center_z -= 1
    elif key == b'd':
        draw.toggleDoor = True
    elif key == b'w':
        draw.toggleWindow = True


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(cam_x, cam_y, cam_z, center_x, center_y, center_z,
              0, 1, 0)
    draw.axes()
#    drawGrid()

    if draw.toggleDoor:
        draw.openCloseDoor()
    if draw.toggleWindow:
        draw.openCloseWindow()

    draw.all()

    glutSwapBuffers()


def init():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(W, H)
    glutCreateWindow('shape')

    glutDisplayFunc(display)
    glutIdleFunc(glutPostRedisplay)
    glutKeyboardFunc(keyboard)

    setup_cam()
    glEnable(GL_DEPTH_TEST)
    setup_lights()

    glutMainLoop()


init()
