import os
import struct

import mesher

class Box:
    
    def __init__(self):
        self.vmesh = mesher.StdMesh()
        self._create_header(self.vmesh)
        self._create_u1_bfp4f_version(self.vmesh)

    def _create_header(self, vmesh):
        vmesh.head = mesher.bf2head()
        vmesh.head.u1 = 0
        vmesh.head.version = 11
        vmesh.head.u3 = 0
        vmesh.head.u4 = 0
        vmesh.head.u5 = 0

    def _create_u1_bfp4f_version(self, vmesh):
        vmesh.u1 = 0
