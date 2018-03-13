import enum  # python 3.4+
import os

import modIO
from modIO import read_float
from modIO import read_float3
from modIO import read_long
from modIO import read_short
from modIO import read_byte

from modIO import write_long
from modIO import write_short
from modIO import write_float3
from modIO import write_byte
from modIO import write_float

import modVec3
from modVec3 import Vec3

class coltype(enum.IntEnum):
    projectile = 0
    vehicle = 1
    soldier = 2
    ai = 3

class ystruct(object):

    def __init__(self, u1=0, u2=0, u3=0, u4=0, u5=0,):
        self.u1 = u1
        self.u2 = u2
        self.u3 = u3
        self.u4 = u4
        self.u5 = u5

    def _read(self, fo):
        self.u1 = read_float(fo)
        self.u2 = read_short(fo)
        self.u3 = read_short(fo)
        self.u4 = read_long(fo)
        self.u5 = read_long(fo)
    
    def _write(self, fo):
        write_float(fo, self.u1)
        write_short(fo, self.u2)
        write_short(fo, self.u3)
        write_long(fo, self.u4)
        write_long(fo, self.u5)
    
    def __eq__(self, other):
        return (self.u1 == other.u1 and
                self.u2 == other.u2 and
                self.u3 == other.u3 and
                self.u4 == other.u4 and
                self.u5 == other.u5)
    
    def __str__(self):
        return '{}, {}, {}, {}, {}'.format(self.u1,
                                            self.u2,
                                            self.u3,
                                            self.u4,
                                            self.u5)


class bf2colface(object):

    def __init__(self, v1=0, v2=0, v3=0, m=0):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.m = m
        
    def __eq__(self, other):
        return (self.v1 == other.v1 and
                self.v2 == other.v2 and
                self.v3 == other.v3 and
                self.m == other.m)

    def _read(self, fo):
        self.v1 = read_short(fo)
        self.v2 = read_short(fo)
        self.v3 = read_short(fo)
        self.m = read_short(fo)
    
    def _write(self, fo):
        write_short(fo, self.v1)
        write_short(fo, self.v2)
        write_short(fo, self.v3)
        write_short(fo, self.m)
    
    def __str__(self):
        return '({}, {}, {}, {})'.format(*self)
    
    def __iter__(self):
        for value in [self.v1, self.v2, self.v3, self.m]:
            yield value


class bf2collod(object):

    def __init__(self):
        self.coltype = 0

        self.facenum = 0
        self.faces = [bf2colface() for i in range(self.facenum)]

        self.vertnum = 0
        self.vertices = [] # list of Vec3
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
    
    def __eq__(self, other):
        equal = True
        if self.coltype != other.coltype:
            print('lod.coltype {} != {}'.format(self.coltype, other.coltype))
            equal = False

        if self.facenum != other.facenum:
            print('lod.facenum {} != {}'.format(self.facenum, other.facenum))
            equal = False
        if self.faces != other.faces:
            equal = False

        if self.vertnum != other.vertnum:
            print('lod.vertnum {} != {}'.format(self.vertnum, other.vertnum))
            equal = False
        if self.vertices != other.vertices:
            print('lod.vertices {} != {}'.format(self.vertices, other.vertices))
            equal = False
        if self.vertids != other.vertids:
            print('lod.vertids {} != {}'.format(self.vertids, other.vertids))
            equal = False

        if self.min != other.min:
            print('lod.min {} != {}'.format(self.min, other.min))
            equal = False
        if self.max != other.max:
            print('lod.max {} != {}'.format(self.max, other.max))
            equal = False

        if self.u7 != other.u7:
            print('lod.u7 {} != {}'.format(self.u7, other.u7))
            equal = False
            
        if self.bmin != other.bmin:
            print('lod.bmin {} != {}'.format(self.bmin, other.bmin))
            equal = False
        if self.bmax != other.bmax:
            print('lod.bmax {} != {}'.format(self.bmax, other.bmax))
            equal = False
        
        if self.ynum != other.ynum:
            print('lod.ynum {} != {}'.format(self.ynum, other.ynum))
            equal = False
        if self.ydata != other.ydata:
            print('lod.ydata {} != {}'.format(self.ydata, other.ydata))
            equal = False
        
        if self.znum != other.znum:
            print('lod.znum {} != {}'.format(self.znum, other.znum))
            equal = False
        if self.zdata != other.zdata:
            print('lod.zdata {} != {}'.format(self.zdata, other.zdata))
            equal = False
        
        if self.anum != other.anum:
            print('lod.anum {} != {}'.format(self.anum, other.anum))
            equal = False
        if self.adata != other.adata:
            print('lod.adata {} != {}'.format(self.adata, other.adata))
            equal = False
        return equal

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
        
    def _write(self, fo, version):
        if version >= 9:
            write_long(fo, self.coltype)

        self.__write_faces(fo)
        self.__write_vertices(fo)
        self.__write_bounds(fo)
        self.__write_ydata(fo)
        self.__write_zdata(fo)
        if version >= 10:
            self.__write_adata(fo)

    def __read_faces(self, fo):
        self.facenum = read_long(fo)
        self.faces = [bf2colface() for i in range(self.facenum)]
        for colface in self.faces:
            colface._read(fo)
    
    def __write_faces(self, fo):
        write_long(fo, self.facenum)

        for colface in self.faces:
            colface._write(fo)

    def __read_vertices(self, fo):
        self.vertnum = read_long(fo)

        self.vertices = []
        for i in range(self.vertnum):
            vertex = Vec3(*read_float3(fo))
            self.vertices.append(vertex)
        
        for i in range(self.vertnum):
            self.vertids.append(read_short(fo))
    
    def __write_vertices(self, fo):
        write_long(fo, self.vertnum)

        for vertex in self.vertices:
            write_float3(fo, *vertex)

        for vertid in self.vertids:
            write_short(fo, vertid)

    def __read_bounds(self, fo):
        self.min = Vec3(*read_float3(fo))
        self.max = Vec3(*read_float3(fo))

        self.u7 = read_byte(fo)

        self.bmin = Vec3(*read_float3(fo))
        self.bmax = Vec3(*read_float3(fo))
        
    def __write_bounds(self, fo):
        write_float3(fo, *self.min)
        write_float3(fo, *self.max)

        write_byte(fo, self.u7)

        write_float3(fo, *self.bmin)
        write_float3(fo, *self.bmax)
    
    def __read_ydata(self, fo):
        self.ynum = read_long(fo)
        self.ydata = [ystruct() for i in range(self.ynum)]
        for ydata in self.ydata:
            ydata._read(fo)
    
    def __write_ydata(self, fo):
        write_long(fo, self.ynum)
        
        for ydata in self.ydata:
            ydata._write(fo)
    
    def __read_zdata(self, fo):
        self.znum = read_long(fo)
        self.zdata = [read_short(fo) for i in range(self.znum)]
    
    def __write_zdata(self, fo):
        write_long(fo, self.znum)

        for value in self.zdata:
            write_short(fo, value)
    
    def __read_adata(self, fo):
        self.anum = read_long(fo)
        self.adata = [read_long(fo) for i in range(self.anum)]
    
    def __write_adata(self, fo):
        write_long(fo, self.anum)

        for value in self.adata:
            write_long(fo, value)

class bf2colsubgeom(object):

    def __init__(self):
        self.lodnum = 0
        self.lods = [bf2collod() for i in range(self.lodnum)]

    def _read(self, fo, version):
        self.lodnum = read_long(fo)
        self.lods = [bf2collod() for i in range(self.lodnum)]
        for lod in self.lods:
            lod._read(fo, version)
            
    def _write(self, fo, version):
        write_long(fo, self.lodnum)

        for lod in self.lods:
            lod._write(fo, version)
    
    def __eq__(self, other):
        equal = True
        if self.lodnum != other.lodnum:
            print('subgeom.lodnum {} != {}'.format(self.lodnum, other.lodnum))
            equal = False
        if self.lods != other.lods:
            equal = False
        return equal


class bf2colgeom(object):

    def __init__(self):
        self.subgeomnum = 0
        self.subgeoms = [bf2colsubgeom() for i in range(self.subgeomnum)]

    def _read(self, fo, version):
        self.subgeomnum = read_long(fo)
        self.subgeoms = [bf2colsubgeom() for i in range(self.subgeomnum)]
        for subgeom in self.subgeoms:
            subgeom._read(fo, version)
    
    def _write(self, fo, version):
        write_long(fo, self.subgeomnum)

        for subgeom in self.subgeoms:
            subgeom._write(fo, version)

    def __eq__(self, other):
        equal = True
        if self.subgeomnum != other.subgeomnum:
            print('geom.subgeomnum {} != {}'.format(self.subgeomnum, other.subgeomnum))
            equal = False
        if self.subgeoms != other.subgeoms:
            equal = False
        return equal


class ColMesh(object):

    def __init__(self):
        self.u1 = 0
        self.version = 0
        self.geomnum = 0
        self.geoms = [bf2colgeom() for i in range(self.geomnum)]
    
    def load(self, filename):
        with open(filename, 'rb') as fo:
            self._read_geoms(fo)
    
    def save(self, filename):
        dir = os.path.dirname(filename)
        if not os.path.exists(dir): os.makedirs(dir)

        with open(filename, 'wb') as fo:
            self._write_geoms(fo)

    def _read_header(self, fo, position=0):
        self.u1 = read_long(fo)
        self.version = read_long(fo)
    
    def _write_header(self, fo):
        write_long(fo, self.u1)
        write_long(fo, self.version)

    def _read_geomnum(self, fo):
        self._read_header(fo)

        self.geomnum = read_long(fo)

    def _read_geoms(self, fo):
        self._read_geomnum(fo)

        self.geoms = [bf2colgeom() for i in range(self.geomnum)]
        for geom in self.geoms:
            geom._read(fo, self.version)

    def _write_geoms(self, fo):
        self._write_header(fo)
    
        write_long(fo, self.geomnum)
        
        for geom in self.geoms:
            geom._write(fo, self.version)






