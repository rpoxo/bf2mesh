import unittest
import os
import struct

from tests_basic import chunks, TestMod

import bf2
import mesher
import creator

@unittest.skip('temporary disabled until finishing lm sizes script for outlawz')
class TestStdMeshCreateBox(unittest.TestCase):

    def setUp(self):
        test_object_std = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box', 'meshes', 'evil_box.staticmesh'])
        test_object_generated = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box_generated', 'meshes', 'evil_box_created.staticmesh'])

        self.path_object_std = os.path.join(bf2.Mod().root, test_object_std)
        self.path_object_generated = os.path.join(bf2.Mod().root, test_object_generated)
        
    def test_can_create_header(self):
        box = creator.Box()

        self.assertTrue(box.vmesh.head.u1 == 0)
        self.assertTrue(box.vmesh.head.version == 11)
        self.assertTrue(box.vmesh.head.u3 is 0)
        self.assertTrue(box.vmesh.head.u4 is 0)
        self.assertTrue(box.vmesh.head.u5 is 0)
    

    def test_can_create_u1_bfp4f_version(self):
        box = creator.Box()

        self.assertTrue(box.vmesh.u1 == 0)

    @unittest.skip('copypasta')
    def test_can_write_geomnum_mesh_std(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_geomnum(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_geomnum(meshfile)

        self.assertTrue(vmesh2.geomnum == vmesh.geomnum)

    @unittest.skip('copypasta')
    def test_can_write_geomnum_mesh_dest(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_dest)
        vmesh._write_geomnum(self.path_object_clone)
    
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_geomnum(meshfile)
            
        self.assertTrue(vmesh2.geomnum == vmesh.geomnum)

    @unittest.skip('copypasta')
    def test_can_write_geom_table_mesh_std(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_geom_table(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_geoms(meshfile)

        self.assertTrue(len(vmesh2.geoms) == len(vmesh.geoms))
        self.assertTrue(vmesh2.geoms[0].lodnum == vmesh.geoms[0].lodnum)

    @unittest.skip('copypasta')
    def test_can_write_geom_table_mesh_two_lods(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_two_lods)
        vmesh._write_geom_table(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_geoms(meshfile)

        self.assertTrue(len(vmesh2.geoms) == len(vmesh.geoms))
        self.assertTrue(vmesh2.geoms[0].lodnum == vmesh.geoms[0].lodnum)

    @unittest.skip('copypasta')
    def test_can_write_geom_table_mesh_dest(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_dest)
        vmesh._write_geom_table(self.path_object_clone)
        
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_geoms(meshfile)

        self.assertTrue(len(vmesh2.geoms) == len(vmesh.geoms))
        self.assertTrue(vmesh2.geoms[0].lodnum == vmesh.geoms[0].lodnum)
        self.assertTrue(vmesh2.geoms[1].lodnum == vmesh.geoms[1].lodnum)

    @unittest.skip('copypasta')
    def test_can_write_vertattribnum_mesh_std(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertattribnum(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_vertattribnum(meshfile)

        self.assertTrue(vmesh2.vertattribnum == vmesh.vertattribnum)

    @unittest.skip('copypasta')
    def test_can_write_vertattribnum_mesh_dest(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_dest)
        vmesh._write_vertattribnum(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_vertattribnum(meshfile)

        self.assertTrue(vmesh2.vertattribnum == vmesh.vertattribnum)

    @unittest.skip('copypasta')
    def test_can_write_vertex_attribute_table(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertex_attribute_table(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_vertext_attribute_table(meshfile)

        self.assertTrue(vmesh2.vertattrib[0] == vmesh.vertattrib[0])
        self.assertTrue(vmesh2.vertattrib[1] == vmesh.vertattrib[1])
        self.assertTrue(vmesh2.vertattrib[2] == vmesh.vertattrib[2])
        self.assertTrue(vmesh2.vertattrib[3] == vmesh.vertattrib[3])
        self.assertTrue(vmesh2.vertattrib[4] == vmesh.vertattrib[4])
        self.assertTrue(vmesh2.vertattrib[5] == vmesh.vertattrib[5])
        self.assertTrue(vmesh2.vertattrib[6] == vmesh.vertattrib[6])
        self.assertTrue(vmesh2.vertattrib[7] == vmesh.vertattrib[7])
        self.assertTrue(vmesh2.vertattrib[8] == vmesh.vertattrib[8])

    @unittest.skip('copypasta')
    def test_can_write_vertformat(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertformat(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_vertformat(meshfile)

        self.assertTrue(vmesh2.vertformat == vmesh.vertformat)

    @unittest.skip('copypasta')
    def test_can_write_vertstride(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertstride(self.path_object_clone)
    
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_vertstride(meshfile)

        self.assertTrue(vmesh2.vertstride == vmesh.vertstride)

    @unittest.skip('copypasta')
    def test_can_write_vertnum(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertnum(self.path_object_clone)
    
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_vertnum(meshfile)

        self.assertTrue(vmesh2.vertnum == vmesh.vertnum)

    @unittest.skip('copypasta')
    def test_can_write_vertex_block(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertex_block(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_vertex_block(meshfile)

        self.assertTrue(len(vmesh2.vertices) == len(vmesh2.vertices))

    @unittest.skip('copypasta')
    def test_can_write_indexnum(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_indexnum(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_indexnum(meshfile)

        self.assertTrue(vmesh2.indexnum == vmesh.indexnum)

    @unittest.skip('copypasta')
    def test_can_write_index_block(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_index_block(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_index_block(meshfile)

        self.assertTrue(len(vmesh2.index) == len(vmesh2.index))

    @unittest.skip('copypasta')
    def test_can_write_u2(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_u2(self.path_object_clone)
        
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_u2(meshfile)

        self.assertTrue(vmesh2.u2 == vmesh.u2)

    @unittest.skip('copypasta')
    def test_can_write_nodes(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_nodes(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_nodes(meshfile)

        self.assertTrue(vmesh2.geoms[0].lod[0].min == vmesh.geoms[0].lod[0].min)
        self.assertTrue(vmesh2.geoms[0].lod[0].max == vmesh.geoms[0].lod[0].max)
        #self.assertTrue(vmesh.geoms[0].lod[0].pivot == (0.5, 1.0, 0.5)) # some old bundleds?
        self.assertTrue(vmesh2.geoms[0].lod[0].nodenum == vmesh.geoms[0].lod[0].nodenum)
        self.assertTrue(vmesh2.geoms[0].lod[0].node == vmesh.geoms[0].lod[0].node)

    @unittest.skip('copypasta')
    def test_can_write_materials(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_materials(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_materials(meshfile)

        self.assertTrue(vmesh2.geoms[0].lod[0].matnum == vmesh2.geoms[0].lod[0].matnum)
        self.assertTrue(vmesh2.geoms[0].lod[0].mat == vmesh2.geoms[0].lod[0].mat)
        self.assertTrue(vmesh2.geoms[0].lod[0].polycount == vmesh2.geoms[0].lod[0].polycount)

    @unittest.skip('copypasta')
    def test_can_write_vertices_attiributes_to_vertices(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_filedata(meshfile)
            vmesh._generate_vertices_attributes()

        vertices_new = []
        for vertice in vmesh.vertices_attributes:
            for axis in vertice['position']:
                vertices_new.append(axis)
            for axis in vertice['normal']:
                vertices_new.append(axis)
            vertices_new.append(vertice['blend_indices'])

            vertices_new.append(vertice['uv1'][0])
            vertices_new.append(vertice['uv1'][1])
            
            vertices_new.append(vertice['uv2'][0])
            vertices_new.append(vertice['uv2'][1])
            
            vertices_new.append(vertice['uv3'][0])
            vertices_new.append(vertice['uv3'][1])
            
            vertices_new.append(vertice['uv4'][0])
            vertices_new.append(vertice['uv4'][1])
            
            if vmesh.vertstride == 80:
                vertices_new.append(vertice['uv5'][0])
                vertices_new.append(vertice['uv5'][1])
            
            for axis in vertice['tangent']:
                vertices_new.append(axis)

        # converting to tuple after generating
        vertices_new = tuple(vertices_new)

        self.assertTrue(len(vmesh.vertices) == len(vertices_new))
        self.assertTrue(vmesh.vertices == vertices_new)

    @unittest.skip('copypasta')
    def test_can_load_bf2_mesh_cloned(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh.write_file_data(self.path_object_clone)
        
        vmesh2 = mesher.LoadBF2Mesh(self.path_object_clone)

        self.assertTrue(vmesh2._tail == vmesh._tail)
    
