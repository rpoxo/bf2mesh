import os
import unittest
import copy
import struct

import bf2
import meshes

class TestStdMesOperations(unittest.TestCase):

    def setUp(self):
        # NOTE: THIS IS VERY SPECIFIC TESTS FOR TEST MODEL READ
        mesh_box = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box', 'meshes', 'evil_box.staticmesh'])
        mesh_box_offset_position = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box', 'meshes', 'evil_box_offset_position.staticmesh'])
        mesh_box_offset_UV = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box', 'meshes', 'evil_box_offset_UV.staticmesh'])
        
        self.box = os.path.join(bf2.Mod().root, mesh_box)
        self.box_offset_position = os.path.join(bf2.Mod().root, mesh_box_offset_position)
        self.box_offset_UV = os.path.join(bf2.Mod().root, mesh_box_offset_UV)
    
    def test_offset_box_position(self):
        vmesh = meshes.LoadBF2Mesh(self.box)
        
        offset = (0.0, 1.0, 0.0)
        old_vertices = list(copy.deepcopy(vmesh.vertices))
        vmesh.offset_vertices(offset)

        counter = 0
        while old_vertices:
            chunk = old_vertices[0:18]
            del old_vertices[0:18]

            position = tuple(chunk[0:3])
            array_offset = int(counter * (len(vmesh.vertices) / vmesh.vertnum)) # counter * 450/25
            new_position = tuple(vmesh.vertices[array_offset:array_offset+3])
            #print(array_offset)
            #print('{} --> {}'.format(position, new_position))
            self.assertTrue(new_position[0] == (position[0]+offset[0]))
            self.assertTrue(new_position[1] == (position[1]+offset[1]))
            self.assertTrue(new_position[2] == (position[2]+offset[2]))

            counter += 1

        vmesh.write_file_data(self.box_offset_position)

    def test_can_offset_UV1(self):
        vmesh = meshes.LoadBF2Mesh(self.box)
        
        offset = (0.0, -1.5)
        uvid = 1
        old_vertices = list(copy.deepcopy(vmesh.vertices))
        vmesh.offset_uv(offset, uvid)

        counter = 0
        while old_vertices:
            chunk = old_vertices[0:18]
            del old_vertices[0:18]

            uv1 = tuple(chunk[7:9])
            array_offset = int(counter * (len(vmesh.vertices) / vmesh.vertnum)) + 7  + int((uvid-1)*2)
            new_uv1 = tuple(vmesh.vertices[array_offset:array_offset+2])
            #print(array_offset)
            #print('{} --> {}'.format(position, new_position))
            self.assertTrue(new_uv1[0] == (uv1[0]+offset[0]))
            self.assertTrue(new_uv1[1] == (uv1[1]+offset[1]))

            counter += 1

        vmesh.write_file_data(self.box_offset_UV)











