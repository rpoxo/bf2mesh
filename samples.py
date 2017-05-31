import os
import struct

import bf2

class StdSample:

    def __init__(self):
        self._tail = 0
        
        # header
        self.fourcc = None
        self.width = None
        self.height = None
        
        self.datanum = None
        self.data = None
        
        self.facenum = None
        self.faces = None

    def _read_head(self, fo):
        fmt = '4s l l'
        size = struct.calcsize(fmt)

        self.fourcc, self.width, self.height = struct.Struct(fmt).unpack(fo.read(size))
        self._tail = fo.tell()
