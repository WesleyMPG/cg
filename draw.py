from OpenGL.GL import *
from PIL import Image as plImage
from Parser import Parser
from contextlib import contextmanager
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

fanRot = 0


def axes():
    """Desenha os eixos para ajudar no posicionamento"""
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
    """Desenha uma grade para ajudar no posicionamento"""
    glBegin(GL_LINES)
    glColor3f(1, 1, 1)
    for z in range(-GRID_LINE_SIZE, GRID_LINE_SIZE+1, 5):
        glVertex3i(-GRID_LINE_SIZE, 0, z)
        glVertex3i(GRID_LINE_SIZE, 0, z)
        glVertex3i(z, 0, -GRID_LINE_SIZE)
        glVertex3i(z, 0, GRID_LINE_SIZE)
    glEnd()


def load_texture(path):
    texture = plImage.open(path)
    data = texture.tobytes('raw', 'RGB', 0, -1)
    w, h = texture.size[0], texture.size[1]

    textId = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textId)
    formato = GL_RGB
    glTexImage2D(GL_TEXTURE_2D, 0, formato,
             w, h, 0, formato, GL_UNSIGNED_BYTE, data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return textId


@contextmanager
def apply_texture(name):
    """Permite a utilização do bloco with para aplicar a textura
        e ao final(com finally) do bloco remove a textura
    """
    glColor3fv([1,1,1])
    glBindTexture(GL_TEXTURE_2D, textures[name])
    try:
        yield
    finally:
        glBindTexture(GL_TEXTURE_2D, 0)


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
    with apply_texture('janela'):
        glPushMatrix()
        glTranslate(-46.2, 3.6, -3.53)
        glTranslate(0, 0, -5)
        glRotate(-windowRot, 0, 1, 0)
        glTranslate(0, 0, 5)
        glRotate(180, 0, 1, 0)

        parser.parse('janela', texture=True)

        glPopMatrix()
        glPushMatrix()
        glTranslate(-46.2, 3.6, 7.05)
        glTranslate(0, 0, 5)
        glRotate(windowRot, 0, 1, 0)
        glTranslate(0, 0, -5)

        parser.parse('janela', texture=True)

        glPopMatrix()


def room():
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [.2, .6, .1, 1.])
    glMaterialfv(GL_FRONT, GL_SPECULAR, [.7, .7, .7, 1.])
    glMaterialf(GL_FRONT, GL_SHININESS, 70)
    glColor3fv(colors.WHITE)
    parser.parse('paredes')
    glColor3fv(colors.BROWN3)
    parser.parse('sofa')
    with apply_texture('cadeira'):
        parser.parse('bau')


def floorCeiling():
    with apply_texture('piso'):
        parser.parse('chao', texture=True)
    glColor3fv(colors.ORANGE1)
    parser.parse('teto')


def bed():
    glColor3fv(colors.BLUE2)
    parser.parse('travesseiro')

    glColor3fv(colors.BLUE1)
    parser.parse('colchao')

    with apply_texture('cama'):
        parser.parse('cama')


def fan():
    global fanRot
    glPushMatrix()

    glTranslate(43, -2.25, -15)
    glRotate(50, 0, 1, 0)
    glColor3fv(colors.BLUE2)
    parser.parse('corpo')

    glPushMatrix()

    glRotate(fanRot, 1, 0, 0)
    fanRot = (fanRot+speed) % 360
    glColor3fv(colors.GREEN2)
    parser.parse('helice')

    glPopMatrix()
    glPopMatrix()


def light():
    glPushMatrix()

    glTranslate(42, -0.60, 2);

    glColor3fv(colors.GREEN3)
    parser.parse('luminaria')

    glPopMatrix()


def table():
    glColor3fv(colors.BROWN1)
    parser.parse('mesa')
    with apply_texture('cadeira'):
        parser.parse('cadeira')
    glColor3fv(colors.ORANGE3)
    parser.parse('lixeira')
    glColor3fv(colors.BROWN3)
    parser.parse('lapis')
    light()
    fan()


def painting():
    with apply_texture('quadro'):
        parser.parse('tela', texture=True)
    with apply_texture('madeira'):
        parser.parse('quadro', texture=True)


def all():
    room()
    door()
    window()
    floorCeiling()
    bed()
    table()
    painting()


textures = None
def load_all_textures():
    global textures
    textures = {
        'quadro': load_texture('mesh/textures/quadro.jpg'),
        'madeira': load_texture('mesh/textures/madeira.jpg'),
        'piso': load_texture('mesh/textures/piso.jpg'),
        'janela': load_texture('mesh/textures/janela.jpg'),
        'cama': load_texture('mesh/textures/cama.jpg'),
        'cadeira': load_texture('mesh/textures/mesa.jpg'),
    }


parser.load('mesh/porta.obj')
parser.load('mesh/janela.obj')
parser.load('mesh/paredes/paredes.obj')
parser.load('mesh/paredes/chao.obj')
parser.load('mesh/paredes/teto.obj')
parser.load('mesh/sofa.obj')
parser.load('mesh/bau.obj')

parser.load('mesh/cama/travesseiro.obj')
parser.load('mesh/cama/colchao.obj')
parser.load('mesh/cama/cama.obj')

parser.load('mesh/mesa/mesa.obj')
parser.load('mesh/mesa/lixeira.obj')
parser.load('mesh/mesa/cadeira.obj')
parser.load('mesh/mesa/luminaria.obj')
parser.load('mesh/mesa/lapis.obj')

parser.load('mesh/mesa/ventilador/helice.obj')
parser.load('mesh/mesa/ventilador/corpo.obj')

parser.load('mesh/quadro/quadro.obj')
parser.load('mesh/quadro/tela.obj')

