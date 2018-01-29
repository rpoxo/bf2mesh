import unittest
import tempfile
import os
import sys
import struct
import shutil
import filecmp

import bf2
import modmesh
from modmesh import D3DDECLTYPE, D3DDECLUSAGE

import tests.mock_mesh as mocks

class TestVisMeshRead(unittest.TestCase):

    def setUp(self):
        # test for simple static box - static&destoryable
        self.path_object_static = os.path.join(*['tests', 'samples', 'evil_box', 'meshes', 'evil_box.staticmesh'])
        self.path_object_dest = os.path.join(*['tests', 'samples', 'evil_box_destroyable', 'meshes', 'evil_box_destroyable.staticmesh'])
        self.path_object_static_clone = os.path.join(*['tests', 'generated', 'write', 'evil_box', 'meshes', 'evil_box.staticmesh'])

        # test for vehicle depot - bundledmesh
        # objects\common\vehicle_depot\meshes
        self.path_object_bundled = os.path.join(*['tests', 'samples', 'vehicle_depot', 'meshes', 'vehicle_depot.bundledmesh'])
        self.path_object_bundled_clone = os.path.join(*['tests', 'generated', 'write', 'vehicle_depot', 'meshes', 'vehicle_depot.staticmesh'])
        
        # test for mec kits - skinnedmesh
        # objects\kits\Mec
        self.path_object_skinned = os.path.join(*['tests', 'samples', 'kits', 'mec', 'Meshes', 'mec_kits.skinnedMesh'])
        self.path_object_skinned_clone = os.path.join(*['tests', 'generated', 'write', 'kits', 'mec', 'Meshes', 'mec_kits.skinnedMesh'])

    @classmethod
    def tearDownClass(cls):
        try:
            path_clear = os.path.join(*['tests', 'generated', 'write'])
            shutil.rmtree(path_clear)
        except FileNotFoundError:
            print('Nothing to clean up')

    def test_can_write_header(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh._write_header(self.path_object_static_clone)
        
        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_head(meshfile)

        self.assertTrue(vmesh2.head.u1 == vmesh.head.u1)
        self.assertTrue(vmesh2.head.version == vmesh.head.version)
        self.assertTrue(vmesh2.head.u3 is vmesh.head.u3)
        self.assertTrue(vmesh2.head.u4 is vmesh.head.u4)
        self.assertTrue(vmesh2.head.u5 is vmesh.head.u5)

    def test_can_write_u1_bfp4f_version(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh._write_u1_bfp4f_version(self.path_object_static_clone)

        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_u1_bfp4f_version(meshfile)

        self.assertTrue(vmesh2.u1 == vmesh.u1)

    def test_can_write_geomnum_mesh_std(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh._write_geomnum(self.path_object_static_clone)

        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_geomnum(meshfile)

        self.assertTrue(vmesh2.geomnum == vmesh.geomnum)

    def test_can_write_geomnum_mesh_dest(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_dest)
        vmesh._write_geomnum(self.path_object_static_clone)
    
        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_geomnum(meshfile)
            
        self.assertTrue(vmesh2.geomnum == vmesh.geomnum)

    def test_can_write_geom_table_mesh_std(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh._write_geom_table(self.path_object_static_clone)

        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_geom_table(meshfile)

        self.assertTrue(len(vmesh2.geoms) == len(vmesh.geoms))
        self.assertTrue(vmesh2.geoms[0].lodnum == vmesh.geoms[0].lodnum)

    def test_can_write_geom_table_mesh_dest(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_dest)
        vmesh._write_geom_table(self.path_object_static_clone)
        
        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_geom_table(meshfile)

        self.assertTrue(len(vmesh2.geoms) == len(vmesh.geoms))
        self.assertTrue(vmesh2.geoms[0].lodnum == vmesh.geoms[0].lodnum)
        self.assertTrue(vmesh2.geoms[1].lodnum == vmesh.geoms[1].lodnum)

    def test_can_write_vertattribnum_mesh_std(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh._write_vertattribnum(self.path_object_static_clone)

        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_vertattribnum(meshfile)

        self.assertTrue(vmesh2.vertattribnum == vmesh.vertattribnum)

    def test_can_write_vertex_attribute_table(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh._write_vertattrib_table(self.path_object_static_clone)

        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_vertattrib_table(meshfile)

        for attrib_id, attrib in enumerate(vmesh.vertattrib):
            self.assertTrue(attrib == vmesh2.vertattrib[attrib_id])

    def test_can_write_vertformat(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh._write_vertformat(self.path_object_static_clone)

        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_vertformat(meshfile)

        self.assertTrue(vmesh2.vertformat == vmesh.vertformat)

    def test_can_write_vertstride(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh._write_vertstride(self.path_object_static_clone)
    
        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_vertstride(meshfile)

        self.assertTrue(vmesh2.vertstride == vmesh.vertstride)

    def test_can_write_vertnum(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh._write_vertnum(self.path_object_static_clone)
    
        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_vertnum(meshfile)

        self.assertTrue(vmesh2.vertnum == vmesh.vertnum)

    def test_can_write_vertex_block(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh._write_vertex_block(self.path_object_static_clone)

        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_vertex_block(meshfile)

        self.assertTrue(len(vmesh2.vertices) == len(vmesh2.vertices))

    def test_can_write_indexnum(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh._write_indexnum(self.path_object_static_clone)

        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_indexnum(meshfile)

        self.assertTrue(vmesh2.indexnum == vmesh.indexnum)

    def test_can_write_index_block(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh._write_index_block(self.path_object_static_clone)

        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_index_block(meshfile)

        self.assertTrue(len(vmesh2.index) == len(vmesh2.index))

    def test_can_write_u2(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh._write_u2(self.path_object_static_clone)
        
        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_u2(meshfile)

        self.assertTrue(vmesh2.u2 == vmesh.u2)

    def test_can_write_nodes(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh._write_nodes(self.path_object_static_clone)

        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_nodes(meshfile)

        self.assertTrue(vmesh2.geoms[0].lods[0].min == vmesh.geoms[0].lods[0].min)
        self.assertTrue(vmesh2.geoms[0].lods[0].max == vmesh.geoms[0].lods[0].max)
        #self.assertTrue(vmesh.geoms[0].lods[0].pivot == (0.5, 1.0, 0.5)) # some old bundleds?
        self.assertTrue(vmesh2.geoms[0].lods[0].nodenum == vmesh.geoms[0].lods[0].nodenum)
        self.assertTrue(vmesh2.geoms[0].lods[0].nodes == vmesh.geoms[0].lods[0].nodes)

    def test_can_write_materials(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh._write_materials(self.path_object_static_clone)

        with open(self.path_object_static_clone, 'rb') as meshfile:
            vmesh2 = modmesh.VisMesh()
            vmesh2._read_materials(meshfile)

        for geom_id, geom in enumerate(vmesh.geoms):
            for lod_id, lod in enumerate(geom.lods):
                self.assertTrue(lod.matnum == vmesh2.geoms[geom_id].lods[lod_id].matnum)
                #for material_id, material in enumerate(lod.materials):
                    #for key, value in material.__dict__.items():
                    #    print('"{:.10}" : {}'.format(key, value))
                    #for key, value in vmesh2.geoms[geom_id].lods[lod_id].materials[material_id].__dict__.items():
                    #    print('"{:.10}" : {}'.format(key, value))
                    #self.assertTrue(material == vmesh2.geoms[geom_id].lods[lod_id].materials[material_id])
                self.assertTrue(lod.polycount == vmesh2.geoms[geom_id].lods[lod_id].polycount)
    
    def test_can_write_staticmesh_identical(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        vmesh.save(self.path_object_static_clone)
        
        self.assertTrue(filecmp.cmp(self.path_object_static, self.path_object_static_clone))
    
    def test_can_write_bundledmesh_identical(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_bundled)
        vmesh.save(self.path_object_bundled_clone)
        
        self.assertTrue(filecmp.cmp(self.path_object_bundled, self.path_object_bundled_clone))

    def test_can_write_skinnedmesh_identical(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_skinned)
        vmesh.save(self.path_object_skinned_clone)
        
        self.assertTrue(filecmp.cmp(self.path_object_skinned, self.path_object_skinned_clone))

    
if __name__ == '__main__':
    unittest.main()
