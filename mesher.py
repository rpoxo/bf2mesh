import os
import struct

import bf2

# https://github.com/ByteHazard/BfMeshView/blob/master/source/modStdMesh.bas

def LoadBF2Mesh(filepath):
    with open(filepath, 'rb') as meshfile:
        isSkinnedMesh = False
        isBundledMesh = False
        isStaticMesh = False
        mesh_types = {
            '.skinnedmesh' : isSkinnedMesh,
            '.bundledmesh' : isBundledMesh,
            '.staticmesh' : isStaticMesh
            }
        mesh_types[os.path.splitext(filepath)[0].lower()] = True
        vmesh = StdMeshFile(meshfile, mesh_types)
    return vmesh

class bf2lod:
    def __init__(self, fo, version):
        self.min = tuple(struct.Struct('3f').unpack(fo.read(struct.calcsize('3f'))))
        self.max = tuple(struct.Struct('3f').unpack(fo.read(struct.calcsize('3f'))))
        if version <= 6:
            self.pivot = tuple(struct.Struct('3f').unpack(fo.read(struct.calcsize('3f'))))
        self.nodenum = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.node = []
        self.polycount = 0
        self.matnum = None
        self.mat = []
    
    def read_lod_node_table(self, fo):
        for i in range(self.nodenum):
            for j in range(16):
                self.node.append(struct.Struct('f').unpack(fo.read(struct.calcsize('f')))[0])
            
    def read_geom_lod(self, fo, mesh_types, version):
        self.matnum = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        #print('matnum = {}'.format(self.matnum))
        #self.mat.append(bf2mat(fo))
        for i in range(self.matnum):
            material = bf2mat(fo, mesh_types, version)
            self.mat.append(material)
            self.polycount = self.polycount + material.inum / 3

class bf2mat:
    def __init__(self, fo, mesh_types, version):
        self.alphamode = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.fxfile = self.__get_string(fo)
        self.technique = self.__get_string(fo)
        self.mapnum = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.map = self.__get_maps(fo)
        self.vstart = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.istart = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.inum = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.vnum = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.u4 = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.u5 = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        if not mesh_types['.skinnedmesh'] and version == 11:
            self.nmin = tuple(struct.Struct('3f').unpack(fo.read(struct.calcsize('3f'))))
            self.nmax = tuple(struct.Struct('3f').unpack(fo.read(struct.calcsize('3f'))))
        
    def __get_string(self, fo):
        string_len = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        string_fmt = str(string_len) + 's'
        return struct.Struct(string_fmt).unpack(fo.read(struct.calcsize(string_fmt)))[0]
    
    def __get_maps(self, fo):
        mapnames = []
        for i in range(self.mapnum):
            mapnames.append(self.__get_string(fo))
        return mapnames
            

class bf2head:
    def __init__(self, fo):
        # some internals
        self._fmt = ('l l l l l')
        self._size = struct.calcsize(self._fmt)

        # reading bin
        data = struct.Struct(self._fmt).unpack(fo.read(self._size))
        self.u1 = data[0]
        self.version = data[1]
        self.u3 = data[2]
        self.u4 = data[3]
        self.u5 = data[4]
    
    def __eq__(self, other):
        if self.u1 != other.u1: return False
        if self.version != other.version : return False
        if self.u3 != other.u3: return False
        if self.u4 != other.u4: return False
        if self.u5 != other.u5: return False
        return True

class bf2geom:
    def __init__(self, fo):
        self.lodnum = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.lod = []

class vertattrib:
    def __init__(self, fo):
        self.flag = struct.Struct('h').unpack(fo.read(struct.calcsize('h')))[0]
        self.offset = struct.Struct('h').unpack(fo.read(struct.calcsize('h')))[0]
        self.vartype = struct.Struct('h').unpack(fo.read(struct.calcsize('h')))[0]
        self.usage = struct.Struct('h').unpack(fo.read(struct.calcsize('h')))[0]
    
    def __len__(self):
        return 4

    def __str__(self):
        return str((self.flag, self.offset, self.vartype, self.usage))
    
    def __eq__(self, other_tuple):
        if (self.flag, self.offset, self.vartype, self.usage) == other_tuple:
            return True
        else:
            return False

def get_vert(fo):
    return struct.Struct('f').unpack(fo.read(struct.calcsize('f')))[0]

def get_index(fo):
    return struct.Struct('h').unpack(fo.read(struct.calcsize('h')))[0]

def _read_u1_bfp4f(fo, offset):
    fo.seek(offset)
    return struct.Struct('b').unpack(fo.read(struct.calcsize('b')))[0]

def _read_geomnum(fo, offset):
    fo.seek(offset)
    return struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]

class StdMeshFile:

    def __init__(self, fo, mesh_types):
        self.head = bf2head(fo)
        self.u1 = struct.Struct('b').unpack(fo.read(struct.calcsize('b')))[0]
        self.geomnum = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.geom = [bf2geom(fo) for i in range(self.geomnum)]
        self.vertattribnum = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.vertattrib = [vertattrib(fo) for i in range(self.vertattribnum)]
        self.vertformat = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.vertstride = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.vertnum = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.vertices = [get_vert(fo) for i in range(int(self.vertstride/self.vertformat * self.vertnum))]
        self.indexnum = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.index = [get_index(fo) for i in range(self.indexnum)]
        self.u2 = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        for geomnum in range(self.geomnum):
            for lodnum in range(self.geom[geomnum].lodnum):
                self.geom[geomnum].lod.insert(lodnum, bf2lod(fo, self.head.version))
                self.geom[geomnum].lod[lodnum].read_lod_node_table(fo)
        for geomnum in range(self.geomnum):
            for lodnum in range(self.geom[geomnum].lodnum):
                self.geom[geomnum].lod[lodnum].read_geom_lod(fo, mesh_types, self.head.version)
        print('file len = {}'.format(fo.tell()))


    def _write_header(self, filepath):
        with open(filepath, 'wb+') as fo:
            dataset = (self.head.u1,
                    self.head.version,
                    self.head.u3,
                    self.head.u4,
                    self.head.u5)
            fo.write(struct.Struct(self.head._fmt).pack(*dataset))
            return fo.tell()

    def _write_u1_bfp4f_version(self, filepath):
        with open(filepath, 'ab+') as fo:
            fmt = 'b'
            fo.write(struct.Struct(fmt).pack(self.u1))
            return fo.tell()


    def _write_geomnum(self, filepath):
        self._write_u1_bfp4f_version(filepath)
        with open(filepath, 'ab+') as fo:
            fmt = 'l'
            fo.write(struct.Struct(fmt).pack(self.geomnum))
            return fo.tell()


















