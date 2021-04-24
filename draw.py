from OpenGL.GL import *
from Parser import Parser
import colors


GRID_LINE_SIZE = 100


parser = Parser()

maxDoorRot = 85
doorRot = 0
doorOpen = False
toggleDoor = False

maxWindowRot = 85
windowRot = 0
windowOpen = False
toggleWindow = False

speed = 10



def axes():
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


def grid():
    glBegin(GL_LINES)
    glColor3f(1, 1, 1)
    for z in range(-GRID_LINE_SIZE, GRID_LINE_SIZE+1, 5):
        glVertex3i(-GRID_LINE_SIZE, 0, z)
        glVertex3i(GRID_LINE_SIZE, 0, z)
        glVertex3i(z, 0, -GRID_LINE_SIZE)
        glVertex3i(z, 0, GRID_LINE_SIZE)
    glEnd()


def openCloseDoor():
    global doorOpen, doorRot, toggleDoor
    if not doorOpen:
        doorRot += speed
        if doorRot >= maxDoorRot:
            doorRot = maxDoorRot
            doorOpen = True
            toggleDoor = False
    else:
        doorRot -= speed
        if doorRot<= 0:
            doorRot = 0
            doorOpen = False
            toggleDoor = False


def door():
    glPushMatrix()
    glTranslate(34.47, -2.4, 72)
    glTranslate(6.6, 0, 0)
    glRotate(doorRot, 0, 1, 0)
    glTranslate(-6.6, 0, 0)

    glColor3fv(colors.BROWN3)
    parser.parse('porta')

    glPopMatrix()


def openCloseWindow():
    global windowOpen, windowRot, toggleWindow
    if not windowOpen:
        windowRot += speed
        if windowRot >= maxWindowRot:
            windowRot = maxWindowRot
            windowOpen = True
            toggleWindow = False
    else:
        windowRot -= speed
        if windowRot<= 0:
            windowRot = 0
            windowOpen = False
            toggleWindow = False


def window():
    glPushMatrix()
    glTranslate(-46.2, 3.6, -3.53)
    glTranslate(0, 0, -5)
    glRotate(-windowRot, 0, 1, 0)
    glTranslate(0, 0, 5)

    glColor3fv(colors.GREEN1)
    parser.parse('janela')

    glPopMatrix()
    glPushMatrix()
    glTranslate(-46.2, 3.6, 7.05)
    glTranslate(0, 0, 5)
    glRotate(windowRot, 0, 1, 0)
    glTranslate(0, 0, -5)

    glColor3fv(colors.GREEN3)
    parser.parse('janela')

    glPopMatrix()


def room():
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [.2, .6, .1, 1.])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [.7, .7, .7, 1.])
    glMaterialf(GL_FRONT, GL_SHININESS, 70)
    glColor3fv(colors.RED3)
    parser.parse('quarto')


def floorCeiling():
    glColor3fv(colors.BLUE3)
    parser.parse('chao')
#    glColor3fv(colors.ORANGE1)
#    parser.parse/teto')


def bed():
    glColor3fv(colors.BLUE2)
    parser.parse('cama')

    glColor3fv(colors.BLUE1)
    parser.parse('colchao')

    glColor3fv(colors.BROWN2)
    parser.parse('cama')


def table():
#    glColor3fv(colors.BROWN1)
#    parser.parse('mesa')
    glColor3fv(colors.ORANGE3)
    parser.parse('lixeira')
    glColor3fv(colors.BROWN3)
    parser.parse('cadeira')
    glColor3fv(colors.GREEN3)
    parser.parse('luminaria')


def all():
    room()
    door()
    window()
    floorCeiling()
    bed()
    table()



glEnable(GL_TEXTURE_2D)
parser.load('mesh/porta.obj')
parser.load('mesh/janela.obj')
parser.load('mesh/quarto.obj')
parser.load('mesh/chao.obj')
parser.load('mesh/teto.obj')

parser.load('mesh/cama/travesseiro.obj')
parser.load('mesh/cama/colchao.obj')
parser.load('mesh/cama/cama.obj')

parser.load('mesh/mesa/mesa.obj')
parser.load('mesh/mesa/lixeira.obj')
parser.load('mesh/mesa/cadeira.obj')
parser.load('mesh/mesa/luminaria.obj')
