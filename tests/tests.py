import unittest
import unittest.mock as mock
import tempfile
import os

import bf2
import mesher


class TestModRoot(unittest.TestCase):
    
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


class TestModSearch(unittest.TestCase):

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
        test_object_path_relative = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box1', 'meshes', 'evil_box1.staticmesh'])
        self.test_object_path = os.path.join(bf2.Mod().root, test_object_path_relative)

    def test_can_store_path(self):
        self.assertTrue(mesher.StdMeshFile(self.test_object_path))
    
    def test_can_read_header(self):
        stdmesh = mesher.StdMeshFile(self.test_object_path)
        stdmesh.read_header()
        self.assertTrue(stdmesh.struct.header.version in [0, 9, 10])
        self.assertTrue(stdmesh.struct.header.u2 in [11])
        
