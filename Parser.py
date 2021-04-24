from Importer import *
from OpenGL.GL import *

class Parser(object):
    def __init__(self):
        self.vertices = []
        self.normals = []
        self.faces = []
        self.textures = []

    def _import(self, file_path):
        with open(file_path) as file:
            imp = Importer(file)
            self.vertices, self.normals,\
            self.faces, self.textures = imp.do_import()

    def _parse(self, use_texture : bool):
        glBegin(GL_QUADS)

        for face in self.faces:
        # estrutura de um vertice na lista de
        # faces: vertex/texture/normal
            for v in face:
                vi, ti, ni = v
                glNormal3fv(self.normals[ni])
                if use_texture: glTexCoord2fv(self.textures[ti])
                glVertex3fv(self.vertices[vi])

        glEnd()

    def parse(self, file_path, texture=False):
        self._import(file_path)
        self._parse(texture)
