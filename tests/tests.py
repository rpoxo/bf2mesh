import unittest
import unittest.mock as mock
import tempfile
import os

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

class TestStdMesh(unittest.TestCase):

    def setUp(self):
        # NOTE: THIS IS VERY SPECIFIC TESTS FOR TEST MODEL READ
        test_object_std = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box1', 'meshes', 'evil_box1.staticmesh'])
        test_object_alt_uvw = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box2', 'meshes', 'evil_box2.staticmesh'])
        test_object_two_lods = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box3', 'meshes', 'evil_box3.staticmesh'])
        test_object_dest = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box4', 'meshes', 'evil_box4.staticmesh'])

        self.path_object_std = os.path.join(bf2.Mod().root, test_object_std)
        self.path_object_alt_uvw = os.path.join(bf2.Mod().root, test_object_alt_uvw)
        self.path_object_two_lods = os.path.join(bf2.Mod().root, test_object_two_lods)
        self.path_object_dest = os.path.join(bf2.Mod().root, test_object_dest)

    def test_can_store_path(self):
        self.assertTrue(mesher.StdMeshFile(self.path_object_std))
    
    def test_can_read_header(self):
        mesh = mesher.StdMeshFile(self.path_object_std)
        mesh.read_header()
        self.assertTrue(mesh.struct.header.u1 is 0)
        self.assertTrue(mesh.struct.header.version in [10, 6, 11])
        self.assertTrue(mesh.struct.header.u3 is 0)
        self.assertTrue(mesh.struct.header.u4 is 0)
        self.assertTrue(mesh.struct.header.u5 is 0)
    
    def test_can_read_unknown_byte(self):
        mesh = mesher.StdMeshFile(self.path_object_std)
        mesh.read_unknown2()
        self.assertTrue(mesh.struct.unknown2.u1 is 0)
    
    def test_can_read_bf2geom_num(self):
        mesh = mesher.StdMeshFile(self.path_object_std)
        mesh.read_bf2geom_num()
        self.assertTrue(mesh.struct.bf2geom.num is 1)

        mesh = mesher.StdMeshFile(self.path_object_dest)
        mesh.read_bf2geom_num()
        self.assertTrue(mesh.struct.bf2geom.num is 2)

    def test_can_read_bf2geom_table(self):
        mesh = mesher.StdMeshFile(self.path_object_std)
        mesh.read_bf2geom_lodnum()
        self.assertTrue(mesh.struct.bf2geom.lodnum is 1)
        
        mesh = mesher.StdMeshFile(self.path_object_two_lods)
        mesh.read_bf2geom_lodnum()
        self.assertTrue(mesh.struct.bf2geom.lodnum is 2)
        
        mesh = mesher.StdMeshFile(self.path_object_dest)
        mesh.read_bf2geom_lodnum()
        self.assertTrue(mesh.struct.bf2geom.lodnum is 2)

    def test_can_read_vertattrib_num(self):
        mesh = mesher.StdMeshFile(self.path_object_std)
        mesh.read_vertattrib_num()
        self.assertTrue(mesh.struct.vertattrib.num is 9)

    def test_can_read_vertattrib_num_CUSTOM_PR_DEST(self):
        try:
            test_object_custom = os.path.join(*['objects', 'staticobjects', 'pr', 'destroyable_objects', 'doors', 'wooddoor1m_03', 'meshes', 'wooddoor1m_03.staticmesh'])
            self.path_object_custom = os.path.join(bf2.Mod().root, test_object_custom)
            mesh = mesher.StdMeshFile(self.path_object_custom)
            mesh.read_vertattrib_num()
            print(mesh.struct.vertattrib.num)
            self.assertTrue(mesh.struct.vertattrib.num is 10)
        except FileNotFoundError:
            self.skipTest('cannot find PR "wooddoor1m_03" mesh')
            
    def test_can_read_vertex_attributes(self):
        mesh = mesher.StdMeshFile(self.path_object_std)
        mesh.read_vertattributes()
        self.assertTrue(mesh.struct.vertattrib.table[0] == (0, 0, 2, 0))
        self.assertTrue(mesh.struct.vertattrib.table[1] == (0, 12, 2, 3))
        self.assertTrue(mesh.struct.vertattrib.table[2] == (0, 24, 4, 2))
        self.assertTrue(mesh.struct.vertattrib.table[3] == (0, 28, 1, 5))
        self.assertTrue(mesh.struct.vertattrib.table[4] == (0, 36, 1, 261))
        self.assertTrue(mesh.struct.vertattrib.table[5] == (0, 44, 1, 517))
        self.assertTrue(mesh.struct.vertattrib.table[6] == (0, 52, 1, 773))
        self.assertTrue(mesh.struct.vertattrib.table[7] == (0, 60, 2, 6))
        self.assertTrue(mesh.struct.vertattrib.table[8] == (255, 0, 17, 0))

    def test_can_read_vertformat(self):
        mesh = mesher.StdMeshFile(self.path_object_std)
        mesh.read_vertformat()
        self.assertTrue(mesh.struct.vertices.vertformat == 4)

    def test_can_read_vertstride(self):
        mesh = mesher.StdMeshFile(self.path_object_std)
        mesh.read_vertstride()
        self.assertTrue(mesh.struct.vertices.vertstride == 72)
    
    def test_can_read_vertnum(self):
        mesh = mesher.StdMeshFile(self.path_object_std)
        mesh.read_vertnum()
        self.assertTrue(mesh.struct.vertices.vertnum == 25)

    def test_can_read_vertex_block(self):
        mesh = mesher.StdMeshFile(self.path_object_std)
        mesh.read_vertex_block()
        self.assertTrue(len(mesh.struct.vertices.table) == 450)








