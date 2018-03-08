import unittest
import os

import modcolmesh

class TestColMeshRead(unittest.TestCase):

    def setUp(self):
        self.path_colmesh = os.path.join(*['tests', 'samples', 'evil_box', 'meshes', 'evil_box.collisionmesh'])

    def test_can_read_header(self):
        with open(self.path_colmesh, 'rb') as meshfile:
            colmesh = modcolmesh.ColMesh()
            colmesh._read_header(meshfile)
            
        self.assertTrue(colmesh.u1 == 0)
        self.assertTrue(colmesh.version == 10)

    def test_can_read_geoms(self):
        with open(self.path_colmesh, 'rb') as meshfile:
            colmesh = modcolmesh.ColMesh()
            colmesh._read_geoms(meshfile)
            self.assertTrue(meshfile.tell() == 1511)
            
        self.assertTrue(len(colmesh.geoms) == colmesh.geomnum == 1)
        
        geom0 = colmesh.geoms[0]
        self.assertTrue(geom0.subgeomnum == 1)
        
        subgeom0 = geom0.subgeoms[0]
        self.assertTrue(subgeom0.lodnum == 3)
        
        lod0 = subgeom0.lods[0]
        self.assertTrue(lod0.coltype == 0)
        self.assertTrue(lod0.facenum == 12)
        self.assertTrue(lod0.u7 == 49)
        self.assertTrue(lod0.ynum == 3)
        self.assertTrue(lod0.znum == 12)
        self.assertTrue(lod0.anum == 36)

    def test_can_read_colmesh(self):
        colmesh = modcolmesh.ColMesh()
        colmesh.load(self.path_colmesh)