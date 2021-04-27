from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from Parser import Parser
from PIL import Image as plImage

W, H = 800, 600
GRID_LINE_SIZE = 25
FOV_Y = 75

parser = Parser()


ortho = False
cam_x, cam_y, cam_z = 2, 7, 7
center_x, center_y, center_z = 0, 0, 0
def setup_cam():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if ortho:
        glOrtho(-8, 8, -8, 8, 0, 50)
    else:
        gluPerspective(FOV_Y, W/H, 0.001, 1000)


def setup_lights():
    ambient_light = [.3, .3, .3, 1]
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient_light)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [.2, .2, .2, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_POSITION, [5, 10, 12])


def keyboard(key, x, y):
    global cam_x, cam_y, cam_z, ortho
    distance = 10
    if key == b't':
        cam_x, cam_y, cam_z = 0.0000001, 20, 0
    elif key == b'l':
        cam_x, cam_y, cam_z = -distance, 0, 0
    elif key == b'r':
        cam_x, cam_y, cam_z = distance, 0, 0
    elif key == b'f':
        cam_x, cam_y, cam_z = 0, 0, distance
    elif key == b'b':
        cam_x, cam_y, cam_z = 0, 0, -distance
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


def drawAxes():
    glBegin(GL_LINES)
    # X
    glColor3f(1, 0, 0)
    glVertex3i(0, 0, 0)
    glVertex3i(GRID_LINE_SIZE, 0, 0)

    # Y
    glColor3f(0, 1, 0)
    glVertex3i(0, 0, 0)
    glVertex3i(0, GRID_LINE_SIZE, 0)

    # z
    glColor3f(0, 0, 1)
    glVertex3i(0, 0, 0)
    glVertex3i(0, 0, GRID_LINE_SIZE)

    glEnd()


def drawGrid():
    glBegin(GL_LINES)
    glColor4f(1, 1, 1, .5)
    for z in range(-GRID_LINE_SIZE, GRID_LINE_SIZE+1):
        if z == 0: continue
        glVertex3i(-GRID_LINE_SIZE, 0, z)
        glVertex3i(GRID_LINE_SIZE, 0, z)
        glVertex3i(z, 0, -GRID_LINE_SIZE)
        glVertex3i(z, 0, GRID_LINE_SIZE)
    glEnd()


def load_texture(path, qtd):
    texture = plImage.open(path)
    data = texture.tobytes('raw', 'RGB', 0)
    w, h = texture.size[0], texture.size[1]

    textId = glGenTextures(qtd)
    formato = GL_RGB
    glBindTexture(GL_TEXTURE_2D, textId)
    glTexImage2D(GL_TEXTURE_2D, 0, formato,
                 w, h, 0, formato, GL_UNSIGNED_BYTE, data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return textId


def drawTex():
    global tg, tg2
    glBindTexture(GL_TEXTURE_2D, tg)
    parser.parse('teste1', texture=True)

    glPushMatrix()

    glColor3fv([1, 1, 1])
    glTranslate(2, 0, 0)
    glBindTexture(GL_TEXTURE_2D, tg2)
    parser.parse('teste1', texture=True)

    glPopMatrix()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(cam_x, cam_y, cam_z, center_x, center_y, center_z,
              0, 1, 0)

    drawAxes()
    drawGrid()
    drawTex()

    glutSwapBuffers()


tg = 0
tg2 = 0
def main():
    global tg, tg2
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(W, H)
    glutCreateWindow('projeto')
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    glutDisplayFunc(display)
    glutIdleFunc(glutPostRedisplay)
    glutKeyboardFunc(keyboard)
    setup_cam()
    setup_lights()
    tg = load_texture('tx1.png', 1)
    tg2 = load_texture('madeira2.jpg', 1)

    glutMainLoop()


parser.load('teste1.obj')
main()

