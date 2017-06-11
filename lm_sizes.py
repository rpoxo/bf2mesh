import os
import sys

import bf2
import mesher

DEBUG = False

excludes = [
    '\staticobjects\test',
]

samples_extensions = [
    'samples',
    'samp_01',
    'samp_02',
    'samp_03',
    'samp_04',
    'samp_05',
    'samp_06',
    'samp_07',
    'samp_08',
    'samp_09',
]


class LM_data:

    def __init__(self, name):
        self.name = name
        self.mesh = None
        self.samples = []


def main():
    modroot = bf2.Mod().root

    lm_sizes_data = {}
    for dir, dirnames, filenames in os.walk(
            os.path.join(modroot, 'objects', 'staticobjects')):
        for filename in filenames:
            filepath = os.path.join(
                modroot, 'objects', 'staticobjects', dir, filename)
            name = os.path.splitext(filename)[0]
            ext = os.path.splitext(filename)[1]
            if name not in lm_sizes_data.keys():
                lm_sizes_data[name] = LM_data(name)
                if ext == '.staticmesh':
                    try:
                        lm_sizes_data[name].mesh = mesher.LoadBF2Mesh(filepath)
                    except mesher.struct.error:
                        print('Failed to load {}'.format(filepath))

if __name__ == "__main__":
    main()
