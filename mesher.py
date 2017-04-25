import os
import struct

import bf2

# https://github.com/ByteHazard/BfMeshView/blob/master/source/modStdMesh.bas

def LoadBF2Mesh(filepath):
    with open(filepath, 'rb') as meshfile:
        vmesh = StdMeshFile(meshfile)
    return vmesh

class bf2head:
    def __init__(self, fo):
        self.u1 = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.version = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.u3 = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.u4 = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.u5 = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]

class bf2geom:
    def __init__(self, fo):
        self.lodnum = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]

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

class StdMeshFile:

    def __init__(self, fo):
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




























