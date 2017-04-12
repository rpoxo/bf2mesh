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
        
        class __Unknown:
            
            def __init__(self):
                self.qflag = None
                self.tail = None
        
        def __init__(self):
            self.header = self.__Header()
            self.bounds = self.__Bounds()
            self.unknown1 = self.__Unknown()
    
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
        end = header_size
        
        self.struct.header.version, self.struct.header.u2 = header_struct.unpack(self.get_filedata()[start:end])
        self.struct.header.tail = header_size
        
    def read_bounds(self):
        self.read_header()
        # min as (int, int, int)
        # max as (int, int, int)
        format = 'i i i i i i'
        bounds_struct = struct.Struct(format)
        bounds_size = struct.calcsize(format)
        
        start = self.struct.header.tail
        end = start + bounds_size
        
        self.struct.bounds.min = tuple(bounds_struct.unpack(self.get_filedata()[start:end])[0:3])
        self.struct.bounds.max = tuple(bounds_struct.unpack(self.get_filedata()[start:end])[3:6])
        self.struct.bounds.tail = self.struct.header.tail + bounds_size


    def read_qflag(self):
        self.read_bounds()
        # qflag as char
        format = 'c'
        qflag_struct = struct.Struct(format)
        qflag_size = struct.calcsize(format)
        
        start = self.struct.bounds.tail
        end = start + qflag_size
        
        self.struct.unknown1.qflag = qflag_struct.unpack(self.get_filedata()[start:end])
        self.struct.unknown1.tail = self.struct.bounds.tail + qflag_size






















