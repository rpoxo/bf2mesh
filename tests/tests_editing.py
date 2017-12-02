import unittest
import os
import sys
import copy
import shutil

import modmesh

import tests.mock_mesh as mocks

class TestVisMeshSingleLod(unittest.TestCase):

    def setUp(self):
        # NOTE: THIS IS VERY SPECIFIC TESTS AGAINST PREPARED OBJECT
        self.path_object_std = os.path.join(*['tests', 'samples', 'evil_box', 'meshes', 'evil_box.staticmesh'])

    @classmethod
    def tearDownClass(cls):
        try:
            path_clear = os.path.join(*['tests', 'generated', 'edit'])
            shutil.rmtree(path_clear)
        except FileNotFoundError:
            print('Nothing to clean up')

    def test_can_rename_texture(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        path_object_clone = os.path.join(*['tests', 'generated', 'edit', 'evil_box_rename_texture', 'meshes', 'evil_box_rename_texture.staticmesh'])
        
        geom = 0
        lod = 0
        material = 0
        map = 0

        # ensure we have diffirent texture before test
        self.assertTrue(vmesh.
                        geoms[geom].
                        lods[lod].
                        materials[material].
                        maps[map] == b'objects/staticobjects/test/evil_box/textures/evil_box_c.dds')

        vmesh.rename_texture(geom,
                            lod,
                            material,
                            map,
                            'readme/assets/apps/python3/mesher/tests/samples/evil_box/textures/evil_box_c.dds')

        # save results for manual check
        vmesh.save(path_object_clone)
        self.assertTrue(vmesh.
                        geoms[geom].
                        lods[lod].
                        materials[material].
                        maps[map] == b'readme/assets/apps/python3/mesher/tests/samples/evil_box/textures/evil_box_c.dds')
                        
                        
    def test_can_get_vertex_data_position(self):
        vmesh = mocks.Box().vmesh
        
        position = vmesh.get_vertex_data(0, 'POSITION')
        self.assertTrue(position == (0.5, 1.0, -0.5))

    def test_can_edit_vertex_data_position(self):
        vmesh = mocks.Box().vmesh
        path_object_clone = os.path.join(*['tests', 'generated', 'edit', 'evil_box_vertex_position', 'meshes', 'evil_box_vertex_position.staticmesh'])
        
        position = (0.5, 2.0, -0.5)
        vmesh.edit_vertex(0, 'POSITION', position)
        # save results for check
        vmesh.save(path_object_clone)
        self.assertTrue(vmesh.get_vertex_data(0, 'POSITION') == position)

    def test_can_offset_mesh(self):
        vmesh = mocks.Box().vmesh
        # a copy for later comparison
        vmesh_original = mocks.Box().vmesh
        path_object_clone = os.path.join(*['tests', 'generated', 'edit', 'evil_box_offset_mesh', 'meshes', 'evil_box_offset_mesh.staticmesh'])
        
        offset = (1.0, 0.0, 0.0)
        vmesh.offset_mesh(offset)
        # save results for check
        vmesh.save(path_object_clone)
        
        for vertid in range(vmesh_original.vertnum):
            position_old = vmesh_original.get_vertex_data(vertid, 'POSITION')
            position_new = vmesh.get_vertex_data(vertid, 'POSITION')
            
            self.assertTrue(position_new == tuple(sum(i) for i in zip(position_old, offset)))

    def test_can_merge_geometry_with_offset(self):
        vmesh = mocks.Box().vmesh
        vmesh2 = mocks.Box().vmesh
        offset = (1.0, 0.0, 0.0)
        vmesh2.offset_mesh(offset)
        vmesh_old = copy.deepcopy(vmesh)
        path_object_clone = os.path.join(*['tests', 'generated', 'edit', 'evil_box_merge_geometry', 'meshes', 'evil_box_merge_geometry.staticmesh'])
        
        vmesh.merge_geometry(vmesh2)
        # save results for check
        vmesh.save(path_object_clone)
        
        self.assertTrue(vmesh.vertnum == vmesh_old.vertnum + vmesh2.vertnum)
        self.assertTrue(vmesh.indexnum == vmesh_old.indexnum + vmesh2.indexnum)
        self.assertTrue(len(vmesh.index) == len(vmesh_old.index) + len(vmesh2.index))
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].vnum == vmesh_old.geoms[0].lods[0].materials[0].vnum + vmesh2.geoms[0].lods[0].materials[0].vnum)
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].inum == vmesh_old.geoms[0].lods[0].materials[0].inum + vmesh2.geoms[0].lods[0].materials[0].inum)
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].nmin == tuple(sum(i) for i in zip(vmesh_old.geoms[0].lods[0].materials[0].nmin, vmesh2.geoms[0].lods[0].materials[0].nmin)))
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].nmax == tuple(sum(i) for i in zip(vmesh_old.geoms[0].lods[0].materials[0].nmax, vmesh2.geoms[0].lods[0].materials[0].nmax)))
        
        for vertid in range(vmesh.vertnum):
            if vertid < vmesh_old.vertnum:
                #print('vmesh.get_vertex_data({}, "POSITION") = {}'.format(vertid, vmesh.get_vertex_data(vertid, 'POSITION')))
                #print('vmesh_old.get_vertex_data({}, "POSITION") = {}'.format(vertid, vmesh_old.get_vertex_data(vertid, 'POSITION')))
                self.assertTrue(vmesh.get_vertex_data(vertid, 'POSITION') == vmesh_old.get_vertex_data(vertid, 'POSITION'))
            else:
                position_old = vmesh_old.get_vertex_data(vertid - vmesh_old.vertnum, 'POSITION')
                #print('[{}]position_old + offset = {}'.format(vertid, tuple(sum(i) for i in zip(position_old, offset))))
                #print('[{}]vmesh.get_vertex_data({}, "POSITION") = {}'.format(vertid, vertid, vmesh.get_vertex_data(vertid, 'POSITION')))
                self.assertTrue(vmesh.get_vertex_data(vertid, 'POSITION') == tuple(sum(i) for i in zip(position_old, offset)))
        
        for idxid in range(vmesh.indexnum):
            if idxid < vmesh_old.indexnum:
                self.assertTrue(vmesh.index[idxid] == vmesh_old.index[idxid])
            else:
                print('vmesh.index[0] = {}'.format(vmesh.index[0]))
                print('vmesh.index[{}] = {}'.format(idxid, vmesh.index[idxid]))
                print('vmesh2.index[{}-->{}] = {}'.format(idxid, idxid-vmesh2.indexnum, vmesh2.index[idxid-vmesh2.indexnum]))
                #print('vmesh2.index[{}-{}] + vmesh_old.indexnum({}) = {}'.format(vmesh2.index[idxid-vmesh2.indexnum] + vmesh_old.indexnum))
                self.assertTrue(vmesh.index[idxid] == vmesh2.index[idxid-vmesh2.indexnum] + vmesh_old.vertnum)












        