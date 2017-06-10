import os
import struct

import bf2

class smp_sample:
    
    def __init__(self):
        self.position = None
        self.rotation = None
        self.face = None
    
    def read(self, fo):
        def read_position(fo):
            fmt = '3f'
            size = struct.calcsize(fmt)
            return struct.Struct(fmt).unpack(fo.read(size))

        def read_rotation(fo):
            fmt = '3f'
            size = struct.calcsize(fmt)
            return struct.Struct(fmt).unpack(fo.read(size))
        
        def read_face(fo):
            fmt = 'l'
            size = struct.calcsize(fmt)
            return struct.Struct(fmt).unpack(fo.read(size))

        self.position = read_position(fo)
        self.rotation = read_rotation(fo)
        self.face = read_face(fo)

class StdSample:

    def __init__(self):
        # header
        self.fourcc = None
        self.width = None
        self.height = None
        
        self.datanum = None
        self.data = []
        
        self.facenum = None
        self.faces = None

    def _read_head(self, fo):
        fmt = '4s l l'
        size = struct.calcsize(fmt)

        self.fourcc, self.width, self.height = struct.Struct(fmt).unpack(fo.read(size))
        self.datanum = self.width * self.height

    def _read_data(self, fo):
        self._read_head(fo)

        for i in range(self.datanum):
            sample = smp_sample()
            sample.read(fo)
            self.data.append(sample)


















