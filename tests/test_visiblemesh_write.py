import unittest
import struct
import os

from bf2mesh.bf2types import USED, UNUSED
from bf2mesh.bf2types import D3DDECLTYPE, D3DDECLUSAGE
import bf2mesh.visiblemesh
from bf2mesh.visiblemesh import VisibleMesh

class test_visiblemesh_write_staticmesh(unittest.TestCase):

    def setUp(self):
        self.path_mesh = 'tests/samples/staticmesh/evil_box/meshes/evil_box.staticmesh'
        self.path_save = 'tests/generated/staticmesh/write/evil_box/meshes/evil_box.staticmesh'
        self.vmesh = VisibleMesh(self.path_mesh)
        self.vmesh.export(self.path_save)
        self.vmesh_save = VisibleMesh(self.path_save)

    def test_can_write_header(self):
        self.assertEqual(self.vmesh_save.head, self.vmesh.head)

    def test_can_write_u1(self):
        self.assertEqual(self.vmesh_save.u1, self.vmesh.u1)
    
    def test_can_write_geomtable(self):
        self.assertEqual(self.vmesh_save.geomnum, self.vmesh.geomnum)
        self.assertEqual(self.vmesh_save.geoms, self.vmesh.geoms)
        for geomId, geom in enumerate(self.vmesh_save.geoms):
            self.assertEqual(geom.lodnum, self.vmesh.geoms[geomId].lodnum)
    
    def test_can_write_vertex_attributes_table(self):
        self.assertEqual(self.vmesh_save.vertattribnum, self.vmesh.vertattribnum)
        self.assertEqual(self.vmesh_save.vertex_attributes, self.vmesh.vertex_attributes)

    def test_can_write_vertices(self):
        self.assertEqual(self.vmesh_save.vertformat, self.vmesh.vertformat)
        self.assertEqual(self.vmesh_save.vertstride, self.vmesh.vertstride)
        self.assertEqual(self.vmesh_save.vertnum, self.vmesh.vertnum)
        self.assertEqual(self.vmesh_save.vertices, self.vmesh.vertices)
    
    def test_can_write_indices(self):
        self.assertEqual(self.vmesh_save.indexnum, self.vmesh.indexnum)
        self.assertEqual(self.vmesh_save.index, self.vmesh.index)
    
    def test_can_write_u2(self):
        self.assertEqual(self.vmesh_save.u2, self.vmesh.u2)
    
    def test_can_write_lods(self):
        for geomId, geom in enumerate(self.vmesh_save.geoms):
            for lodId, lod in enumerate(geom.lods):
                other_lod = self.vmesh.geoms[geomId].lods[lodId]
                self.assertEqual(lod, other_lod)

class test_visiblemesh_write_skinnedmesh_kits(unittest.TestCase):

    def setUp(self):
        self.path_mesh = 'tests/samples/skinnedmesh/kits/ru/meshes/ru_kits.skinnedmesh'
        self.path_save = 'tests/generated/skinnedmesh/write/kits/ru/meshes/ru_kits.skinnedmesh'
        self.vmesh = VisibleMesh(self.path_mesh)
        self.vmesh.export(self.path_save)
        self.vmesh_save = VisibleMesh(self.path_save)

    def test_can_write_lods(self):
        for geomId, geom in enumerate(self.vmesh_save.geoms):
            for lodId, lod in enumerate(geom.lods):
                other_lod = self.vmesh.geoms[geomId].lods[lodId]
                self.assertEqual(lod, other_lod)