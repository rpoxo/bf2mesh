import unittest
import os
import sys
import copy
import shutil
import math

import modmesh
from modmesh import D3DDECLTYPE
from modmesh import D3DDECLUSAGE
from modmesh import Vec3

import tests.mock_mesh as mocks

class TestVisMeshStatic(unittest.TestCase):

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

    @unittest.skip('TODO: refactor')
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

        modmesh.VisMeshTransform(vmesh).rename_texture(geom,
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

    def test_can_translate_mesh(self):
        vmesh = mocks.Box()
        vmesh_clone = mocks.Box()
        path_object_clone = os.path.join(*['tests', 'generated', 'edit', 'evil_box_translate_mesh', 'meshes', 'evil_box_translate_mesh.staticmesh'])
        
        # using bf2 axis
        # x, y, z = red, green, blue lines in bfmeshview
        offset = (1.0, 0.0, 0.0)
        vmesh.translate(offset)
        
        vertices = [vertex for vertex in vmesh.get_vertices()]
        vertices_old = [vertex for vertex in vmesh_clone.get_vertices()]
        for id_vertex, vertex in enumerate(vertices):
            position = getattr(vertex, D3DDECLUSAGE.POSITION.name)
            position_old = getattr(vertices_old[id_vertex], D3DDECLUSAGE.POSITION.name)
            
            self.assertTrue(position == sum(i) for i in zip(position_old, offset))
        
        # save for manual check
        vmesh.save(path_object_clone)

    def test_can_rotate_mesh(self):
        vmesh = mocks.Box()
        vmesh_clone = mocks.Box()
        path_object_clone = os.path.join(*['tests', 'generated', 'edit', 'evil_box_rotate_mesh', 'meshes', 'evil_box_rotate_mesh.staticmesh'])
        
        rotation = (45.0, 0.0, 0.0)
        vmesh.rotate(rotation)
        vmesh.save(path_object_clone)

    def test_can_rotate_mesh_pavement(self):
        path_pavement = os.path.join(*['tests', 'samples', 'pavement', '24m_1', 'meshes', '24m_1.staticmesh'])
        path_pavement_clone = os.path.join(*['tests', 'generated', 'edit', 'pavement', '24m_1_rotate', 'meshes', '24m_1_rotate.staticmesh'])
        vmesh = modmesh.LoadBF2Mesh(path_pavement)

        rotation = (45.0, 0.0, 0.0)
        vmesh.rotate(rotation)
        vmesh.save(path_pavement_clone)

    def test_can_merge_simple_mesh(self):
        vmesh = mocks.Box()
        vmesh2 = mocks.Box()
        vmesh.isStaticMesh = True
        vmesh2.isStaticMesh = True
        path_object_clone = os.path.join(*['tests', 'generated', 'edit', 'evil_box_merge_mesh', 'meshes', 'evil_box_merge_mesh.staticmesh'])
        
        offset = (1.0, 0.0, 0.0)
        vmesh2.translate(offset)

        vmesh.merge(vmesh2)
        vmesh.save(path_object_clone)

    def test_can_merge_statics_from_GPO(self):
        path_pavement = os.path.join(*['tests', 'samples', 'pavement', '24m_1', 'meshes', '24m_1.staticmesh'])
        path_pavement_clone = os.path.join(*['tests', 'generated', 'edit', 'pavement', '24m_1_merge', 'meshes', '24m_1_merge.staticmesh'])
        
        # from fallujah
        position1 = Vec3(491.567, 24.653, 495.454)
        rotation1 = (0.2, 0.0, 0.0)

        position2 = Vec3(491.416, 24.653, 443.974)
        rotation2 = (0.2, 0.0, 0.0)
        
        diff = position2 - position1
        
        vmesh1 = modmesh.LoadBF2Mesh(path_pavement)
        vmesh2 = modmesh.LoadBF2Mesh(path_pavement)
        
        vmesh1.rotate(rotation1)
        vmesh2.rotate(rotation2)
        vmesh2.translate(diff)
        vmesh1.merge(vmesh2)
        
        # translating to center
        min = Vec3(*vmesh1.geoms[0].lods[0].min)
        max = Vec3(*vmesh1.geoms[0].lods[0].max)
        center_offset = (min + max) / 2
        #print(min)
        #print(max)
        #print(center_offset)
        #print(position1 + center_offset)
        vmesh1.translate(-center_offset)
        
        #vmesh1.geoms[0].lods[0].materials.
        
        vmesh1.save(path_pavement_clone)
        #raise
        
        #vmesh_test = modmesh.LoadBF2Mesh(path_pavement_clone)

        
@unittest.skip('rewriting')
class TestVisMesh_SkinnedMesh(unittest.TestCase):

    def setUp(self):
        self.path_object_skinned = os.path.join(*['tests', 'samples', 'kits', 'mec', 'Meshes', 'mec_kits.skinnedMesh'])

    @unittest.skip('slow, refactor to copy vertex data')
    def test_can_copy_geom_by_ref(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_skinned)
        vmesh_old = copy.deepcopy(vmesh)
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
        vmesh_old = modmesh.LoadBF2Mesh(self.path_object_skinned) # faster than deepcopy
        if not vmesh.isSkinnedMesh:
            self.fail("Source mesh not skinned")
        path_object_skinned_clone = os.path.join(*['tests', 'generated', 'edit', 'kits', 'mec_geom_delete', 'Meshes', 'mec_kits_geom_delete.skinnedMesh'])

        # delete from "middle"
        id_geom_delete = 1
        vstart_at = vmesh.geoms[id_geom_delete].lods[0].materials[0].vstart
        istart_at = vmesh.geoms[id_geom_delete].lods[0].materials[0].istart
        vnum_to_delete = sum([sum([material.vnum for material in lod.materials]) for lod in vmesh.geoms[id_geom_delete].lods])
        inum_to_delete = sum([sum([material.inum for material in lod.materials]) for lod in vmesh.geoms[id_geom_delete].lods])
        geomnum_before = vmesh.geomnum
        geoms_old = vmesh_old.geoms
        vertices_old = vmesh_old.vertices
        indices_old = vmesh_old.index
        vnum_before = vmesh.vertnum
        inum_before = vmesh.indexnum
        
        # transforming
        modmesh.VisMeshTransform(vmesh).delete_geom_id(id_geom_delete)
        vmesh.save(path_object_skinned_clone)
        
        # checking geoms arr
        self.assertTrue(vmesh.geomnum == geomnum_before - 1)
        self.assertTrue(len(vmesh.geoms) == geomnum_before - 1)
        # verify that we cleaned up unnecessary vertex data
        self.assertTrue(vmesh.vertnum == vnum_before - vnum_to_delete)
        self.assertTrue(len(vmesh.vertices) == len(vertices_old) -
            sum([len(D3DDECLTYPE(attrib.vartype)) for attrib in vmesh.vertattrib]) * vnum_to_delete)
        # and corrected vertex indices
        self.assertTrue(vmesh.indexnum == inum_before - inum_to_delete)
        self.assertTrue(len(vmesh.index) == inum_before - inum_to_delete)
        # verify that geoms adjusted vstart and istart offsets properly
        id_geom = id_geom_delete
        while id_geom < vmesh.geomnum:
            id_geom_old = id_geom+1
            for id_lod, lod in enumerate(vmesh.geoms[id_geom].lods):
                rignum_old = geoms_old[id_geom_old].lods[id_lod].rignum
                self.assertTrue(lod.rignum == rignum_old)
                for id_rig, rig in enumerate(lod.rigs):
                    bonenum_old = geoms_old[id_geom_old].lods[id_lod].rigs[id_rig].bonenum
                    self.assertTrue(rig.bonenum == bonenum_old)
                    for id_bone, bone in enumerate(rig.bones):
                        self.assertTrue(bone.id == geoms_old[id_geom_old].lods[id_lod].rigs[id_rig].bones[id_bone].id)
                        self.assertTrue(bone.matrix == geoms_old[id_geom_old].lods[id_lod].rigs[id_rig].bones[id_bone].matrix)
                for id_mat, material in enumerate(lod.materials):
                    self.assertTrue(material.vnum == geoms_old[id_geom_old].lods[id_lod].materials[id_mat].vnum)
                    self.assertTrue(material.vstart == geoms_old[id_geom_old].lods[id_lod].materials[id_mat].vstart - vnum_to_delete)
                    self.assertTrue(material.inum == geoms_old[id_geom_old].lods[id_lod].materials[id_mat].inum)
                    self.assertTrue(material.istart == geoms_old[id_geom_old].lods[id_lod].materials[id_mat].istart - inum_to_delete)
                    # and verify that we deleted vertex and index with correct offset
                    vstart = int(vmesh.vertstride / vmesh.vertformat * material.vstart)
                    vstart_old = int(vmesh.vertstride / vmesh.vertformat * geoms_old[id_geom_old].lods[id_lod].materials[id_mat].vstart)
                    vnum = int(vmesh.vertstride / vmesh.vertformat * material.vnum)
                    for id_data, vdata in enumerate(vmesh.vertices[vstart:vstart+vnum]):
                        # Apparently pr skinnedmeshes containing nan data in vertices array
                        #  test fails as nan != nan even through rest of data are same
                        if math.isnan(vdata) and math.isnan(vertices_old[vstart_old+id_data]):
                            continue
                        self.assertEqual(vdata, vertices_old[vstart_old+id_data],
                            msg='id {}:{} after {},\nvnum_to_delete = {},\nat geom{} lod{} material{}'.format(vstart+id_data, vstart_old+id_data,
                                id_data,
                                vnum_to_delete,
                                id_geom,
                                id_lod,
                                id_mat)
                                )
                    #'''
                    inum = material.inum
                    istart = material.istart
                    istart_old = geoms_old[id_geom_old].lods[id_lod].materials[id_mat].istart
                    for id_index, index in enumerate(vmesh.index[istart:istart+inum]):
                        self.assertEqual(index, indices_old[istart_old+id_index])
            id_geom += 1
    
    #@unittest.skip('TODO: make sure to rebuild vertices and indices')
    def test_can_edit_geoms_order(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_skinned)
        vmesh_old = modmesh.LoadBF2Mesh(self.path_object_skinned) # faster than deepcopy
        if not vmesh.isSkinnedMesh:
            self.fail("Source mesh not skinned")
        path_object_skinned_clone = os.path.join(*['tests', 'generated', 'edit', 'kits', 'mec_geoms_ordered', 'Meshes', 'mec_kits_geoms_ordered.skinnedMesh'])

        # for simplicity we'll just reverse geoms list
        order_old = [i for i in range(vmesh.geomnum)]
        order_new = list(reversed(order_old))

        geoms_old = vmesh_old.geoms
        vertices_old = vmesh_old.vertices
        indices_old = vmesh_old.index
        
        modmesh.VisMeshTransform(vmesh).order_geoms_by(order_new)
        vmesh.save(path_object_skinned_clone)
        
        # verify geomtable reversed properly
        for id_geom, geom in enumerate(vmesh.geoms):
            id_geom_old = len(vmesh.geoms) - id_geom - 1 # idk, numering start from 0?
            geom_old = geoms_old[id_geom_old]
            self.assertTrue(geom.lodnum == geom_old.lodnum)
            self.assertTrue(len(geom.lods) == len(geom_old.lods))
            for id_lod, lod in enumerate(geom.lods):
                lod_old = geom_old.lods[id_lod]
                self.assertTrue(lod.rignum == lod_old.rignum)
                self.assertTrue(len(lod.rigs) == len(lod_old.rigs))
                for id_rig, rig in enumerate(lod.rigs):
                    rig_old = lod_old.rigs[id_rig]
                    self.assertTrue(rig.bonenum == rig_old.bonenum)
                    self.assertTrue(rig.bonenum == rig_old.bonenum)
                    for id_bone, bone in enumerate(rig.bones):
                        bone_old = rig_old.bones[id_bone]
                        self.assertTrue(bone.id == bone_old.id)
                        self.assertTrue(bone.matrix == bone_old.matrix)
                for id_mat, material in enumerate(lod.materials):
                    material_old = lod_old.materials[id_mat]
                    self.assertTrue(material.vnum == material_old.vnum)
                    self.assertTrue(material.inum == material_old.inum)
                    self.assertTrue(material.vstart == material_old.vstart)
                    self.assertTrue(material.istart == material_old.istart)

                    # verify that we have same geom data packed properly
                    vstart = int(vmesh.vertstride / vmesh.vertformat * material.vstart)
                    vstart_old = int(vmesh.vertstride / vmesh.vertformat * geoms_old[id_geom_old].lods[id_lod].materials[id_mat].vstart)
                    vnum = int(vmesh.vertstride / vmesh.vertformat * material.vnum)
                    for id_vdata, vdata in enumerate(vmesh.vertices[vstart:vstart+vnum]):
                        # Apparently pr skinnedmeshes containing nan data in vertices array
                        #  test fails as nan != nan even through rest of data are same
                        if math.isnan(vdata) and math.isnan(vertices_old[vstart_old+id_vdata]):
                            continue
                        self.assertEqual(vdata, vertices_old[vstart_old+id_vdata])
                    
                    # and proper indices
                    inum = material.inum
                    istart = material.istart
                    istart_old = geoms_old[id_geom_old].lods[id_lod].materials[id_mat].istart
                    for id_index, index in enumerate(vmesh.index[istart:istart+inum]):
                        self.assertEqual(index, indices_old[istart_old+id_index])




if __name__ == '__main__':
    unittest.main()
        