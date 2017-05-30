import unittest
import unittest.mock as mock
import tempfile
import os
import sys
import struct

from tests_basic import chunks, TestMod

import bf2
import mesher

class TestStdMeshMerging(unittest.TestCase):

    def setUp(self):
        # NOTE: THIS IS VERY SPECIFIC TESTS FOR TEST MODEL READ
        test_object_std = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box', 'meshes', 'evil_box.staticmesh'])
        test_object_with_offset = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box_single_offset', 'meshes', 'evil_box_single_offset.staticmesh'])
        test_object_merged = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box5', 'meshes', 'evil_box5.staticmesh'])
        test_object_generated = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box_generated', 'meshes', 'evil_box_generated.staticmesh'])
        
        self.path_object_std = os.path.join(bf2.Mod().root, test_object_std)
        self.path_object_std_2 = os.path.join(bf2.Mod().root, test_object_with_offset)
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
