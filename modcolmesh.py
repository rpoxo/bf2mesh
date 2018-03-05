import enum  # python 3.4+

import modIO
from modIO import read_int
from modIO import read_float
from modIO import read_float3
from modIO import read_long
from modIO import read_short
from modIO import read_string
from modIO import read_byte
from modIO import read_matrix4

import modVec3
from modVec3 import Vec3

class coltype(enum.IntEnum):
    projectile = 0
    vehicle = 1
    soldier = 2
    ai = 3

class ystruct(object):

    def __init__(self):
        self.u1 = 0
        self.u2 = 0
        self.u3 = 0
        self.u4 = 0
        self.u5 = 0

    def _read(self, fo):
        self.u1 = read_float(fo)
        self.u2 = read_short(fo)
        self.u3 = read_short(fo)
        self.u4 = read_long(fo)
        self.u5 = read_long(fo)
    
    def __str__(self):
        return 'ydata\n' + 'u1:{}\nu2:{}\nu3:{}\nu4:{}\nu5:{}\n'.format(
                                                        self.u1,
                                                        self.u2,
                                                        self.u3,
                                                        self.u4,
                                                        self.u5)


class bf2colface(object):

    def __init__(self):
        self.v1 = 0
        self.v2 = 0
        self.v3 = 0
        self.m = 0

    def _read(self, fo):
        self.v1 = read_short(fo)
        self.v2 = read_short(fo)
        self.v3 = read_short(fo)
        self.m = read_short(fo)


class bf2collod(object):

    def __init__(self):
        self.coltype = 0

        self.facenum = 0
        self.faces = [bf2colface() for i in range(self.facenum)]

        self.vertnum = 0
        self.vertices = []  # make list comprehension instead
        self.vertids = []  # some unknown 2 bytes ints

        self.min = Vec3(0.0, 0.0, 0.0)
        self.max = Vec3(0.0, 0.0, 0.0)

        self.u7 = 0

        self.bmin = Vec3(0.0, 0.0, 0.0)
        self.bmax = Vec3(0.0, 0.0, 0.0)

        self.ynum = 0
        self.ydata = [ystruct() for i in range(self.ynum)]

        self.znum = 0
        self.zdata = []

        self.anum = 0
        self.adata = []

    def _read(self, fo, version):
        if version >= 9:
            self.coltype = coltype(read_long(fo))

        self.__read_faces(fo)
        self.__read_vertices(fo)
        self.__read_bounds(fo)
        self.__read_ydata(fo)
        self.__read_zdata(fo)
        if version >= 10:
            self.__read_adata(fo)

    def __read_faces(self, fo):
        self.facenum = read_long(fo)
        self.faces = [bf2colface() for i in range(self.facenum)]
        for colface in self.faces:
            colface._read(fo)

    def __read_vertices(self, fo):
        self.vertnum = read_long(fo)

        self.vertices = []
        for i in range(self.vertnum):
            vertex = Vec3(*read_float3(fo))
            self.vertices.append(vertex)
        
        for i in range(self.vertnum):
            self.vertids.append(read_short(fo))

    def __read_bounds(self, fo):
        self.min = Vec3(*read_float3(fo))
        self.max = Vec3(*read_float3(fo))

        self.u7 = read_byte(fo)

        self.bmin = Vec3(*read_float3(fo))
        self.bmax = Vec3(*read_float3(fo))
    
    def __read_ydata(self, fo):
        self.ynum = read_long(fo)
        self.ydata = [ystruct() for i in range(self.ynum)]
        for ydata in self.ydata:
            ydata._read(fo)
    
    def __read_zdata(self, fo):
        self.znum = read_long(fo)
        self.zdata = [read_short(fo) for i in range(self.znum)]
    
    def __read_adata(self, fo):
        self.anum = read_long(fo)
        self.adata = [read_long(fo) for i in range(self.anum)]


class bf2colsubgeom(object):

    def __init__(self):
        self.lodnum = 0
        self.lods = [bf2collod() for i in range(self.lodnum)]

    def _read(self, fo, version):
        self.lodnum = read_long(fo)
        self.lods = [bf2collod() for i in range(self.lodnum)]
        for lod in self.lods:
            lod._read(fo, version)


class bf2colgeom(object):

    def __init__(self):
        self.subgeomnum = 0
        self.subgeoms = [bf2colsubgeom() for i in range(self.subgeomnum)]

    def _read(self, fo, version):
        self.subgeomnum = read_long(fo)
        self.subgeoms = [bf2colsubgeom() for i in range(self.subgeomnum)]
        for subgeom in self.subgeoms:
            subgeom._read(fo, version)


class ColMesh(object):

    def __init__(self):
        self.u1 = 0
        self.version = 0
        self.geomnum = 0
        self.geoms = [bf2colgeom() for i in range(self.geomnum)]

    def _read_header(self, fo, position=0):
        self.u1 = read_long(fo)
        self.version = read_long(fo)

    def _read_geomnum(self, fo):
        self._read_header(fo)

        self.geomnum = read_long(fo)

    def _read_geoms(self, fo):
        self._read_geomnum(fo)

        self.geoms = [bf2colgeom() for i in range(self.geomnum)]
        for geom in self.geoms:
            geom._read(fo, self.version)
