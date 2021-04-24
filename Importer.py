class Importer(object):
    def __init__(self):
        self.file = None

    def _get_section(self, section : str, format_f=None):
        format_f = (lambda x: x) if format_f is None else format_f
        section_found = False
        temp = []
        for line in self.file:
            is_vertex_line = line.startswith(section)
            if is_vertex_line:
                temp.append(format_f(line))
                section_found = True
            elif section_found and not is_vertex_line:
                break
        return temp

    @staticmethod
    def faces_func(line):
        """f 1/1/1 5/2/1 7/3/1 3/4/1
            vertex_index/texture_index/normal_index
        """
        line = line.split()[1:]
        temp = []
        for i in line:
            # os indices no arquivo obj começam a partir do 1
            temp.append([int(x)-1 for x in i.split('/')])
        return temp

    @staticmethod
    def vertices_func(line):
        return [float(x) for x in line.split()[1:]]

    @staticmethod
    def normals_func(line):
        return [float(x) for x in line.split()[1:]]

    @staticmethod
    def textures_func(line):
        return [float(x) for x in line.split()[1:]]

    def do_import(self, file):
        self.file = file.readlines()
        vertices = self._get_section('v ', Importer.vertices_func)
        normals = self._get_section('vn', Importer.normals_func)
        faces = self._get_section('f', Importer.faces_func)
        textures = self._get_section('vt', Importer.textures_func)
        return vertices, normals, faces, textures


if __name__ == '__main__':
    with open('teste1.obj') as file:
        imp = Importer()
        print(imp.do_import(file)[3])

