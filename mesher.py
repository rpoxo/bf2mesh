import os
import struct

import bf2

# https://github.com/ByteHazard/BfMeshView/blob/master/source/modStdMesh.bas
class StdMeshFile:

    class __Filestruct: # pure containers
    
        class __Header:
            
            def __init__(self):
                self.version = None
                self.u2 = None
                self.tail = None
        
        class __Bounds:
            
            def __init__(self):
                self.min = None
                self.max = None
                self.tail = None
        
        def __init__(self):
            self.header = self.__Header()
            self.bounds = self.__Bounds()
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.filedata = None
        self.struct = self.__Filestruct()

    def get_filedata(self):
        if self.filedata == None:
            with open(self.filepath, 'rb') as fo:
                self.filedata = fo.read()
        
        return self.filedata


    def read_header(self):
        # version as long
        # u2 as long
        format = 'l l'
        header_struct = struct.Struct(format)
        header_size = struct.calcsize(format)

        start = 0
        end, self.struct.header.tail = header_size, header_size
        
        self.struct.header.version, self.struct.header.u2 = header_struct.unpack(self.get_filedata()[start:end])
        
    def read_bounds(self):
        self.read_header()
        # min as (int, int, int)
        # max as (int, int, int)
        format = 'i i i i i i'
        bounds_struct = struct.Struct(format)
        bounds_size = struct.calcsize(format)
        
        start = self.struct.header.tail
        end = self.struct.header.tail + bounds_size
        
        self.struct.bounds.min = tuple(bounds_struct.unpack(self.get_filedata()[start:end])[0:3])
        self.struct.bounds.max = tuple(bounds_struct.unpack(self.get_filedata()[start:end])[3:6])
        self.struct.bounds.tail = self.struct.header.tail + bounds_size


























