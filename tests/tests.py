import unittest
import unittest.mock as mock
import tempfile
import os
import sys
import struct

import bf2
import mesher


class TestMod(unittest.TestCase):
    
    @mock.patch('os.getcwd')
    def test_can_find_mod_root(self, mock_function):
        mocked_mod_root = os.sep.join(['games', 'PRGame', 'mods', 'pr'])
        mocked_work_dir = os.sep.join(['games', 'PRGame', 'mods', 'pr', 'readme'])
        mock_function.return_value = mocked_work_dir

        mod = bf2.Mod()
        self.assertTrue(mod.find_mod_root() == mocked_mod_root)

    def test_mod_init_with_mod_root(self):
        mod = bf2.Mod()
        self.assertTrue('mods' in mod.root.split(os.sep))

    def test_can_get_object_path(self):
        test_object_name = 'faction_type_name_variant'
        test_folder = os.path.join('objects', 'vehicles', 'land')
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_mod = os.path.join(temp_dir, test_folder)
            os.makedirs(temp_mod)
            with tempfile.NamedTemporaryFile('w', suffix='.con', dir=temp_mod, delete=False) as confile:
                confile.write('ObjectTemplate.create PlayerControlObject ' + test_object_name)
                confile.close()
                mod = bf2.Mod()
                mod.root = temp_dir
                self.assertTrue(mod.get_object_path(test_object_name) == os.path.join(temp_mod, test_object_name, confile.name))

#@unittest.skip('testing failed mesh load')
class TestStdMeshReading(unittest.TestCase):

    def setUp(self):
        # NOTE: THIS IS VERY SPECIFIC TESTS FOR TEST MODEL READ
        test_object_std = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box1', 'meshes', 'evil_box1.staticmesh'])
        test_object_alt_uvw = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box2', 'meshes', 'evil_box2.staticmesh'])
        test_object_two_lods = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box3', 'meshes', 'evil_box3.staticmesh'])
        test_object_dest = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box4', 'meshes', 'evil_box4.staticmesh'])
        test_object_merged = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box5', 'meshes', 'evil_box5.staticmesh'])

        self.path_object_std = os.path.join(bf2.Mod().root, test_object_std)
        self.path_object_alt_uvw = os.path.join(bf2.Mod().root, test_object_alt_uvw)
        self.path_object_two_lods = os.path.join(bf2.Mod().root, test_object_two_lods)
        self.path_object_dest = os.path.join(bf2.Mod().root, test_object_dest)
        self.path_object_merged = os.path.join(bf2.Mod().root, test_object_merged)

    def test_can_read_header(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_head(meshfile)
            
        self.assertTrue(vmesh.head.u1 == 0)
        self.assertTrue(vmesh.head.version in [10, 6, 11])
        self.assertTrue(vmesh.head.u3 == 0)
        self.assertTrue(vmesh.head.u4 == 0)
        self.assertTrue(vmesh.head.u5 == 0)
        self.assertTrue(vmesh._tail == 20)

    def test_can_read_u1_bfp4f_version(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_u1_bfp4f_version(meshfile)
            
        self.assertTrue(vmesh.u1 == 0)
        self.assertTrue(vmesh._tail == 21)

    def test_can_read_geomnum_mesh_std(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_geomnum(meshfile)
            
        self.assertTrue(vmesh.geomnum == 1)
        self.assertTrue(vmesh._tail == 25)
    
    def test_can_read_geomnum_mesh_dest(self):
        with open(self.path_object_dest, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_geomnum(meshfile)
            
        self.assertTrue(vmesh.geomnum == 2)
        self.assertTrue(vmesh._tail == 25)

    def test_can_read_geom_table_mesh_std(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_geoms(meshfile)

        self.assertTrue(len(vmesh.geoms) == 1)
        self.assertTrue(vmesh.geoms[0].lodnum == 1)
        self.assertTrue(vmesh._tail == 29)
    
    def test_can_read_geom_table_mesh_two_lods(self):
        with open(self.path_object_two_lods, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_geoms(meshfile)

        self.assertTrue(len(vmesh.geoms) == 1)
        self.assertTrue(vmesh.geoms[0].lodnum == 2)
        self.assertTrue(vmesh._tail == 29)
    
    def test_can_read_geom_table_mesh_dest(self):
        with open(self.path_object_dest, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_geoms(meshfile)

        self.assertTrue(len(vmesh.geoms) == 2)
        self.assertTrue(vmesh.geoms[0].lodnum == 2)
        self.assertTrue(vmesh.geoms[1].lodnum == 2)
        self.assertTrue(vmesh._tail == 33)

    def test_can_read_vertattribnum_mesh_std(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_vertattribnum(meshfile)

        self.assertTrue(vmesh.vertattribnum == 9)
        self.assertTrue(vmesh._tail == 33)

    def test_can_read_vertattribnum_mesh_dest(self):
        with open(self.path_object_dest, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_vertattribnum(meshfile)

        self.assertTrue(vmesh.vertattribnum == 9)
        self.assertTrue(vmesh._tail == 37)
    
    def test_can_read_vertex_attribute_table(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_vertext_attribute_table(meshfile)

        self.assertTrue(vmesh.vertattrib[0] == (0, 0, 2, 0))
        self.assertTrue(vmesh.vertattrib[1] == (0, 12, 2, 3))
        self.assertTrue(vmesh.vertattrib[2] == (0, 24, 4, 2))
        self.assertTrue(vmesh.vertattrib[3] == (0, 28, 1, 5))
        self.assertTrue(vmesh.vertattrib[4] == (0, 36, 1, 261))
        self.assertTrue(vmesh.vertattrib[5] == (0, 44, 1, 517))
        self.assertTrue(vmesh.vertattrib[6] == (0, 52, 1, 773))
        self.assertTrue(vmesh.vertattrib[7] == (0, 60, 2, 6))
        self.assertTrue(vmesh.vertattrib[8] == (255, 0, 17, 0))
        self.assertTrue(vmesh._tail == 105)

    def test_can_read_vertformat(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_vertformat(meshfile)

        self.assertTrue(vmesh.vertformat == 4)
        self.assertTrue(vmesh._tail == 109)

    def test_can_read_vertstride(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_vertstride(meshfile)

        self.assertTrue(vmesh.vertstride == 72)
        self.assertTrue(vmesh._tail == 113)

    def test_can_read_vertnum(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_vertnum(meshfile)

        self.assertTrue(vmesh.vertnum == 25)
        self.assertTrue(vmesh._tail == 117)

    def test_can_read_vertex_block(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_vertex_block(meshfile)

        self.assertTrue(len(vmesh.vertices) == 450)
        self.assertTrue(vmesh._tail == 1917)

    def test_can_read_indexnum(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_indexnum(meshfile)

        self.assertTrue(vmesh.indexnum == 36)
        self.assertTrue(vmesh._tail == 1921)

    def test_can_read_index_block(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_index_block(meshfile)

        self.assertTrue(len(vmesh.index) == 36)
        self.assertTrue(vmesh._tail == 1993)

    def test_can_read_u2(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_u2(meshfile)

        self.assertTrue(vmesh.u2 is 8)
        self.assertTrue(vmesh._tail == 1997)

    def test_can_read_nodes(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_nodes(meshfile)

        self.assertTrue(vmesh.geoms[0].lod[0].min == (-0.5, 0, -0.5))
        self.assertTrue(vmesh.geoms[0].lod[0].max == (0.5, 1.0, 0.5))
        #self.assertTrue(vmesh.geoms[0].lod[0].pivot == (0.5, 1.0, 0.5)) # some old bundleds?
        self.assertTrue(vmesh.geoms[0].lod[0].nodenum == 1)
        self.assertTrue(vmesh._tail == 2089)

    def test_can_read_materials(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_materials(meshfile)

        self.assertTrue(vmesh.geoms[0].lod[0].matnum == 1)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].alphamode == 0)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].fxfile == b'StaticMesh.fx')
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].technique == b'Base')
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].mapnum == 2)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].map[0] == b'objects/staticobjects/test/evil_box1/textures/evil_box1_c.dds')
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].map[1] == b'Common\Textures\SpecularLUT_pow36.dds')
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].vstart == 0)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].istart == 0)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].inum == 36)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].vnum == 25)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].u4 == 8064)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].u5 == 65535)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].nmin == (-0.5, 0.0, -0.5))
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].nmax == (0.5, 1.0, 0.5))
        self.assertTrue(vmesh.geoms[0].lod[0].polycount == 12)
        self.assertTrue(vmesh._tail == 2280)

    def test_can_load_bf2_mesh(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(isinstance(vmesh, mesher.StdMesh))

    def test_meshes_diff(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh2 = mesher.LoadBF2Mesh(self.path_object_merged)

        self.assertTrue(vmesh.head == vmesh2.head)
        self.assertTrue(vmesh.u1 == vmesh2.u1)
        self.assertTrue(vmesh.geomnum == vmesh2.geomnum)
        self.assertTrue(len(vmesh.geoms) == len(vmesh2.geoms) == 1)
        self.assertTrue(vmesh.geoms[0].lodnum == vmesh2.geoms[0].lodnum)
        self.assertTrue(len(vmesh.geoms[0].lod) == len(vmesh2.geoms[0].lod) == 1)
        self.assertTrue(vmesh.geoms[0].lod[0].min == vmesh2.geoms[0].lod[0].min)
        self.assertTrue(vmesh.geoms[0].lod[0].max != vmesh2.geoms[0].lod[0].max) # diff
        self.assertTrue(vmesh2.geoms[0].lod[0].max == (1.5, 1.0, 0.5))
        self.assertTrue(vmesh.geoms[0].lod[0].nodenum == vmesh2.geoms[0].lod[0].nodenum)
        self.assertTrue(vmesh.geoms[0].lod[0].node == vmesh2.geoms[0].lod[0].node) # not geometry?
        self.assertTrue(vmesh.geoms[0].lod[0].polycount != vmesh2.geoms[0].lod[0].polycount != 0) # diff
        self.assertTrue(vmesh.vertattribnum == vmesh2.vertattribnum)
        self.assertTrue(vmesh.vertattrib == vmesh2.vertattrib)
        self.assertTrue(vmesh.vertformat == vmesh2.vertformat)
        self.assertTrue(vmesh.vertstride == vmesh2.vertstride)
        self.assertTrue(vmesh.vertnum != vmesh2.vertnum) # diff
        self.assertTrue(vmesh.vertices != vmesh2.vertices) # diff it's appears that this is real geom data, perhaps just add?
        #for index, id in enumerate(vmesh.index):
            #print('index[{}] {}'.format(index, id))
        self.assertTrue(vmesh.indexnum != vmesh2.indexnum) # diff
        self.assertTrue(vmesh.index != vmesh2.index) # diff reversed order?
        self.assertTrue(vmesh.u2 == vmesh2.u2)
        self.assertTrue(vmesh.geoms[0].lod[0].matnum == vmesh2.geoms[0].lod[0].matnum == 1)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].alphamode == vmesh2.geoms[0].lod[0].mat[0].alphamode)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].fxfile == vmesh2.geoms[0].lod[0].mat[0].fxfile)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].technique == vmesh2.geoms[0].lod[0].mat[0].technique)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].mapnum == vmesh2.geoms[0].lod[0].mat[0].mapnum)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].map[0] == vmesh2.geoms[0].lod[0].mat[0].map[0])
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].map[1] == vmesh2.geoms[0].lod[0].mat[0].map[1])
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].vstart == vmesh2.geoms[0].lod[0].mat[0].vstart)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].istart == vmesh2.geoms[0].lod[0].mat[0].istart)
        #print('vmesh inum = {}'.format(vmesh.geoms[0].lod[0].mat[0].inum))
        #print('vmesh2 inum = {}'.format(vmesh2.geoms[0].lod[0].mat[0].inum))
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].inum != vmesh2.geoms[0].lod[0].mat[0].inum) # diff
        #print('vmesh vnum = {}'.format(vmesh.geoms[0].lod[0].mat[0].vnum))
        #print('vmesh2 vnum = {}'.format(vmesh2.geoms[0].lod[0].mat[0].vnum))
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].vnum != vmesh2.geoms[0].lod[0].mat[0].vnum) # diff
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].u4 == vmesh2.geoms[0].lod[0].mat[0].u4)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].u5 == vmesh2.geoms[0].lod[0].mat[0].u5)
        #print('vmesh nmax = {}'.format(vmesh.geoms[0].lod[0].mat[0].nmax))
        #print('vmesh2 nmax = {}'.format(vmesh2.geoms[0].lod[0].mat[0].nmax))
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].nmin == vmesh2.geoms[0].lod[0].mat[0].nmin)
        self.assertTrue(vmesh.geoms[0].lod[0].mat[0].nmax != vmesh2.geoms[0].lod[0].mat[0].nmax) # diff
        #raise

    @unittest.skip('i\o intensive')
    def test_can_read_PR_MESHES_REPO_1490(self):
        counter = 0
        for dir, dirnames, filenames in os.walk(os.path.join(bf2.Mod().root, 'objects', 'staticobjects')):
            for filename in filenames:
                if filename.split('.')[-1].lower() == 'staticmesh':
                    counter += 1
                    try:
                        vmesh = mesher.LoadBF2Mesh(os.path.join(bf2.Mod().root, dir, filename))
                    except MemoryError:
                        print('Failed to load {}'.format(os.path.join(bf2.Mod().root, dir, filename)))
        print(counter)
        #raise
    
class TestStdMeshReading_Specials(unittest.TestCase):

    # objects\staticobjects\Bridges\EoD_Bridge_Big\Meshes\eod_bridge_big.staticmesh
    # it has version 4 and inum and vnum in material
    def test_can_read_not_skinned_mesh_version_4(self):
        path_mesh = os.path.join(bf2.Mod().root, 'objects', 'staticobjects', 'Bridges', 'EoD_Bridge_Big', 'Meshes', 'eod_bridge_big.staticmesh')
        #vmesh = mesher.LoadBF2Mesh(path_mesh)
        with open(path_mesh, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_materials(meshfile)
        

class TestStdMeshWriting(unittest.TestCase):

    def setUp(self):
        # NOTE: THIS IS VERY SPECIFIC TESTS FOR TEST MODEL READ
        test_object_std = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box1', 'meshes', 'evil_box1.staticmesh'])
        test_object_alt_uvw = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box2', 'meshes', 'evil_box2.staticmesh'])
        test_object_two_lods = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box3', 'meshes', 'evil_box3.staticmesh'])
        test_object_dest = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box4', 'meshes', 'evil_box4.staticmesh'])
        test_object_merged = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box5', 'meshes', 'evil_box5.staticmesh'])
        
        test_object_clone = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box1', 'meshes', 'evil_box1_clone.staticmesh'])
        
        self.path_object_std = os.path.join(bf2.Mod().root, test_object_std)
        self.path_object_std = os.path.join(bf2.Mod().root, test_object_std)
        self.path_object_alt_uvw = os.path.join(bf2.Mod().root, test_object_alt_uvw)
        self.path_object_two_lods = os.path.join(bf2.Mod().root, test_object_two_lods)
        self.path_object_dest = os.path.join(bf2.Mod().root, test_object_dest)
        self.path_object_merged = os.path.join(bf2.Mod().root, test_object_merged)

        self.path_object_clone = os.path.join(bf2.Mod().root, test_object_clone)

    def tearDown(self):
        try:
            os.remove(self.path_object_clone)
        except FileNotFoundError:
            print('Nothing to clean up')

    def test_can_write_header(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_header(self.path_object_clone)
        
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_head(meshfile)

        self.assertTrue(vmesh2.head.u1 == vmesh.head.u1)
        self.assertTrue(vmesh2.head.version == vmesh.head.version)
        self.assertTrue(vmesh2.head.u3 is vmesh.head.u3)
        self.assertTrue(vmesh2.head.u4 is vmesh.head.u4)
        self.assertTrue(vmesh2.head.u5 is vmesh.head.u5)

    def test_can_write_u1_bfp4f_version(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_u1_bfp4f_version(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_u1_bfp4f_version(meshfile)

        self.assertTrue(vmesh2.u1 == vmesh.u1)

    def test_can_write_geomnum_mesh_std(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_geomnum(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_geomnum(meshfile)

        self.assertTrue(vmesh2.geomnum == vmesh.geomnum)

    def test_can_write_geomnum_mesh_dest(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_dest)
        vmesh._write_geomnum(self.path_object_clone)
    
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_geomnum(meshfile)
            
        self.assertTrue(vmesh2.geomnum == vmesh.geomnum)

    def test_can_write_geom_table_mesh_std(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_geom_table(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_geoms(meshfile)

        self.assertTrue(len(vmesh2.geoms) == len(vmesh.geoms))
        self.assertTrue(vmesh2.geoms[0].lodnum == vmesh.geoms[0].lodnum)

    def test_can_write_geom_table_mesh_two_lods(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_two_lods)
        vmesh._write_geom_table(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_geoms(meshfile)

        self.assertTrue(len(vmesh2.geoms) == len(vmesh.geoms))
        self.assertTrue(vmesh2.geoms[0].lodnum == vmesh.geoms[0].lodnum)

    def test_can_write_geom_table_mesh_dest(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_dest)
        vmesh._write_geom_table(self.path_object_clone)
        
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_geoms(meshfile)

        self.assertTrue(len(vmesh2.geoms) == len(vmesh.geoms))
        self.assertTrue(vmesh2.geoms[0].lodnum == vmesh.geoms[0].lodnum)
        self.assertTrue(vmesh2.geoms[1].lodnum == vmesh.geoms[1].lodnum)

    def test_can_write_vertattribnum_mesh_std(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertattribnum(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_vertattribnum(meshfile)

        self.assertTrue(vmesh2.vertattribnum == vmesh.vertattribnum)

    def test_can_write_vertattribnum_mesh_dest(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_dest)
        vmesh._write_vertattribnum(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_vertattribnum(meshfile)

        self.assertTrue(vmesh2.vertattribnum == vmesh.vertattribnum)

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

    def test_can_write_vertformat(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertformat(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_vertformat(meshfile)

        self.assertTrue(vmesh2.vertformat == vmesh.vertformat)

    def test_can_write_vertstride(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertstride(self.path_object_clone)
    
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_vertstride(meshfile)

        self.assertTrue(vmesh2.vertstride == vmesh.vertstride)

    def test_can_write_vertnum(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertnum(self.path_object_clone)
    
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_vertnum(meshfile)

        self.assertTrue(vmesh2.vertnum == vmesh.vertnum)

    def test_can_write_vertex_block(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertex_block(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_vertex_block(meshfile)

        self.assertTrue(len(vmesh2.vertices) == len(vmesh2.vertices))

    def test_can_write_indexnum(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_indexnum(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_indexnum(meshfile)

        self.assertTrue(vmesh2.indexnum == vmesh.indexnum)

    def test_can_write_index_block(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_index_block(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_index_block(meshfile)

        self.assertTrue(len(vmesh2.index) == len(vmesh2.index))

    def test_can_write_u2(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_u2(self.path_object_clone)
        
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_u2(meshfile)

        self.assertTrue(vmesh2.u2 == vmesh.u2)

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

    def test_can_write_materials(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh._write_materials(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = mesher.StdMesh()
            vmesh2._read_materials(meshfile)

        self.assertTrue(vmesh2.geoms[0].lod[0].matnum == vmesh2.geoms[0].lod[0].matnum)
        self.assertTrue(vmesh2.geoms[0].lod[0].mat == vmesh2.geoms[0].lod[0].mat)
        self.assertTrue(vmesh2.geoms[0].lod[0].polycount == vmesh2.geoms[0].lod[0].polycount)

    def test_can_load_bf2_mesh_cloned(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh.write_file_data(self.path_object_clone)
        
        vmesh2 = mesher.LoadBF2Mesh(self.path_object_clone)

        self.assertTrue(vmesh2._tail == vmesh._tail)
        





