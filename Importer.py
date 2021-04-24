class Importer(object):
    def __init__(self, file):
        self.file = file.readlines()
        self.vertices = []
        self.normals = []
        self.faces = []
        self.textures = []

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

    def do_import(self):
        def faces_f(line):
            """f 1/1/1 5/2/1 7/3/1 3/4/1
                vertex_index/texture_index/normal_index
            """
            line = line.split()[1:]
            temp = []
            for i in line:
                # os indices no arquivo obj começam a partir do 1
                temp.append([int(x)-1 for x in i.split('/')])
            return temp

        vertices_f = lambda line: [float(x) for x in line.split()[1:]]
        normals_f = lambda line: [float(x) for x in line.split()[1:]]
        textures_f = lambda line: [float(x) for x in line.split()[1:]]
        self.vertices = self._get_section('v ', vertices_f)
        self.normals = self._get_section('vn', normals_f)
        self.faces = self._get_section('f', faces_f)
        self.textures = self._get_section('vt', textures_f)
        return self.vertices, self.normals, self.faces, self.textures


if __name__ == '__main__':
    with open('teste1.obj') as file:
        imp = Importer(file)
        print(imp.do_import()[3])

