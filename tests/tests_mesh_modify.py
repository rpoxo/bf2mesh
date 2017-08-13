import os
import unittest
import copy
import struct

import bf2
import modmesh
import modmesh

@unittest.skip('testing failed mesh load')
class TestStdMeshOperations(unittest.TestCase):

    def setUp(self):
        box_std = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box', 'meshes', 'evil_box.staticmesh'])
        modified_box_position = os.path.join(*['objects', 'staticobjects', 'test', 'generated', 'modified_box_position', 'meshes', 'modified_box_position.staticmesh'])
        modified_box_UV1 = os.path.join(*['objects', 'staticobjects', 'test', 'generated', 'modified_box_UV1', 'meshes', 'modified_box_UV1.staticmesh'])
        
        self.box_std = os.path.join(bf2.Mod().root, box_std)
        self.modified_box_position = os.path.join(bf2.Mod().root, modified_box_position)
        self.modified_box_UV1 = os.path.join(bf2.Mod().root, modified_box_UV1)

    def test_can_offset_mesh(self):
        vmesh = meshes.LoadBF2Mesh(self.box_std)

        offset = (0.0, 0.0, 1.0)
        modmesh.offset_vertices(vmesh, offset)
        vmesh.write_file_data(self.modified_box_position)
    
    def test_can_offset_UV1(self):
        vmesh = meshes.LoadBF2Mesh(self.box_std)

        offset = (0.5, 0.5)
        modmesh.offset_UV1(vmesh, offset)
        vmesh.write_file_data(self.modified_box_UV1)

@unittest.skip('testing failed mesh load')
class TestMaterialsOptimization(unittest.TestCase):

    def setUp(self):
        # File: "D:\Games\Project Reality\mods\pr_repo\objects\weapons\Handheld\GBRIF_L85A2iron\meshes\gbrif_l85a2iron.bundledmesh"
        l85_mesh = os.path.join(*['objects', 'weapons', 'Handheld', 'GBRIF_L85A2iron', 'meshes', 'gbrif_l85a2iron.bundledmesh'])
        modified_mesh_position = os.path.join(*['objects', 'weapons', 'Handheld', 'GBRIF_L85A2iron', 'meshes', 'gbrif_l85a2iron_position.bundledmesh'])
        modified_mesh_materials = os.path.join(*['objects', 'weapons', 'Handheld', 'GBRIF_L85A2iron', 'meshes', 'gbrif_l85a2iron_materials.bundledmesh'])
        
        self.l85_mesh = os.path.join(bf2.Mod().root, l85_mesh)
        self.modified_mesh_position = os.path.join(bf2.Mod().root, modified_mesh_position)
        self.modified_mesh_materials = os.path.join(bf2.Mod().root, modified_mesh_materials)

    @unittest.skip('disabled: only for manual use')
    def test_can_offset_mesh(self):
        vmesh = meshes.LoadBF2Mesh(self.l85_mesh)

        offset = (0.0, 0.0, 1.0)
        modmesh.offset_vertices(vmesh, offset)
        vmesh.write_file_data(self.modified_mesh_position)

    def test_can_modify_l85_last_material(self):
        vmesh = meshes.LoadBF2Mesh(self.l85_mesh)
        
        geom = 0
        lod = 0
        mat_parent = 2
        mat_child = 3
        modmesh.merge_materials(vmesh, geom, lod, mat_parent, mat_child)
        vmesh.write_file_data(self.modified_mesh_materials)
        raise
