import os
import struct

import modmath


def LoadBF2Sample(filepath):
    with open(filepath, 'rb') as samplefile:
        sample = StdSample()
        sample.load_file_data(samplefile)
    return sample


class smp_sample:

    def __init__(self):
        self.position = None
        self.rotation = None
        self.face = None

    def read(self, fo):
        self.position = modmath.float3(fo)
        self.rotation = modmath.float3(fo)
        self.face = modmath.long(fo)


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
        self.v1 = modmath.float3(fo)
        self.n1 = modmath.float3(fo)

        self.v2 = modmath.float3(fo)
        self.n2 = modmath.float3(fo)

        self.v3 = modmath.float3(fo)
        self.n3 = modmath.float3(fo)


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

    def load_file_data(self, fo):
        self._read_faces(fo)

    def _read_head(self, fo):
        self.fourcc = modmath.string(fo, lenght=4)
        self.width = modmath.long(fo)
        self.height = modmath.long(fo)

    def _read_data(self, fo):
        self._read_head(fo)

        self.datanum = self.width * self.height
        for i in range(self.datanum):
            sample = smp_sample()
            sample.read(fo)
            self.data.append(sample)

    def _read_faces(self, fo):
        self._read_data(fo)

        self.facenum = modmath.long(fo)
        for i in range(self.facenum):
            face = smp_face()
            face.read(fo)
            self.faces.append(face)
