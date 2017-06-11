import os
import struct

import bf2
import modmath
import samples

# https://github.com/ByteHazard/BfMeshView/blob/master/source/modStdMesh.bas


def LoadBF2Mesh(
        filepath,
        loadTextures=False,
        loadSamples=False,
        loadCon=False):
    with open(filepath, 'rb') as meshfile:
        file_extension = os.path.splitext(filepath)[1].lower()

        isSkinnedMesh = (file_extension == '.skinnedmesh')
        isBundledMesh = (file_extension == '.bundledmesh')
        isStaticMesh = (file_extension == '.staticmesh')

        vmesh = StdMesh(isSkinnedMesh, isBundledMesh, isStaticMesh)
        vmesh.load_file_data(meshfile)

        if loadSamples:
            dir = os.path.dirname(filepath)
            for filename in os.listdir(dir):
                filepath = os.path.join(dir, filename)
                name = os.path.splitext(filename)[0]
                ext = os.path.splitext(filename)[1]
                if ext[:5] == '.samp':
                    if ext == '.samples':
                        vmesh.geoms[
                            0].lod[
                            0].sample = samples.LoadBF2Sample(filepath)
                    else:
                        geom = ext.split('_')[1][0]
                        lod = ext.split('_')[1][1]
                        vmesh.geoms[
                            geom].lod[
                            lod].sample = samples.LoadBF2Sample(filepath)
    return vmesh


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class bf2lod:

    def __init__(self, fo, version):
        # some internals
        self.version = version

        self.min = None
        self.max = None
        self.pivot = None
        self.nodenum = None

        self.node = []
        self.polycount = 0
        self.matnum = None
        self.mat = []

        self.sample = None


class bf2mat:

    def __init__(self, fo, isSkinnedMesh, version):
        self.alphamode = modmath.long(fo)
        #print('   alphamode: {}'.format(self.alphamode))
        self.fxfile = self.__get_string(fo)
        #print('   fxfile: {}'.format(self.fxfile))
        self.technique = self.__get_string(fo)
        #print('   technique: {}'.format(self.technique))
        self.mapnum = modmath.long(fo)
        #print('   mapnum: {}'.format(self.mapnum))
        self.map = self.__get_maps(fo)
        self.vstart = modmath.long(fo)
        #print('   vstart: {}'.format(self.vstart))
        self.istart = modmath.long(fo)
        #print('   istart: {}'.format(self.istart))
        self.inum = modmath.long(fo)
        #print('   inum: {}'.format(self.inum))
        self.vnum = modmath.long(fo)
        #print('   vnum: {}'.format(self.vnum))
        self.u4 = modmath.long(fo)
        self.u5 = modmath.long(fo)
        if not isSkinnedMesh and version == 11:
            self.nmin = modmath.float3(fo)
            self.nmax = modmath.float3(fo)

    def __get_string(self, fo):
        string_len = modmath.long(fo)
        return modmath.string(fo, string_len)

    def __get_maps(self, fo):
        mapnames = []
        for i in range(self.mapnum):
            mapname = self.__get_string(fo)
            mapnames.append(mapname)
            #print('    {}'.format(mapname))
        return mapnames


class bf2head:

    def __init__(self):
        # some internals
        self._fmt = None
        self._size = None

        # reading bin
        data = None
        self.u1 = None
        self.version = None
        self.u3 = None
        self.u4 = None
        self.u5 = None

    def read(self, fo):
        # for some reason it fails when using modmath
        self._fmt = ('5l')
        self._size = struct.calcsize(self._fmt)

        #data = struct.Struct(self._fmt).unpack(fo.read(self._size))
        self.u1 = modmath.long(fo)
        self.version = modmath.long(fo)
        self.u3 = modmath.long(fo)
        self.u4 = modmath.long(fo)
        self.u5 = modmath.long(fo)

    def __eq__(self, other):
        if self.u1 != other.u1:
            return False
        if self.version != other.version:
            return False
        if self.u3 != other.u3:
            return False
        if self.u4 != other.u4:
            return False
        if self.u5 != other.u5:
            return False
        return True


class bf2geom:

    def __init__(self, fo):
        self.lodnum = modmath.long(fo)
        self.lod = []


class vertattrib:

    def __init__(self, fo):
        self.flag = modmath.short(fo)
        self.offset = modmath.short(fo)
        self.vartype = modmath.short(fo)
        self.usage = modmath.short(fo)

    def __str__(self):
        return str((self.flag, self.offset, self.vartype, self.usage))

    def __eq__(self, other_tuple):
        if (self.flag, self.offset, self.vartype, self.usage) == other_tuple:
            return True
        else:
            return False


class StdMesh:

    def __init__(
            self,
            isSkinnedMesh=False,
            isBundledMesh=False,
            isStaticMesh=False):
        # setting some internals
        self.isSkinnedMesh = False
        self.isBundledMesh = False
        self.isStaticMesh = False

        # mesh data
        self.head = None  # header contains version and some bfp4f data
        self.u1 = None  # version flag for bfp4f
        self.geomnum = None  # amount of geoms
        self.geoms = None  # geoms data struct, to be filled as we reading file
        self.vertattribnum = None  # number of vertattributes xDDD
        self.vertattrib = None  # vertattrib array, no idea what it does
        # vert format? no idea hwta it does, perhaps bytes len(all floats)
        self.vertformat = None
        self.vertstride = None  # bytes size for vertex attributes buffer
        self.vertnum = None  # number of vertices
        self.vertices = []  # vertices array, actual geometry
        self.vertices_attributes = None  # generated buffers for better reading
        self.indexnum = None  # number of indices
        self.index = None  # vertex indices
        self.u2 = None  # some another bfp4f garbage..

    # just a wrapper for better name
    def load_file_data(self, fo):
        # materials read will read everything inb4
        self._read_filedata(fo)
        self._generate_vertices_attributes()

    def write_file_data(self, fo):
        # materials read will read everything inb4
        self._write_materials(fo)

    #-----------------------------
    # READING FILEDATA
    #-----------------------------
    def _read_head(self, fo):
        header = bf2head()
        header.read(fo)
        self.head = header
        #print('head ends at {}'.format(fo.tell()))

    def _read_u1_bfp4f_version(self, fo):
        self._read_head(fo)

        self.u1 = modmath.byte(fo)

    def _read_geomnum(self, fo):
        self._read_u1_bfp4f_version(fo)

        self.geomnum = modmath.long(fo)

    def _read_geoms(self, fo):
        self._read_geomnum(fo)

        self.geoms = [bf2geom(fo) for i in range(self.geomnum)]

    def _read_vertattribnum(self, fo):
        self._read_geoms(fo)

        self.vertattribnum = modmath.long(fo)

    def _read_vertext_attribute_table(self, fo):
        self._read_vertattribnum(fo)

        self.vertattrib = [vertattrib(fo) for i in range(self.vertattribnum)]

    def _read_vertformat(self, fo):
        self._read_vertext_attribute_table(fo)

        self.vertformat = modmath.long(fo)

    def _read_vertstride(self, fo):
        self._read_vertformat(fo)

        self.vertstride = modmath.long(fo)

    def _read_vertnum(self, fo):
        self._read_vertstride(fo)

        self.vertnum = modmath.long(fo)

    def _read_vertex_block(self, fo):
        self._read_vertnum(fo)

        vertices_num = int(self.vertstride / self.vertformat * self.vertnum)
        # TODO: refactor
        fmt = '{}f'.format(vertices_num)
        size = struct.calcsize(fmt)

        self.vertices = struct.Struct(fmt).unpack(fo.read(size))

    def _read_indexnum(self, fo):
        self._read_vertex_block(fo)

        self.indexnum = modmath.long(fo)

    def _read_index_block(self, fo):
        self._read_indexnum(fo)

        # TODO: refactor
        fmt = '{}h'.format(self.indexnum)
        size = struct.calcsize(fmt)

        self.index = struct.Struct(fmt).unpack(fo.read(size))

    def _read_u2(self, fo):
        if not self.isSkinnedMesh:
            self._read_index_block(fo)

            self.u2 = modmath.long(fo)

    def _read_nodes(self, fo):
        self._read_u2(fo)

        for geomnum in range(self.geomnum):
            for lodnum in range(self.geoms[geomnum].lodnum):
                self.geoms[geomnum].lod.insert(
                    lodnum, bf2lod(fo, self.head.version))
                self.__read_lod_node_table(fo, self.geoms[geomnum].lod[lodnum])

    def _read_materials(self, fo):
        self._read_nodes(fo)

        #print('geom block starts at {}'.format(fo.tell()))

        def _read_matnum(fo, lod):
            lod.matnum = modmath.long(fo)

        for geomnum in range(self.geomnum):
            for lodnum in range(self.geoms[geomnum].lodnum):
                #print(' mesh {} start at {}'.format(lodnum, fo.tell()))
                _read_matnum(fo, self.geoms[geomnum].lod[lodnum])
                # print(
                #    ' matnum: {}'.format(
                #        self.geoms[geomnum].lod[lodnum].matnum))
                # for matnum in range(self.geoms[geomnum].lod[lodnum].matnum):
                self.__read_lod_material(fo, self.geoms[geomnum].lod[lodnum])
                #print(' mesh {} end at {}'.format(lodnum, fo.tell()))
        #print('geom block ends at {}'.format(fo.tell()))

    def _read_filedata(self, fo):
        self._read_materials(fo)

    #-----------------------------
    # WRITING FILEDATA
    #-----------------------------
    def _write_header(self, filepath):
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filepath, 'wb+') as fo:
            dataset = (self.head.u1,
                       self.head.version,
                       self.head.u3,
                       self.head.u4,
                       self.head.u5)
            fo.write(struct.Struct(self.head._fmt).pack(*dataset))

    def _write_u1_bfp4f_version(self, filepath):
        self._write_header(filepath)
        with open(filepath, 'ab+') as fo:
            fmt = 'b'
            fo.write(struct.Struct(fmt).pack(self.u1))

    def _write_geomnum(self, filepath):
        self._write_u1_bfp4f_version(filepath)
        with open(filepath, 'ab+') as fo:
            fmt = 'l'
            fo.write(struct.Struct(fmt).pack(self.geomnum))

    def _write_geom_table(self, filepath):
        self._write_geomnum(filepath)
        with open(filepath, 'ab+') as fo:
            for geomnum in range(self.geomnum):
                fmt = 'l'
                fo.write(struct.Struct(fmt).pack(self.geoms[geomnum].lodnum))

    def _write_vertattribnum(self, filepath):
        self._write_geom_table(filepath)
        with open(filepath, 'ab+') as fo:
            fmt = 'l'
            fo.write(struct.Struct(fmt).pack(self.vertattribnum))

    def _write_vertex_attribute_table(self, filepath):
        self._write_vertattribnum(filepath)
        with open(filepath, 'ab+') as fo:
            for vertattribnum in range(self.vertattribnum):
                fmt = '4h'
                data = (self.vertattrib[vertattribnum].flag,
                        self.vertattrib[vertattribnum].offset,
                        self.vertattrib[vertattribnum].vartype,
                        self.vertattrib[vertattribnum].usage)
                fo.write(struct.Struct(fmt).pack(*data))

    def _write_vertformat(self, filepath):
        self._write_vertex_attribute_table(filepath)
        with open(filepath, 'ab+') as fo:
            fmt = 'l'
            fo.write(struct.Struct(fmt).pack(self.vertformat))

    def _write_vertstride(self, filepath):
        self._write_vertformat(filepath)
        with open(filepath, 'ab+') as fo:
            fmt = 'l'
            fo.write(struct.Struct(fmt).pack(self.vertstride))

    def _write_vertnum(self, filepath):
        self._write_vertstride(filepath)
        with open(filepath, 'ab+') as fo:
            fmt = 'l'
            fo.write(struct.Struct(fmt).pack(self.vertnum))

    def _write_vertex_block(self, filepath):
        self._write_vertnum(filepath)
        with open(filepath, 'ab+') as fo:
            fmt = '{}f'.format(len(self.vertices))
            fo.write(struct.Struct(fmt).pack(*self.vertices))

    def _write_indexnum(self, filepath):
        self._write_vertex_block(filepath)
        with open(filepath, 'ab+') as fo:
            fmt = 'l'
            fo.write(struct.Struct(fmt).pack(self.indexnum))

    def _write_index_block(self, filepath):
        self._write_indexnum(filepath)
        with open(filepath, 'ab+') as fo:
            fmt = '{}h'.format(len(self.index))
            fo.write(struct.Struct(fmt).pack(*self.index))

    def _write_u2(self, filepath):
        self._write_index_block(filepath)
        if not self.isSkinnedMesh:
            with open(filepath, 'ab+') as fo:
                fmt = 'l'
                fo.write(struct.Struct(fmt).pack(self.u2))

    def _write_nodes(self, filepath):
        self._write_u2(filepath)
        with open(filepath, 'ab+') as fo:
            for geomnum in range(self.geomnum):
                for lodnum in range(self.geoms[geomnum].lodnum):
                    self.__write_lod_node_table(
                        fo, self.geoms[geomnum].lod[lodnum])

    def _write_materials(self, filepath):
        self._write_nodes(filepath)
        with open(filepath, 'ab+') as fo:
            for geomnum in range(self.geomnum):
                for lodnum in range(self.geoms[geomnum].lodnum):
                    fo.write(
                        struct.Struct('l').pack(
                            self.geoms[geomnum].lod[lodnum].matnum))
                    self.__write_lod_material(
                        fo, self.geoms[geomnum].lod[lodnum])

    #-----------------------------
    # PRIVATE
    #-----------------------------

    def __read_lod_node_table(self, fo, lod):
        #print('nodes chunk start at  {}'.format(fo.tell()))

        def _read_bounds(fo, lod):
            lod.min = modmath.float3(fo)
            lod.max = modmath.float3(fo)

        def _read_pivot(fo, lod):
            lod.pivot = modmath.float3(fo)

        def _read_nodenum(fo, lod):
            lod.nodenum = modmath.long(fo)

        _read_bounds(fo, lod)
        if self.head.version <= 6:
            _read_pivot(fo, lod)
        _read_nodenum(fo, lod)

        # reading nodes
        for i in range(lod.nodenum):
            for j in range(16):
                lod.node.append(modmath.float(fo))
        #print('nodes chunk end at {}'.format(fo.tell()))

    def __write_lod_node_table(self, fo, lod):
        #print('nodes chunk start at  {}'.format(fo.tell()))

        def _write_bounds(fo, lod):
            fmt = '3f'
            fo.write(struct.Struct(fmt).pack(*lod.min))
            fo.write(struct.Struct(fmt).pack(*lod.max))

        def _write_pivot(fo, lod):
            if lod.version <= 6:
                fmt = '3f'
                fo.write(struct.Struct(fmt).pack(*lod.pivot))

        def _write_nodenum(fo, lod):
            fmt = 'l'
            fo.write(struct.Struct(fmt).pack(lod.nodenum))

        _write_bounds(fo, lod)
        if self.head.version <= 6:
            _write_pivot(fo, lod)
        _write_nodenum(fo, lod)

        # writing nodes
        for i in range(lod.nodenum):
            for j in range(16):
                fmt = 'f'
                fo.write(struct.Struct(fmt).pack(lod.node[j]))

    def __read_lod_material(self, fo, lod):
        for i in range(lod.matnum):
            #print('  mat {} start at {}'.format(i, fo.tell()))
            material = bf2mat(fo, self.isSkinnedMesh, self.head.version)
            #print('  mat {} ends at {}'.format(i, fo.tell()))
            lod.mat.insert(i, material)
            lod.polycount = lod.polycount + material.inum / 3

    def __write_lod_material(self, fo, lod):
        def __write_bstring(fo, bstring):
            fo.write(struct.Struct('l').pack(len(bstring)))
            fo.write(struct.Struct('{}s'.format(len(bstring))).pack(bstring))

        for i in range(lod.matnum):
            fo.write(struct.Struct('l').pack(lod.mat[i].alphamode))
            __write_bstring(fo, lod.mat[i].fxfile)
            __write_bstring(fo, lod.mat[i].technique)
            fo.write(struct.Struct('l').pack(lod.mat[i].mapnum))
            for mapnum in range(lod.mat[i].mapnum):
                __write_bstring(fo, lod.mat[i].map[mapnum])
            fo.write(struct.Struct('l').pack(lod.mat[i].vstart))
            fo.write(struct.Struct('l').pack(lod.mat[i].istart))
            fo.write(struct.Struct('l').pack(lod.mat[i].inum))
            fo.write(struct.Struct('l').pack(lod.mat[i].vnum))
            fo.write(struct.Struct('l').pack(lod.mat[i].u4))
            fo.write(struct.Struct('l').pack(lod.mat[i].u5))
            if not self.isSkinnedMesh and self.head.version == 11:
                fo.write(struct.Struct('3f').pack(*lod.mat[i].nmin))
                fo.write(struct.Struct('3f').pack(*lod.mat[i].nmax))

    def _generate_vertices_attributes(self):
        self.vertices_attributes = []
        if self.vertstride == 72:
            lenght = 18
        elif self.vertstride == 80:
            lenght = 20
        for chunk in chunks(self.vertices, lenght):
            position = tuple(chunk[0:3])
            normal = tuple(chunk[3:6])
            blend_indices = chunk[6]
            uv1 = tuple(chunk[7:9])
            uv2 = tuple(chunk[9:11])
            uv3 = tuple(chunk[11:13])
            uv4 = tuple(chunk[13:15])
            if lenght == 18:
                uv5 = None
                tangent = tuple(chunk[15:18])
            elif lenght == 20:
                uv5 = tuple(chunk[15:17])
                tangent = tuple(chunk[17:20])

            vert = {
                'position': position,
                'normal': normal,
                'blend_indices': blend_indices,
                'uv1': uv1,
                'uv2': uv2,
                'uv3': uv3,
                'uv4': uv4,
                'tangent': tangent
            }
            if lenght == 20:
                vert['uv5'] = uv5
            self.vertices_attributes.append(vert)

    def _write_vertices_attributes(self):
        vertices_new = []
        for vertice in self.vertices_attributes:
            for axis in vertice['position']:
                vertices_new.append(axis)
            for axis in vertice['normal']:
                vertices_new.append(axis)
            vertices_new.append(vertice['blend_indices'])

            vertices_new.append(vertice['uv1'][0])
            vertices_new.append(vertice['uv1'][1])

            vertices_new.append(vertice['uv2'][0])
            vertices_new.append(vertice['uv2'][1])

            vertices_new.append(vertice['uv3'][0])
            vertices_new.append(vertice['uv3'][1])

            vertices_new.append(vertice['uv4'][0])
            vertices_new.append(vertice['uv4'][1])

            if self.vertstride == 80:
                vertices_new.append(vertice['uv5'][0])
                vertices_new.append(vertice['uv5'][1])

            for axis in vertice['tangent']:
                vertices_new.append(axis)

        # converting to set after generating
        self.vertices = tuple(vertices_new)
