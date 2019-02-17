import os
import sys
sys.path.append('tests')
import copy

import bf2

import modmesh
import modcolmesh
from modVec3 import Vec3

def main():
    colpath = os.path.join(
        bf2.Mod().root,
        'objects',
        'staticobjects',
        'pr',
        'citybuildings',
        'pavement',
        'divider',
        '24m_1',
        'Meshes',
        '24m_1.collisionmesh')
    colmesh = modcolmesh.ColMesh(colpath)
    colmesh2 = copy.deepcopy(colmesh)

    # from fallujah
    position1 = Vec3(491.567, 24.653, 495.454)
    rotation1 = (0.2, 0.0, 0.0)

    position2 = Vec3(491.416, 24.653, 443.974)
    rotation2 = (0.2, 0.0, 0.0)
    
    diff = position2 - position1

    print(diff)
    raise

    colmesh2.translate(diff)
    colmesh.merge(colmesh2)

    col0 = colmesh.geoms[0].subgeoms[0].lods[0]
    min, max = Vec3(*col0.min), Vec3(*col0.max)
    center_offset = (min + max) / 2
    #print(min)
    #print(max)
    #print(center_offset)
    #print(position1 + center_offset)
    colmesh.translate(-center_offset)

    path_save = os.path.join(
        bf2.Mod().root,
        'objects',
        'staticobjects',
        'pr',
        'citybuildings',
        'pavement',
        'divider',
        '24m_1_merge',
        'meshes',
        '24m_1_merge.collisionmesh')
    colmesh.save(path_save)




if __name__ == '__main__':
    main()