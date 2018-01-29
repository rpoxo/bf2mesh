import unittest
import copy
import os

import modmesh
from modmesh import D3DDECLTYPE, D3DDECLUSAGE

# shit just for merge test
class TestVisMeshDiff(unittest.TestCase):

    def setUp(self):
        self.path_3ds = os.path.join(*['tests', 'samples', 'pavement', '24m_1_merge_3ds', 'meshes', '24m_1_merge.staticmesh'])
        self.path_mesher = os.path.join(*['tests', 'generated', 'edit', 'pavement', '24m_1_merge', 'meshes', '24m_1_merge.staticmesh'])
    
    @unittest.skip('float inaccuracy, 3ds junk')
    def test_show_diff_geoms(self):
        vmesh1 = modmesh.LoadBF2Mesh(self.path_3ds)
        vmesh2 = modmesh.LoadBF2Mesh(self.path_mesher)
        
        self.assertEqual(vmesh1.geomnum, vmesh2.geomnum)
        for id_geom, geom1 in enumerate(vmesh1.geoms):
            geom2 = vmesh2.geoms[id_geom]
            self.assertEqual(geom1, geom2)
    

if __name__ == '__main__':
    unittest.main()