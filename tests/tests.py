import unittest
import unittest.mock as mock
import tempfile
import os
import sys

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
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(vmesh.head.u1 is 0)
        self.assertTrue(vmesh.head.version in [10, 6, 11])
        self.assertTrue(vmesh.head.u3 is 0)
        self.assertTrue(vmesh.head.u4 is 0)
        self.assertTrue(vmesh.head.u5 is 0)
    
    def test_can_read_u1(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(vmesh.head.u1 is 0)

    def test_can_read_geomnum(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        print(vmesh.geomnum)
        self.assertTrue(vmesh.geomnum is 1)

        vmesh = mesher.LoadBF2Mesh(self.path_object_dest)
        self.assertTrue(vmesh.geomnum is 2)

    def test_can_read_geom_table(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(vmesh.geom[0].lodnum is 1)

        vmesh = mesher.LoadBF2Mesh(self.path_object_two_lods)
        self.assertTrue(vmesh.geom[0].lodnum is 2)

        vmesh = mesher.LoadBF2Mesh(self.path_object_dest)
        self.assertTrue(len(vmesh.geom) is 2)
        self.assertTrue(vmesh.geom[0].lodnum is 2)
        self.assertTrue(vmesh.geom[1].lodnum is 2)

    def test_can_read_vertattribnum_CUSTOM_PR_DEST(self):
        try:
            test_object_custom = os.path.join(*['objects', 'staticobjects', 'pr', 'destroyable_objects', 'doors', 'wooddoor1m_03', 'meshes', 'wooddoor1m_03.staticmesh'])
            self.path_object_custom = os.path.join(bf2.Mod().root, test_object_custom)
            vmesh = mesher.LoadBF2Mesh(self.path_object_custom)
            self.assertTrue(vmesh.vertattribnum is 10)
        except FileNotFoundError:
            self.skipTest('cannot find PR "wooddoor1m_03" mesh')

    def test_can_read_vertex_attribute_table(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(vmesh.vertattrib[0] == (0, 0, 2, 0))
        self.assertTrue(vmesh.vertattrib[1] == (0, 12, 2, 3))
        self.assertTrue(vmesh.vertattrib[2] == (0, 24, 4, 2))
        self.assertTrue(vmesh.vertattrib[3] == (0, 28, 1, 5))
        self.assertTrue(vmesh.vertattrib[4] == (0, 36, 1, 261))
        self.assertTrue(vmesh.vertattrib[5] == (0, 44, 1, 517))
        self.assertTrue(vmesh.vertattrib[6] == (0, 52, 1, 773))
        self.assertTrue(vmesh.vertattrib[7] == (0, 60, 2, 6))
        self.assertTrue(vmesh.vertattrib[8] == (255, 0, 17, 0))

    def test_can_read_vertformat(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(vmesh.vertformat == 4)

    def test_can_read_vertstride(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(vmesh.vertstride == 72)

    def test_can_read_vertnum(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(vmesh.vertnum == 25)

    def test_can_read_vertex_block(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(len(vmesh.vertices) == 450)

    def test_can_read_indexnum(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(vmesh.indexnum is 36)

    def test_can_read_index_block(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(len(vmesh.index) == 36)

    def test_can_read_u2(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(vmesh.u2 is 8)

    def test_can_read_nodes_bounds(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(vmesh.geom[0].lod[0].min == (-0.5, 0, -0.5))
        self.assertTrue(vmesh.geom[0].lod[0].max == (0.5, 1.0, 0.5))
        #self.assertTrue(vmesh.geom[0].lod[0].pivot == (0.5, 1.0, 0.5)) # some old bundleds?

    def test_can_read_nodes_nodenum(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(vmesh.geom[0].lod[0].nodenum == 1)

    @unittest.skip('no idea how to verify, lenght seems to be correct')
    def test_can_read_nodes_matrices(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_dest)
        #for geomnum in range(vmesh.geomnum):
        #    for lodnum in range(vmesh.geom[geomnum].lodnum):
        #        print(vmesh.geom[geomnum].lod[lodnum].node)
        #raise

    def test_can_read_geom_lod(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(vmesh.geom[0].lod[0].matnum == 1)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].alphamode == 0)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].fxfile == b'StaticMesh.fx')
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].technique == b'Base')
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].mapnum == 2)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].map[0] == b'objects/staticobjects/test/evil_box1/textures/evil_box1_c.dds')
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].map[1] == b'Common\Textures\SpecularLUT_pow36.dds')
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].vstart == 0)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].istart == 0)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].inum == 36)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].vnum == 25)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].u4 == 8064)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].u5 == 65535)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].nmin == (-0.5, 0.0, -0.5))
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].nmax == (0.5, 1.0, 0.5))
        self.assertTrue(vmesh.geom[0].lod[0].polycount == 12)
    
    def test_can_read_merged_mesh(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_merged)

    def test_meshes_diff(self):
        vmesh = mesher.LoadBF2Mesh(self.path_object_std)
        vmesh2 = mesher.LoadBF2Mesh(self.path_object_merged)

        self.assertTrue(vmesh.head == vmesh2.head)
        self.assertTrue(vmesh.u1 == vmesh2.u1)
        self.assertTrue(vmesh.geomnum == vmesh2.geomnum)
        self.assertTrue(len(vmesh.geom) == len(vmesh2.geom) == 1)
        self.assertTrue(vmesh.geom[0].lodnum == vmesh2.geom[0].lodnum)
        self.assertTrue(len(vmesh.geom[0].lod) == len(vmesh2.geom[0].lod) == 1)
        self.assertTrue(vmesh.geom[0].lod[0].min == vmesh2.geom[0].lod[0].min)
        self.assertTrue(vmesh.geom[0].lod[0].max != vmesh2.geom[0].lod[0].max) # diff
        self.assertTrue(vmesh2.geom[0].lod[0].max == (1.5, 1.0, 0.5))
        self.assertTrue(vmesh.geom[0].lod[0].nodenum == vmesh2.geom[0].lod[0].nodenum)
        self.assertTrue(vmesh.geom[0].lod[0].node == vmesh2.geom[0].lod[0].node) # not geometry?
        self.assertTrue(vmesh.geom[0].lod[0].polycount != vmesh2.geom[0].lod[0].polycount != 0) # diff
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
        self.assertTrue(vmesh.geom[0].lod[0].matnum == vmesh2.geom[0].lod[0].matnum == 1)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].alphamode == vmesh2.geom[0].lod[0].mat[0].alphamode)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].fxfile == vmesh2.geom[0].lod[0].mat[0].fxfile)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].technique == vmesh2.geom[0].lod[0].mat[0].technique)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].mapnum == vmesh2.geom[0].lod[0].mat[0].mapnum)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].map[0] == vmesh2.geom[0].lod[0].mat[0].map[0])
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].map[1] == vmesh2.geom[0].lod[0].mat[0].map[1])
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].vstart == vmesh2.geom[0].lod[0].mat[0].vstart)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].istart == vmesh2.geom[0].lod[0].mat[0].istart)
        print('vmesh inum = {}'.format(vmesh.geom[0].lod[0].mat[0].inum))
        print('vmesh2 inum = {}'.format(vmesh2.geom[0].lod[0].mat[0].inum))
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].inum != vmesh2.geom[0].lod[0].mat[0].inum) # diff
        print('vmesh vnum = {}'.format(vmesh.geom[0].lod[0].mat[0].vnum))
        print('vmesh2 vnum = {}'.format(vmesh2.geom[0].lod[0].mat[0].vnum))
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].vnum != vmesh2.geom[0].lod[0].mat[0].vnum) # diff
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].u4 == vmesh2.geom[0].lod[0].mat[0].u4)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].u5 == vmesh2.geom[0].lod[0].mat[0].u5)
        #print('vmesh nmax = {}'.format(vmesh.geom[0].lod[0].mat[0].nmax))
        #print('vmesh2 nmax = {}'.format(vmesh2.geom[0].lod[0].mat[0].nmax))
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].nmin == vmesh2.geom[0].lod[0].mat[0].nmin)
        self.assertTrue(vmesh.geom[0].lod[0].mat[0].nmax != vmesh2.geom[0].lod[0].mat[0].nmax) # diff
        #raise

    @unittest.skip('i\o intensive')
    def test_can_read_PR_MESHES_1480(self):
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
        raise
    
    def test_can_read_failed_mesh(self):
        vmesh = mesher.LoadBF2Mesh(os.path.join(bf2.Mod().root, 'objects\staticobjects\Bridges\EoD_Bridge_Big\Meshes\eod_bridge_big.staticmesh'))





