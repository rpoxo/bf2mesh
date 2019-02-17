import unittest
import os
import copy

import modVec3
from modVec3 import Vec3

import modcolmesh

import tests.mock_mesh as mocks

class TestColMeshEdit(unittest.TestCase):

    def setUp(self):
        self.path_colmesh = os.path.join(*['tests', 'samples', 'evil_box', 'meshes', 'evil_box.collisionmesh'])
        self.path_write_folder = os.path.join(*['tests', 'generated', 'edit'])

    def test_can_translate_colmesh(self):
        colmesh = modcolmesh.ColMesh()
        colmesh.load(self.path_colmesh)
        colmesh_old = copy.deepcopy(colmesh)
        path_write = os.path.join(*['tests', 'generated', 'edit', 'evil_box_translate_mesh', 'meshes', 'evil_box_translate_mesh.collisionmesh'])

        colmesh = modcolmesh.ColMesh()
        colmesh.load(self.path_colmesh)
            
        offset = Vec3(1.0, 0.0, 0.0)
        colmesh.translate(offset)

        colmesh.save(path_write)
        
        self.assertEqual(len(colmesh.geoms), len(colmesh_old.geoms))
        for id_geom, geom in enumerate(colmesh.geoms):
            geom_old = colmesh_old.geoms[id_geom]
            self.assertEqual(len(geom.subgeoms), len(geom_old.subgeoms))
            for id_sub, subgeom in enumerate(geom.subgeoms):
                subgeom_old = geom_old.subgeoms[id_sub]
                self.assertEqual(len(subgeom.lods), len(subgeom_old.lods))
                for id_lod, lod in enumerate(subgeom.lods):
                    lod_old = subgeom_old.lods[id_lod]
                    self.assertEqual(len(lod.vertices), len(lod_old.vertices))
                    self.assertEqual(len(lod.faces), len(lod_old.faces))
                    
                    for id_vert, vertex in enumerate(lod.vertices):
                        vertex_old = lod_old.vertices[id_vert]
                        print('[{}] {} : {}'.format(id_vert, vertex, vertex_old))
                        self.assertEqual(vertex, (vertex_old + offset))
   
    #@unittest.skip('TODO: read more about cols')
    def test_can_merge_geoms(self):
        colmesh = modcolmesh.ColMesh(self.path_colmesh)
        colmesh2 = copy.deepcopy(colmesh)
        path_write = os.path.join(*[self.path_write_folder,
                                    'evil_box_merge_mesh', 'meshes', 'evil_box_merge_mesh.collisionmesh'])
        
        # translate 2nd mesh first
        colmesh2.translate(Vec3(1.0, 0.0, 0.0))

        colmesh.merge(colmesh2)
        colmesh.save(path_write)


if __name__ == '__main__':
    unittest.main()
