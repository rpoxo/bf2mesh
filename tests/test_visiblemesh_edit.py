import unittest
import struct
import os

from bf2mesh.bf2types import USED, UNUSED
from bf2mesh.bf2types import D3DDECLTYPE, D3DDECLUSAGE
import bf2mesh.visiblemesh
from bf2mesh.visiblemesh import VisibleMesh

class test_visiblemesh_edit_skinnedmesh_kits(unittest.TestCase):

    def setUp(self):
        self.path_mesh = 'tests/samples/skinnedmesh/kits/ru/meshes/ru_kits.skinnedmesh'
        with VisibleMesh(self.path_mesh) as vmesh:
            if len(vmesh.geoms) != 22: self.skipTest('invalid input mesh, expected 22 geoms')

            if vmesh.geoms[2].lods[0].materials[0].vstart != 6815: self.skipTest('invalid input mesh, expected 6815 vstart for geom2lod0material0')
            if vmesh.geoms[2].lods[0].materials[0].istart != 12477: self.skipTest('invalid input mesh, expected 12477 istart for geom2lod0material0')
            if vmesh.geoms[2].lods[0].materials[0].vnum != 5108: self.skipTest('invalid input mesh, expected 5108 vertices for geom2lod0material0')
            if vmesh.geoms[2].lods[0].materials[0].inum != 10722: self.skipTest('invalid input mesh, expected 10722 indices for geom2lod0material0')
            
            if vmesh.geoms[2].lods[1].materials[0].vstart != 11923: self.skipTest('invalid input mesh, expected 11923 vstart for geom2lod1material0')
            if vmesh.geoms[2].lods[1].materials[0].istart != 23199: self.skipTest('invalid input mesh, expected 23199 istart for geom2lod1material0')
            if vmesh.geoms[2].lods[1].materials[0].vnum != 469: self.skipTest('invalid input mesh, expected 469 vertices for geom2lod1material0')
            if vmesh.geoms[2].lods[1].materials[0].inum != 741: self.skipTest('invalid input mesh, expected 741 indices for geom2lod1material0')

            if vmesh.geoms[2].lods[2].materials[0].vstart != 12392: self.skipTest('invalid input mesh, expected 12392 vstart for geom2lod2material0')
            if vmesh.geoms[2].lods[2].materials[0].istart != 23940: self.skipTest('invalid input mesh, expected 23940 istart for geom2lod2material0')
            if vmesh.geoms[2].lods[2].materials[0].vnum != 176: self.skipTest('invalid input mesh, expected 176 vertices for geom2lod2material0')
            if vmesh.geoms[2].lods[2].materials[0].inum != 246: self.skipTest('invalid input mesh, expected 246 indices for geom2lod2material0')
            
    def test_edit_order_raise_exception_if_new_order_num_not_equal(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            self.assertRaises(AttributeError, vmesh.change_geoms_order, [0, 1, 2])
    
    def test_edit_order_mesh_data_updated(self):
        def get_geom_vertices(vmesh, geomId):
            vertex_size = sum([len(D3DDECLTYPE(v_attrib.vartype)) for v_attrib in vmesh.vertex_attributes if v_attrib.flag is USED])

            geom_lod0_material0_vstart = vmesh.geoms[geomId].lods[0].materials[0].vstart * vertex_size
            geom_lods_vnum = sum([sum([material.vnum for material in lod.materials]) for lod in vmesh.geoms[geomId].lods])
            return list(vmesh.vertices[geom_lod0_material0_vstart:geom_lod0_material0_vstart + geom_lods_vnum])

        path_export = 'tests/generated/skinnedmesh/edit/ordered/kits/ru/meshes/ru_kits.skinnedmesh'
        with VisibleMesh(self.path_mesh) as vmesh:
            vertices_size_old = len(vmesh.vertices)
            vertices_geom2_vertices = get_geom_vertices(vmesh, 2)
            vmesh.change_geoms_order([0, 2, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21])

            # edited startpoints
            self.assertEqual(vmesh.geoms[1].lods[0].materials[0].vstart, vmesh.geoms[0].lods[0].materials[0].vstart + sum([lod.materials[0].vnum for lod in vmesh.geoms[0].lods]))
            self.assertEqual(vmesh.geoms[1].lods[0].materials[0].istart, vmesh.geoms[0].lods[0].materials[0].istart + sum([lod.materials[0].inum for lod in vmesh.geoms[0].lods]))

            # edited amount of vertices and indices
            self.assertEqual(vmesh.geoms[1].lods[0].materials[0].vnum, 5108)
            self.assertEqual(vmesh.geoms[1].lods[0].materials[0].inum, 10722)

            self.assertEqual(vmesh.geoms[1].lods[1].materials[0].vnum, 469)
            self.assertEqual(vmesh.geoms[1].lods[1].materials[0].inum, 741)

            self.assertEqual(vmesh.geoms[1].lods[2].materials[0].vnum, 176)
            self.assertEqual(vmesh.geoms[1].lods[2].materials[0].inum, 246)

            # edited vertices array correctly
            self.assertEqual(len(vmesh.vertices), vertices_size_old)
            vertices_geom1_vertices = get_geom_vertices(vmesh, 1)
            self.assertEqual(len(vertices_geom1_vertices), len(vertices_geom2_vertices)) #check for numbers first for early exit
            self.assertListEqual(vertices_geom2_vertices, get_geom_vertices(vmesh, 1))
            # edited indices array
            # TODO: indices update
            vmesh.export(path_export)

class test_visiblemesh_edit_staticmesh(unittest.TestCase):

    def setUp(self):
        self.meshes = {
            'simple' : (
                        'tests/samples/staticmesh/evil_box/meshes/evil_box.staticmesh',
                        'tests/generated/staticmesh/edit/translate/evil_box/meshes/evil_box.staticmesh',
                        'tests/generated/staticmesh/edit/merge/evil_box/meshes/evil_box.staticmesh',
                        'tests/generated/staticmesh/edit/rotate/evil_box/meshes/evil_box.staticmesh',
                        ),
            'lods' : (
                        'tests/samples/staticmesh/evil_box_lods/meshes/evil_box_lods.staticmesh',
                        'tests/generated/staticmesh/edit/translate/evil_box_lods/meshes/evil_box_lods.staticmesh',
                        'tests/generated/staticmesh/edit/merge/evil_box_lods/meshes/evil_box_lods.staticmesh',
                        'tests/generated/staticmesh/edit/rotate/evil_box_lods/meshes/evil_box_lods.staticmesh',
                        ),
            'dest' : (
                        'tests/samples/staticmesh/evil_box_dest/meshes/evil_box_dest.staticmesh',
                        'tests/generated/staticmesh/edit/translate/evil_box_dest/meshes/evil_box_dest.staticmesh',
                        'tests/generated/staticmesh/edit/merge/evil_box_dest/meshes/evil_box_dest.staticmesh',
                        'tests/generated/staticmesh/edit/rotate/evil_box_dest/meshes/evil_box_dest.staticmesh',
                        ),
            }
        with VisibleMesh(self.meshes['simple'][0]) as vmesh:
            if len(vmesh.geoms) != 1: self.skipTest('invalid input mesh, expected 1 geom')
        with VisibleMesh(self.meshes['lods'][0]) as vmesh:
            if len(vmesh.geoms[0].lods) != 2: self.skipTest('invalid input mesh, expected 2 lods in geom0')
        with VisibleMesh(self.meshes['dest'][0]) as vmesh:
            if len(vmesh.geoms) != 2: self.skipTest('invalid input mesh, expected 2 geoms')
    
    class Vertex(object):
        pass
        
    def test_can_translate_staticmesh(self):
        offset = (0.0, 0.0, 1.5)
        for staticmesh in self.meshes:
            path_mesh, path_export = self.meshes[staticmesh][0], self.meshes[staticmesh][1]
            with VisibleMesh(path_mesh) as vmesh:
                vertices_old = tuple(vmesh.vertices)
                vmesh.translate(offset)
                vmesh.export(path_export)

                for geomId, geom in enumerate(vmesh.geoms):
                    for lodId, lod in enumerate(geom.lods):
                        for materialId, material in enumerate(lod.materials):
                            for vertId in range(material.vnum):
                                _start = (material.vstart + vertId) * vmesh.vertex_size
                                _end = _start + vmesh.vertex_size
                                vertexBuffer = vmesh.vertices[_start:_end]
                                vertex_OldBuffer = vertices_old[_start:_end]
                                #print('%d -> %d' % (_start, _end))
                                vertex = self.Vertex()
                                vertex_old = self.Vertex()
                                for attrib in vmesh.vertex_attributes:
                                    if attrib.flag is UNUSED: continue
                                    _start = int(attrib.offset / vmesh.vertformat)
                                    _end = _start + len(D3DDECLTYPE(attrib.vartype))
                                    setattr(vertex, D3DDECLUSAGE(attrib.usage).name, vertexBuffer[_start:_end])
                                    setattr(vertex_old, D3DDECLUSAGE(attrib.usage).name, vertex_OldBuffer[_start:_end])
                                    #print('[%d]new %s to %s' % (vertId, D3DDECLUSAGE(attrib.usage).name, vertexBuffer[_start:_end]))
                                    #print('[%d]old %s to %s' % (vertId, D3DDECLUSAGE(attrib.usage).name, vertex_OldBuffer[_start:_end]))
                                self.assertEqual(tuple(a-b for a, b in zip(getattr(vertex, D3DDECLUSAGE.POSITION.name), offset)), getattr(vertex_old, D3DDECLUSAGE.POSITION.name))

    # TODO: come up with test for that shit
    def test_can_merge_staticmesh(self):
        #self.skipTest('NotImplemented')
        for staticmesh in self.meshes:
            path_mesh, path_export = self.meshes[staticmesh][0], self.meshes[staticmesh][2]
            vmesh = VisibleMesh(path_mesh)
            vmesh2 = VisibleMesh(path_mesh)
            vmesh_old = VisibleMesh(path_mesh) # to compare later

            vmesh.merge(vmesh2)
            vmesh.export(path_export)

            for geomId, geom in enumerate(vmesh.geoms):
                for lodId, lod in enumerate(geom.lods):
                    for materialId, material in enumerate(lod.materials):
                        material2 = vmesh2.geoms[geomId].lods[lodId].materials[materialId]
                        material_old = vmesh_old.geoms[geomId].lods[lodId].materials[materialId]
                        self.assertEqual(material.vnum, material2.vnum + material_old.vnum)
                        self.assertEqual(material.inum, material2.inum + material_old.inum)

    
    def test_can_rotate_staticmesh(self):
        rotation = (45.0, 0.0, 0.0)
        for staticmesh in self.meshes:
            path_mesh, path_export = self.meshes[staticmesh][0], self.meshes[staticmesh][3]
            with VisibleMesh(path_mesh) as vmesh:
                vmesh.rotate(rotation)
                vmesh.export(path_export)
        self.skipTest('DUNNO how check beside visual yet, ported from v1')


                        