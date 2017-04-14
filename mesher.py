import os
import struct

import bf2

# https://github.com/ByteHazard/BfMeshView/blob/master/source/modStdMesh.bas


class StdMeshFile:

    class __Filestruct:  # pure containers

        class __Header:

            def __init__(self):
                self.u1 = None
                self.version = None
                self.u3 = None
                self.u4 = None
                self.u5 = None
        
        class __Unknown:

            def __init__(self):
                self.u2 = None
        
        class __Geom:

            def __init__(self):
                self.num = None
        
        class __Bf2Geom:
        
            class __Lod():
            
                class __Bounds():
                
                    def __init__(self):
                        self.min = None
                        self.max = None
                        self.pivot = None
                
                def __init__(self):
                    self.bounds = self.__Bounds()
                    self.rignum = None
            
            def __init__(self):
                self.lodnum = None
                self.lod = self.__Lod()

        def __init__(self):
            self.header = self.__Header()
            self.unknown2 = self.__Unknown()
            self.geom = self.__Geom()
            self.bf2geom = self.__Bf2Geom()

    def __init__(self, filepath):
        self.filepath = filepath
        self.filedata = None
        self.struct = self.__Filestruct()

    def get_filedata(self):
        if self.filedata is None:
            with open(self.filepath, 'rb') as fo:
                self.filedata = fo.read()

        return self.filedata

    def read_header(self):
        # u1 As long          '0
        # version As long     '10 for most bundledmesh, 6 for some bundledmesh, 11 for staticmesh
        # u3 As long          '0
        # u4 As long          '0
        # u5 As long          '0
        format = 'l l l l l'
        data_struct = struct.Struct(format)
        data_size = struct.calcsize(format)

        start = 0
        tail = data_size

        self.struct.header.u1, self.struct.header.version, self.struct.header.u3, self.struct.header.u4, self.struct.header.u5 = data_struct.unpack(self.get_filedata()[start:tail])
        return tail

    def read_unknown2(self):
        # u1 As char          'always 0?
        format = 'b'
        data_struct = struct.Struct(format)
        data_size = struct.calcsize(format)

        start = self.read_header()
        tail = start + data_size

        self.struct.unknown2.u1 = data_struct.unpack(self.get_filedata()[start:tail])[0]
        return tail

    def read_geom_num(self):
        # geomnum As l
        format = 'l'
        data_struct = struct.Struct(format)
        data_size = struct.calcsize(format)

        start = self.read_unknown2()
        tail = start + data_size

        self.struct.geom.num = data_struct.unpack(self.get_filedata()[start:tail])[0]
        return tail

    def read_bf2geom_lodnum(self):
        # geomnum As l
        format = 'l'
        data_struct = struct.Struct(format)
        data_size = struct.calcsize(format)

        start = self.read_geom_num()
        tail = start + data_size

        self.struct.bf2geom.lodnum = data_struct.unpack(self.get_filedata()[start:tail])[0]
        return tail
    
    def read_bf2geom_lod_bounds(self):
        # geomnum As l
        format = 'l l l l l l l l l'
        data_struct = struct.Struct(format)
        data_size = struct.calcsize(format)

        start = self.read_bf2geom_lodnum()
        tail = start + data_size

        self.struct.bf2geom.lod.bounds.min = data_struct.unpack(self.get_filedata()[start:tail])[0:3]
        self.struct.bf2geom.lod.bounds.max = data_struct.unpack(self.get_filedata()[start:tail])[3:6]
        self.struct.bf2geom.lod.bounds.pivot = data_struct.unpack(self.get_filedata()[start:tail])[6:9]
        return tail













