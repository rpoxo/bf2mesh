import unittest
import unittest.mock as mock
import tempfile
import os
import sys
import struct

import bf2
import mesher

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

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
        test_object_2merge = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box6', 'meshes', 'evil_box6.staticmesh'])

        self.path_object_std = os.path.join(bf2.Mod().root, test_object_std)
        self.path_object_alt_uvw = os.path.join(bf2.Mod().root, test_object_alt_uvw)
        self.path_object_two_lods = os.path.join(bf2.Mod().root, test_object_two_lods)
        self.path_object_dest = os.path.join(bf2.Mod().root, test_object_dest)
        self.path_object_merged = os.path.join(bf2.Mod().root, test_object_merged)
        self.path_object_2merge = os.path.join(bf2.Mod().root, test_object_2merge)

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
    
    def test_can_generate_vertices_attributes(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_filedata(meshfile)
        
        vmesh._generate_vertices_attributes()
        vertsinfo = []
        for chunk in chunks(vmesh.vertices, 18):
            position = tuple(chunk[0:3])
            normal = tuple(chunk[3:6])
            blend_indices = chunk[6]
            uv1 = tuple(chunk[7:9])
            uv2 = tuple(chunk[9:11])
            uv3 = tuple(chunk[11:13])
            uv4 = tuple(chunk[13:15])
            tangent = tuple(chunk[15:18])

            vert = {
                'position' : position,
                'normal' : normal,
                'blend_indices' : blend_indices,
                'uv1' : uv1,
                'uv2' : uv2,
                'uv3' : uv3,
                'uv4' : uv4,
                'tangent' : tangent
                }
            vertsinfo.append(vert)
        self.assertTrue(vmesh.vertices_attributes == vertsinfo)

    
class TestStdMeshReading_Specials(unittest.TestCase):

    # objects\staticobjects\Bridges\EoD_Bridge_Big\Meshes\eod_bridge_big.staticmesh
    # it has version 4 and inum and vnum in material
    def test_can_read_not_skinned_mesh_version_4(self):
        path_mesh = os.path.join(bf2.Mod().root, 'objects', 'staticobjects', 'Bridges', 'EoD_Bridge_Big', 'Meshes', 'eod_bridge_big.staticmesh')
        #vmesh = mesher.LoadBF2Mesh(path_mesh)
        with open(path_mesh, 'rb') as meshfile:
            vmesh = mesher.StdMesh()
            vmesh._read_materials(meshfile)
            
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

    def test_can_load_bf2_mesh_cloned(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh.write_file_data(self.path_object_clone)
        
        vmesh2 = mesher.LoadBF2Mesh(self.path_object_clone)

        self.assertTrue(vmesh2._tail == vmesh._tail)
        
class TestStdMeshMerging(unittest.TestCase):

    def setUp(self):
        # NOTE: THIS IS VERY SPECIFIC TESTS FOR TEST MODEL READ
        test_object_std = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box1', 'meshes', 'evil_box1.staticmesh'])
        test_object_std_2 = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box6', 'meshes', 'evil_box6.staticmesh'])
        test_object_merged = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box5', 'meshes', 'evil_box5.staticmesh'])
        test_object_generated = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box_generated', 'meshes', 'evil_box_generated.staticmesh'])
        
        self.path_object_std = os.path.join(bf2.Mod().root, test_object_std)
        self.path_object_std_2 = os.path.join(bf2.Mod().root, test_object_std_2)
        self.path_object_merged = os.path.join(bf2.Mod().root, test_object_merged)
        self.path_object_generated = os.path.join(bf2.Mod().root, test_object_generated)
        

    def tearDown(self):
        #try:
        #    os.remove(self.path_object_clone)
        #except FileNotFoundError:
        #    print('Nothing to clean up')
        pass
    
    @unittest.skip('theory')
    def test_can_move_mesh(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        
        for vertice in vmesh.vertices_attributes:
            new_position_x = vertice['position'][0] + 1.0
            new_position = (new_position_x, vertice['position'][1], vertice['position'][2])
            vertice['position'] = new_position
        vmesh._write_vertices_attributes()
        vmesh.write_file_data(self.path_object_generated)
    
    @unittest.skip('theory')
    def test_can_move_mesh_TOILET(self):
        #objects\staticobjects\pr\toilet
        path_object_toilet = os.path.join(bf2.Mod().root, os.path.join(*['objects', 'staticobjects', 'pr', 'toilet', 'meshes', 'toilet.staticmesh']))
        vmesh = mesher.LoadBF2Mesh(path_object_toilet)

        for vertice in vmesh.vertices_attributes:
            new_position_x = vertice['position'][0] + 5.0
            new_position = (new_position_x, vertice['position'][1], vertice['position'][2])
            vertice['position'] = new_position
        vmesh._write_vertices_attributes()
        vmesh.write_file_data(self.path_object_generated)
        
    
    @unittest.skip('theory')
    def test_meshes_read_plane(self):
        test_object_triangle = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box8', 'meshes', 'evil_box8.staticmesh'])
        test_object_plane = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box9', 'meshes', 'evil_box9.staticmesh'])
        test_object_plane2 = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box10', 'meshes', 'evil_box10.staticmesh'])

        path_object_triangle = os.path.join(bf2.Mod().root, test_object_triangle)
        path_object_plane = os.path.join(bf2.Mod().root, test_object_plane)
        path_object_plane2 = os.path.join(bf2.Mod().root, test_object_plane2)
        #vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        #vmesh = mesher.LoadBF2Mesh(path_object_triangle)
        vmesh = mesher.LoadBF2Mesh(path_object_plane)
        vmesh2 = mesher.LoadBF2Mesh(path_object_plane2)
        #print('vmesh.vertnum = {}'.format(vmesh.vertnum))
        #for index, vertice in enumerate(vmesh.vertices):
        #    print('v1[{}] {}'.format(index, vertice))
        #print('len(vmesh.vertices) = {}'.format(len(vmesh.vertices)))
        
        vertinfo = []
        for chunk in chunks(vmesh.vertices, 18):
            position = tuple(chunk[0:3])
            #print('position = {}'.format(position))
            normal = tuple(chunk[3:6])
            #print('normal = {}'.format(normal))
            blend_indices = chunk[7]
            #print('blend indices = {}'.format(blend_indices))
            uv1 = tuple(chunk[7:9])
            #print('uv1 = {}'.format(uv1))
            uv2 = tuple(chunk[9:11])
            #print('uv2 = {}'.format(uv2))
            uv3 = tuple(chunk[11:13])
            #print('uv3 = {}'.format(uv3))
            uv4 = tuple(chunk[13:15])
            #print('uv4 = {}'.format(uv4))
            tangent = tuple(chunk[15:18])
            #print('tangent = {}'.format(tangent))
            vert = {
                'position' : position,
                'normal' : normal,
                'blend_indices' : blend_indices,
                'uv1' : uv1,
                'uv2' : uv2,
                'uv3' : uv3,
                'uv4' : uv4,
                'tangent' : tangent
                }
            vertinfo.append(vert)

        vertinfo2 = []
        for chunk in chunks(vmesh2.vertices, 18):
            position = tuple(chunk[0:3])
            #print('position = {}'.format(position))
            normal = tuple(chunk[3:6])
            #print('normal = {}'.format(normal))
            blend_indices = chunk[7]
            #print('blend indices = {}'.format(blend_indices))
            uv1 = tuple(chunk[7:9])
            #print('uv1 = {}'.format(uv1))
            uv2 = tuple(chunk[9:11])
            #print('uv2 = {}'.format(uv2))
            uv3 = tuple(chunk[11:13])
            #print('uv3 = {}'.format(uv3))
            uv4 = tuple(chunk[13:15])
            #print('uv4 = {}'.format(uv4))
            tangent = tuple(chunk[15:18])
            #print('tangent = {}'.format(tangent))
            vert = {
                'position' : position,
                'normal' : normal,
                'blend_indices' : blend_indices,
                'uv1' : uv1,
                'uv2' : uv2,
                'uv3' : uv3,
                'uv4' : uv4,
                'tangent' : tangent
                }
            vertinfo2.append(vert)
        for index, vert in enumerate(vertinfo):
            print('position1 = {}, position2 = {}'.format(vert['position'], vertinfo2[index]['position']))
            print('normal1 = {}, normal2 = {}'.format(vert['normal'], vertinfo2[index]['normal']))
            print('blend_indices1 = {}, blend_indices2 = {}'.format(vert['blend_indices'], vertinfo2[index]['blend_indices']))
            print('uv1_1 = {}, uv1_2 = {}'.format(vert['uv1'], vertinfo2[index]['uv1']))
            print('uv2_1 = {}, uv2_2 = {}'.format(vert['uv2'], vertinfo2[index]['uv2']))
            print('uv3_1 = {}, uv3_2 = {}'.format(vert['uv3'], vertinfo2[index]['uv3']))
            print('uv4_1 = {}, uv4_2 = {}'.format(vert['uv4'], vertinfo2[index]['uv4']))
            print('tangent1 = {}, tangent2 = {}'.format(vert['tangent'], vertinfo2[index]['tangent']))

        raise
        
    def test_meshes_diff_moved_box(self):
        vmesh_std = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh_std_2 = mesher.LoadBF2Mesh(self.path_object_std_2)

        # this stuff seems to be same for my boxes
        self.assertTrue(vmesh_std.head == vmesh_std_2.head)
        self.assertTrue(vmesh_std.u1 == vmesh_std_2.u1)
        self.assertTrue(vmesh_std.geomnum == vmesh_std_2.geomnum)
        self.assertTrue(len(vmesh_std.geoms) == len(vmesh_std_2.geoms) == 1)
        self.assertTrue(vmesh_std.geoms[0].lodnum == vmesh_std_2.geoms[0].lodnum)
        self.assertTrue(len(vmesh_std.geoms[0].lod) == len(vmesh_std_2.geoms[0].lod) == 1)

        # in 3dsmax it's a (-5, -5, 0) which is (-5, 0, -5)*0.1 as bf2 y and z swapped and divided by 10
        self.assertTrue(vmesh_std.geoms[0].lod[0].min== (-0.5, 0.0, -0.5))
        # std_2 box is moved to right by 10 so it's min starting from +5
        self.assertTrue(vmesh_std_2.geoms[0].lod[0].min == (0.5, 0.0, -0.5))

        # std_2 boxe have right side further than std box
        self.assertTrue(vmesh_std.geoms[0].lod[0].max == (0.5, 1.0, 0.5))
        self.assertTrue(vmesh_std_2.geoms[0].lod[0].max == (1.5, 1.0, 0.5))

        # NOT ACTUAL GEOMETRY???? i expected this to be diffirent
        self.assertTrue(vmesh_std.geoms[0].lod[0].nodenum == vmesh_std_2.geoms[0].lod[0].nodenum)
        self.assertTrue(vmesh_std.geoms[0].lod[0].node == vmesh_std_2.geoms[0].lod[0].node)
        
        # that's same for single boxes
        self.assertTrue(vmesh_std.geoms[0].lod[0].polycount == vmesh_std_2.geoms[0].lod[0].polycount == 12)

        # ###### ACTUAL GEOM ######
        self.assertTrue(vmesh_std.vertattribnum == vmesh_std_2.vertattribnum)
        self.assertTrue(vmesh_std.vertattrib == vmesh_std_2.vertattrib)
        self.assertTrue(vmesh_std.vertformat == vmesh_std_2.vertformat)
        self.assertTrue(vmesh_std.vertstride == vmesh_std_2.vertstride)

        # that's same for single boxes, diffirent for merged one
        # what are those vertices?
        self.assertTrue(vmesh_std.vertnum == vmesh_std_2.vertnum == 25)

        # seems like a real geom data
        # 72 / 4 * 25
        # _vertices_num = int(self.vertstride / self.vertformat * self.vertnum)
        # vertstride appears to be a struct of 
        '''
        for index, vertice in enumerate(vmesh_std.vertices):
            if vertice == vmesh_std_2.vertices[index]:
                #print('v[{}] {}'.format(index, vertice))
                continue
            print('v1[{}] {} == v2[{}] {}'.format(index, vertice, index, vmesh_std_2.vertices[index],))
        print('len(vmesh_std.vertices) = {}'.format(len(vmesh_std.vertices)))
        print('len(vmesh_std_2.vertices) = {}'.format(len(vmesh_std_2.vertices)))
        self.assertTrue(vmesh_std.vertices == vmesh_std_2.vertices)
        '''
        # ###### ACTUAL GEOM ######
        
        #for index, id in enumerate(vmesh_std.index):
        #    print('index[{}] {}'.format(index, id))
        self.assertTrue(vmesh_std.indexnum == vmesh_std_2.indexnum)
        self.assertTrue(vmesh_std.index == vmesh_std_2.index)
        self.assertTrue(vmesh_std.u2 == vmesh_std_2.u2)
        self.assertTrue(vmesh_std.geoms[0].lod[0].matnum == vmesh_std_2.geoms[0].lod[0].matnum == 1)
        self.assertTrue(vmesh_std.geoms[0].lod[0].mat[0].alphamode == vmesh_std_2.geoms[0].lod[0].mat[0].alphamode)
        self.assertTrue(vmesh_std.geoms[0].lod[0].mat[0].fxfile == vmesh_std_2.geoms[0].lod[0].mat[0].fxfile)
        self.assertTrue(vmesh_std.geoms[0].lod[0].mat[0].technique == vmesh_std_2.geoms[0].lod[0].mat[0].technique)
        self.assertTrue(vmesh_std.geoms[0].lod[0].mat[0].mapnum == vmesh_std_2.geoms[0].lod[0].mat[0].mapnum)
        self.assertTrue(vmesh_std.geoms[0].lod[0].mat[0].map[0] == vmesh_std_2.geoms[0].lod[0].mat[0].map[0])
        self.assertTrue(vmesh_std.geoms[0].lod[0].mat[0].map[1] == vmesh_std_2.geoms[0].lod[0].mat[0].map[1])
        self.assertTrue(vmesh_std.geoms[0].lod[0].mat[0].vstart == vmesh_std_2.geoms[0].lod[0].mat[0].vstart)
        self.assertTrue(vmesh_std.geoms[0].lod[0].mat[0].istart == vmesh_std_2.geoms[0].lod[0].mat[0].istart)
        self.assertTrue(vmesh_std.geoms[0].lod[0].mat[0].inum == vmesh_std_2.geoms[0].lod[0].mat[0].inum)
        self.assertTrue(vmesh_std.geoms[0].lod[0].mat[0].vnum == vmesh_std_2.geoms[0].lod[0].mat[0].vnum)
        
        # some stuff from BFP4F
        #print('vmesh_std.geoms[0].lod[0].mat[0].u4 = {}'.format(vmesh_std.geoms[0].lod[0].mat[0].u4))
        #print('vmesh_std_2.geoms[0].lod[0].mat[0].u4 = {}'.format(vmesh_std_2.geoms[0].lod[0].mat[0].u4))
        self.assertTrue(vmesh_std.geoms[0].lod[0].mat[0].u4 != vmesh_std_2.geoms[0].lod[0].mat[0].u4)
        self.assertTrue(vmesh_std.geoms[0].lod[0].mat[0].u5 != vmesh_std_2.geoms[0].lod[0].mat[0].u5)
        
        # boundaries
        #print('vmesh_std.geoms[0].lod[0].mat[0].nmin = {}'.format(vmesh_std.geoms[0].lod[0].mat[0].nmin))
        #print('vmesh_std_2.geoms[0].lod[0].mat[0].nmin = {}'.format(vmesh_std_2.geoms[0].lod[0].mat[0].nmin))
        self.assertTrue(vmesh_std.geoms[0].lod[0].mat[0].nmin != vmesh_std_2.geoms[0].lod[0].mat[0].nmin)
        self.assertTrue(vmesh_std.geoms[0].lod[0].mat[0].nmax != vmesh_std_2.geoms[0].lod[0].mat[0].nmax)
        #raise




