import unittest
import os
import sys
import copy
import shutil

import modmesh

import tests.mock_mesh as mocks

class TestVisMeshSingleLod(unittest.TestCase):

    def setUp(self):
        self.path_object_std = os.path.join(*['tests', 'samples', 'evil_box', 'meshes', 'evil_box.staticmesh'])

    @classmethod
    def tearDownClass(cls):
        try:
            path_clear = os.path.join(*['tests', 'generated', 'edit'])
            # not cleaning for testing
            #shutil.rmtree(path_clear)
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

class TestVisMesh_SkinnedMesh(unittest.TestCase):

    def setUp(self):
        self.path_object_skinned = os.path.join(*['tests', 'samples', 'kits', 'mec', 'Meshes', 'mec_kits.skinnedMesh'])

    def test_can_copy_geom(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_skinned)
        vmesh_old = modmesh.LoadBF2Mesh(self.path_object_skinned)
        if not vmesh.isSkinnedMesh:
            raise
        path_object_skinned_clone = os.path.join(*['tests', 'generated', 'edit', 'kits', 'mec_geom_copy', 'Meshes', 'mec_kits_geom_copy.skinnedMesh'])

        # example geom
        geomToCopy = 0
        geomCopyTo = 1

        # debugging
        #geom = 0
        #lod = 0
        #mat = 0
        #print('vnum = {}'.format(vmesh.geoms[geom].lods[lod].materials[mat].vnum))
        #print('vstart = {}'.format(vmesh.geoms[geom].lods[lod].materials[mat].vstart))
        #print('inum = {}'.format(vmesh.geoms[geom].lods[lod].materials[mat].inum))
        #print('istart = {}'.format(vmesh.geoms[geom].lods[lod].materials[mat].istart))
        
        modmesh.VisMeshTransform(vmesh).copy_geom_id(geomToCopy, geomCopyTo)
        vmesh.save(path_object_skinned_clone)

        self.assertTrue(vmesh.geomnum == vmesh_old.geomnum + 1)
        self.assertTrue(len(vmesh.geoms) == len(vmesh_old.geoms) + 1)
        self.assertTrue(vmesh.geoms[geomCopyTo].lodnum == vmesh_old.geoms[geomToCopy].lodnum)
        for id_lod, lod in enumerate(vmesh.geoms[geomCopyTo].lods):
            self.assertTrue(lod.rignum == vmesh_old.geoms[geomToCopy].lods[id_lod].rignum)
            for id_rig, rig in enumerate(lod.rigs):
                self.assertTrue(rig.bonenum == vmesh_old.geoms[geomToCopy].lods[id_lod].rigs[id_rig].bonenum)
                for id_bone, bone in enumerate(rig.bones):
                    self.assertTrue(bone.id == vmesh_old.geoms[geomToCopy].lods[id_lod].rigs[id_rig].bones[id_bone].id)
                    self.assertTrue(bone.matrix == vmesh_old.geoms[geomToCopy].lods[id_lod].rigs[id_rig].bones[id_bone].matrix)
            for id_mat, material in enumerate(lod.materials):
                self.assertTrue(material.vnum == vmesh_old.geoms[geomToCopy].lods[id_lod].materials[id_mat].vnum)
                self.assertTrue(material.vstart == vmesh_old.geoms[geomToCopy].lods[id_lod].materials[id_mat].vstart)
                self.assertTrue(material.inum == vmesh_old.geoms[geomToCopy].lods[id_lod].materials[id_mat].inum)
                self.assertTrue(material.istart == vmesh_old.geoms[geomToCopy].lods[id_lod].materials[id_mat].istart)

    def test_can_delete_geom(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_skinned)
        vmesh_old = modmesh.LoadBF2Mesh(self.path_object_skinned)
        if not vmesh.isSkinnedMesh:
            raise
        path_object_skinned_clone = os.path.join(*['tests', 'generated', 'edit', 'kits', 'mec_geom_delete', 'Meshes', 'mec_kits_geom_delete.skinnedMesh'])

        # example geom
        geomToDelete = 18

        modmesh.VisMeshTransform(vmesh).delete_geom_id(geomToDelete)
        vmesh.save(path_object_skinned_clone)

        self.assertTrue(vmesh.geomnum == vmesh_old.geomnum - 1)
        self.assertTrue(len(vmesh.geoms) == len(vmesh_old.geoms) - 1)
        
        # not last geom, so have to compare geomToDelete in new and geomToDelete+1 in old mesh
        if vmesh_old.geomnum > geomToDelete:
            self.assertTrue(vmesh.geoms[geomToDelete].lodnum == vmesh_old.geoms[geomToDelete+1].lodnum)
            for id_lod, lod in enumerate(vmesh.geoms[geomToDelete].lods):
                self.assertTrue(lod.rignum == vmesh_old.geoms[geomToDelete+1].lods[id_lod].rignum)
                for id_rig, rig in enumerate(lod.rigs):
                    self.assertTrue(rig.bonenum == vmesh_old.geoms[geomToDelete+1].lods[id_lod].rigs[id_rig].bonenum)
                    for id_bone, bone in enumerate(rig.bones):
                        self.assertTrue(bone.id == vmesh_old.geoms[geomToDelete+1].lods[id_lod].rigs[id_rig].bones[id_bone].id)
                        self.assertTrue(bone.matrix == vmesh_old.geoms[geomToDelete+1].lods[id_lod].rigs[id_rig].bones[id_bone].matrix)
                for id_mat, material in enumerate(lod.materials):
                    self.assertTrue(material.vnum == vmesh_old.geoms[geomToDelete+1].lods[id_lod].materials[id_mat].vnum)
                    self.assertTrue(material.vstart == vmesh_old.geoms[geomToDelete+1].lods[id_lod].materials[id_mat].vstart)
                    self.assertTrue(material.inum == vmesh_old.geoms[geomToDelete+1].lods[id_lod].materials[id_mat].inum)
                    self.assertTrue(material.istart == vmesh_old.geoms[geomToDelete+1].lods[id_lod].materials[id_mat].istart)
    
    def test_can_edit_geoms_order(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_skinned)
        vmesh_old = modmesh.LoadBF2Mesh(self.path_object_skinned)
        if not vmesh.isSkinnedMesh:
            raise
        path_object_skinned_clone = os.path.join(*['tests', 'generated', 'edit', 'kits', 'mec_geoms_ordered', 'Meshes', 'mec_kits_geoms_ordered.skinnedMesh'])

        # new geomes
        newGeomsList = tuple([i for i in range(vmesh.geomnum-1, -1, -1)]) # revert geoms order

        modmesh.VisMeshTransform(vmesh).edit_geoms_order(newGeomsList)
        vmesh.save(path_object_skinned_clone)

        self.assertTrue(vmesh.geomnum == vmesh_old.geomnum)
        self.assertTrue(len(vmesh.geoms) == len(vmesh_old.geoms))
        
        for id_geom, geom in enumerate(vmesh.geoms):
            id_geom_old = vmesh_old.geomnum - 1 - id_geom
            self.assertTrue(geom.lodnum == vmesh_old.geoms[id_geom_old].lodnum)
            for id_lod, lod in enumerate(geom.lods):
                self.assertTrue(lod.rignum == vmesh_old.geoms[id_geom_old].lods[id_lod].rignum)
                for id_rig, rig in enumerate(lod.rigs):
                    self.assertTrue(rig.bonenum == vmesh_old.geoms[id_geom_old].lods[id_lod].rigs[id_rig].bonenum)
                    for id_bone, bone in enumerate(rig.bones):
                        self.assertTrue(bone.id == vmesh_old.geoms[id_geom_old].lods[id_lod].rigs[id_rig].bones[id_bone].id)
                        self.assertTrue(bone.matrix == vmesh_old.geoms[id_geom_old].lods[id_lod].rigs[id_rig].bones[id_bone].matrix)
                for id_mat, material in enumerate(lod.materials):
                    self.assertTrue(material.vnum == vmesh_old.geoms[id_geom_old].lods[id_lod].materials[id_mat].vnum)
                    self.assertTrue(material.vstart == vmesh_old.geoms[id_geom_old].lods[id_lod].materials[id_mat].vstart)
                    self.assertTrue(material.inum == vmesh_old.geoms[id_geom_old].lods[id_lod].materials[id_mat].inum)
                    self.assertTrue(material.istart == vmesh_old.geoms[id_geom_old].lods[id_lod].materials[id_mat].istart)





        