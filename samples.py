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

class smp_face:
    
    def __init__(self):
        '''
            v1 As float3
            n1 As float3
            
            v2 As float3
            n2 As float3
            
            v3 As float3
            n3 As float3
        '''
        self.v1 = None
        self.n1 = None
        
        self.v2 = None
        self.n2 = None
        
        self.v3 = None
        self.n3 = None
    
    def read(self, fo):
        def read_float3(fo):
            fmt = '3f'
            size = struct.calcsize(fmt)
            return struct.Struct(fmt).unpack(fo.read(size))
        
        self.v1 = read_float3(fo)
        self.n1 = read_float3(fo)
        
        self.v2 = read_float3(fo)
        self.n2 = read_float3(fo)
        
        self.v3 = read_float3(fo)
        self.n3 = read_float3(fo)

class StdSample:

    def __init__(self):
        # header
        self.fourcc = None
        self.width = None
        self.height = None
        
        self.datanum = None
        self.data = []
        
        self.facenum = None
        self.faces = []
        
    def read_filedata(self, fo):
        self._read_faces(fo)

    def _read_head(self, fo):
        fmt = '4s l l'
        size = struct.calcsize(fmt)

        self.fourcc, self.width, self.height = struct.Struct(fmt).unpack(fo.read(size))

    def _read_data(self, fo):
        self._read_head(fo)

        self.datanum = self.width * self.height
        for i in range(self.datanum):
            sample = smp_sample()
            sample.read(fo)
            self.data.append(sample)
    
    def _read_faces(self, fo):
        def read_facenum(fo):
            fmt = 'l'
            size = struct.calcsize(fmt)
            return struct.Struct(fmt).unpack(fo.read(size))[0]
            
        self._read_data(fo)

        self.facenum = read_facenum(fo)
        for i in range(self.facenum):
            face = smp_face()
            face.read(fo)
            self.faces.append(face)

















