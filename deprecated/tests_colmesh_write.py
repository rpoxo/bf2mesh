import unittest
import os

import modcolmesh

import tests.mock_mesh as mocks

class TestColMeshWrite(unittest.TestCase):

    def setUp(self):
        self.path_colmesh = os.path.join(*['tests', 'samples', 'evil_box', 'meshes', 'evil_box.collisionmesh'])

    def test_can_write_header(self):
        colmesh = modcolmesh.ColMesh()
        colmesh.load(self.path_colmesh)
        path_write = os.path.join(*['tests', 'generated', 'write', 'evil_box', 'meshes', 'evil_box_header.collisionmesh'])
        
        dir = os.path.dirname(path_write)
        if not os.path.exists(dir): os.makedirs(dir)

        with open(path_write, 'wb') as fo:
            colmesh._write_header(fo)
        
        with open(path_write, 'rb') as fo:
            colmesh2 = modcolmesh.ColMesh()
            colmesh2._read_header(fo)
            
            self.assertEqual(colmesh2.u1, colmesh.u1)
            self.assertEqual(colmesh2.version, colmesh.version)
        
    def test_can_write_geoms(self):
        colmesh = modcolmesh.ColMesh()
        colmesh.load(self.path_colmesh)
        path_write = os.path.join(*['tests', 'generated', 'write', 'evil_box', 'meshes', 'evil_box_geoms.collisionmesh'])
        
        dir = os.path.dirname(path_write)
        if not os.path.exists(dir): os.makedirs(dir)

        with open(path_write, 'wb') as fo:
            colmesh._write_geoms(fo)
        
        with open(path_write, 'rb') as fo:
            colmesh2 = modcolmesh.ColMesh()
            colmesh2._read_geoms(fo)
            
            self.assertEqual(colmesh2.geomnum, colmesh.geomnum)
            self.assertEqual(colmesh2.geoms, colmesh.geoms)
        
    def test_can_create_colmesh_from_mock(self):
        path_write = os.path.join(*['tests', 'generated', 'write', 'evil_box', 'meshes', 'evil_box_mock.collisionmesh'])
        
        colmesh = mocks.ColBox()
        colmesh.save(path_write)
        
        colmesh = modcolmesh.ColMesh()
        colmesh.load(path_write)




if __name__ == '__main__':
    unittest.main()
