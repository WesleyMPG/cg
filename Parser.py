from Importer import *
from OpenGL.GL import *
from os.path import split, splitext

class Parser(object):
    def __init__(self):
        self.objects = {}
        self.importer = Importer()

    def _import(self, file_path):
        getFileName = lambda path: splitext(split(file_path)[1])[0]
        with open(file_path) as file:
            data = self.importer.do_import(file)
        return data, getFileName(file_path)

    def _add_obj(self, data, file_name):
        """Regista o objeto no parser"""
        vertices, normals, faces, textures = data
        self.objects[file_name] = {
            'vertices': vertices,
            'normals': normals,
            'faces': faces,
            'textures': textures,
        }

    def _parse(self, name, use_texture : bool):
        obj = self.objects[name]
        glBegin(GL_QUADS)

        for face in obj['faces']:
        # estrutura de um vertice na lista de
        # faces: vertex/texture/normal
            for v in face:
                vi, ti, ni = v
                glNormal3fv(obj['normals'][ni])
                glTexCoord2fv(obj['textures'][ti])
                glVertex3fv(obj['vertices'][vi])
        glEnd()

    def load(self, file_path):
        """Carrega o arquivo"""
        data, file_name = self._import(file_path)
        self._add_obj(data, file_name)

    def parse(self, name, texture=False):
        """Faz o desenho do objeto"""
        self._parse(name, texture)

