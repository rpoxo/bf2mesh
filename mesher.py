import os
import struct

import bf2

class StdMeshFile:

    class __Filestruct:
    
        class __Header:
            
            def __init__(self):
                self.version = None
                self.u2 = None
        
        def __init__(self):
            self.header = self.__Header()
    
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
        header_struct = struct.Struct('l l')
        self.struct.header.version, self.struct.header.u2 = header_struct.unpack(self.get_filedata()[0:8])
        