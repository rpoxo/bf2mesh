import unittest
import struct
import logging

from bf2mesh.bf2types import USED, UNUSED
from bf2mesh.bf2types import D3DDECLTYPE, D3DDECLUSAGE
import bf2mesh.visiblemesh
from bf2mesh.visiblemesh import VisibleMesh

class test_visiblemesh_read_static(unittest.TestCase):

    def setUp(self):
        self.path_mesh = 'tests/samples/staticmesh/evil_box/meshes/evil_box.staticmesh'

    def test_can_read_header(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            self.assertEqual(vmesh.head.u1, 0)
            self.assertEqual(vmesh.head.version, 11) # statics usuallly being 11, old ones is 4
            self.assertEqual(vmesh.head.u3, 0)
            self.assertEqual(vmesh.head.u4, 0)
            self.assertEqual(vmesh.head.u5, 0)
    
    def test_can_read_u1(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            self.assertEqual(vmesh.u1, 0)

    def test_can_read_geomnum(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            self.assertEqual(vmesh.geomnum, 1)
    
    def test_can_read_geom_table(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            self.assertTrue(len(vmesh.geoms) == vmesh.geomnum == 1)
            self.assertEqual(vmesh.geoms[0].lodnum, 1)
        
    def test_can_read_vertattribnum(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            # by default 3dsmax exporter gives 5 attribs + 4 empty UV maps
            self.assertEqual(vmesh.vertattribnum, 10)
    
    def test_can_read_vertex_attribute_table(self):
        mock_vertattrib = [
            bf2mesh.visiblemesh._bf2vertattrib(USED, 0, D3DDECLTYPE.FLOAT3, D3DDECLUSAGE.POSITION),
            bf2mesh.visiblemesh._bf2vertattrib(USED, 0, D3DDECLTYPE.FLOAT3, D3DDECLUSAGE.NORMAL),
            bf2mesh.visiblemesh._bf2vertattrib(USED, 0, D3DDECLTYPE.D3DCOLOR, D3DDECLUSAGE.BLENDINDICES),
            bf2mesh.visiblemesh._bf2vertattrib(USED, 0, D3DDECLTYPE.FLOAT2, D3DDECLUSAGE.UV1),
            bf2mesh.visiblemesh._bf2vertattrib(USED, 0, D3DDECLTYPE.FLOAT2, D3DDECLUSAGE.UV2),
            bf2mesh.visiblemesh._bf2vertattrib(USED, 0, D3DDECLTYPE.FLOAT2, D3DDECLUSAGE.UV3),
            bf2mesh.visiblemesh._bf2vertattrib(USED, 0, D3DDECLTYPE.FLOAT2, D3DDECLUSAGE.UV4),
            bf2mesh.visiblemesh._bf2vertattrib(USED, 0, D3DDECLTYPE.FLOAT2, D3DDECLUSAGE.UV5),
            bf2mesh.visiblemesh._bf2vertattrib(USED, 0, D3DDECLTYPE.FLOAT3, D3DDECLUSAGE.TANGENT),
            bf2mesh.visiblemesh._bf2vertattrib(UNUSED, 0, D3DDECLTYPE.UNUSED, D3DDECLUSAGE.POSITION),
        ]
        # recalculating offset
        offset = 0
        for id, vertattrib in enumerate(mock_vertattrib, 1):
            if vertattrib.flag == UNUSED:
                # TODO: think what'll happend if UNUSED in middle of array
                vertattrib.offset = 0
            else:
                vertattrib.offset = offset

            # seems like offset size should be mapped to VisibleMesh.vertformat, but we reading it later from file
            size_previous = len(mock_vertattrib[id-1].vartype) * struct.calcsize('f')
            offset += size_previous
            logging.debug('attrib [%d] = %d %d %d %d' % (id, vertattrib.flag, vertattrib.offset, vertattrib.vartype, vertattrib.usage))

        with VisibleMesh(self.path_mesh) as vmesh:
            self.assertEqual(len(mock_vertattrib), len(vmesh.vertex_attributes))
            for id in range(vmesh.vertattribnum):
                self.assertEqual(mock_vertattrib[id].flag, vmesh.vertex_attributes[id].flag)
                self.assertEqual(mock_vertattrib[id].offset, vmesh.vertex_attributes[id].offset)
                self.assertEqual(mock_vertattrib[id].vartype, vmesh.vertex_attributes[id].vartype)
                self.assertEqual(mock_vertattrib[id].usage, vmesh.vertex_attributes[id].usage)
        
    
    def test_can_read_vertex_format(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            self.assertEqual(vmesh.vertformat, 4)

    def test_can_read_vertstride(self):
        with VisibleMesh(self.path_mesh) as vmesh:

            vertstride = 0
            for attrib in vmesh.vertex_attributes:
                vertstride += len(D3DDECLTYPE(attrib.vartype)) * vmesh.vertformat
            self.assertEqual(vmesh.vertstride, (vertstride))

    def test_can_read_vertnum(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            # 3dsmax exported box have additional vertex, classical box should be 3*8=24 vertices
            self.assertEqual(vmesh.vertnum, 25)

    def test_can_read_vertex_block(self):
        mock_test_data = (
            0.5, 0.0, 0.5, # position
            0.0, -1.0, 0.0 # normals
        )
        with VisibleMesh(self.path_mesh) as vmesh:
            # no need to mock whole vertices array in test, reading first few
            self.assertEqual(vmesh.vertices[0:6], mock_test_data[0:6])

    def test_can_read_indexnum(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            self.assertEqual(vmesh.indexnum, 36)

    def test_can_read_index_block(self):
        mock_test_data = (22, 23, 20, 20, 21, 22)
        with VisibleMesh(self.path_mesh) as vmesh:
            # no need to mock whole vertices array in test, reading first few
            self.assertEqual(vmesh.index[0:6], mock_test_data[0:6])

    def test_can_read_u2(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            self.assertEqual(vmesh.u2, 8) # some weirdo bfp4f stuff

    def test_can_read_lod_table(self):
        # node deformation matrix? cant remember
        mock_node_matrix = [
            (1.0, 0.0, 0.0, 0.0),
            (0.0, 1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0, 0.0),
            (0.0, 0.0, 0.0, 1.0)
        ]
        with VisibleMesh(self.path_mesh) as vmesh:
            self.assertEqual(vmesh.geoms[0].lods[0].min, (-0.5, 0, -0.5))
            self.assertEqual(vmesh.geoms[0].lods[0].max, (0.5, 1.0, 0.5))
            self.assertEqual(vmesh.geoms[0].lods[0].nodenum, 1)
            self.assertEqual(vmesh.geoms[0].lods[0].nodes[0], mock_node_matrix)
    

    def test_can_read_materials(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            self.assertEqual(vmesh.geoms[0].lods[0].matnum, 1)
            self.assertEqual(vmesh.geoms[0].lods[0].materials[0].alphamode, 0)
            self.assertEqual(vmesh.geoms[0].lods[0].materials[0].fxfile, b'StaticMesh.fx')
            self.assertEqual(vmesh.geoms[0].lods[0].materials[0].technique, b'Base')
            self.assertEqual(vmesh.geoms[0].lods[0].materials[0].mapnum, 2)
            self.assertEqual(vmesh.geoms[0].lods[0].materials[0].maps[0], b'objects/staticobjects/test/evil_box/textures/evil_box_c.dds')
            self.assertEqual(vmesh.geoms[0].lods[0].materials[0].maps[1], b'Common\Textures\SpecularLUT_pow36.dds')  # pylint: disable=W1401
            self.assertEqual(vmesh.geoms[0].lods[0].materials[0].vstart, 0)
            self.assertEqual(vmesh.geoms[0].lods[0].materials[0].istart, 0)
            self.assertEqual(vmesh.geoms[0].lods[0].materials[0].inum, 36)
            self.assertEqual(vmesh.geoms[0].lods[0].materials[0].vnum, 25)
            self.assertEqual(vmesh.geoms[0].lods[0].materials[0].u4, 8064) # no idea what this shit is
            self.assertEqual(vmesh.geoms[0].lods[0].materials[0].u5, 65535)
            self.assertEqual(vmesh.geoms[0].lods[0].materials[0].mmin, (-0.5, 0.0, -0.5))
            self.assertEqual(vmesh.geoms[0].lods[0].materials[0].mmax, (0.5, 1.0, 0.5))

    def test_can_load_staticmesh(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            self.assertTrue(vmesh.isStaticMesh)
            self.assertTrue(vmesh.isLoaded)

class test_visiblemesh_read_static_destroyable(unittest.TestCase):
    '''
    Destroyable static meshes have geom1 for destroyed state
    '''

    def setUp(self):
        self.path_mesh = 'tests/samples/staticmesh/evil_box_dest/meshes/evil_box_dest.staticmesh'

    def test_can_read_geomnum(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            self.assertEqual(vmesh.geomnum, 2)
    
    def test_can_read_geom_table(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            self.assertTrue(len(vmesh.geoms) == vmesh.geomnum == 2)
            self.assertEqual(vmesh.geoms[0].lodnum, 1)
            self.assertEqual(vmesh.geoms[1].lodnum, 1)

class test_visiblemesh_read_skinned_kits(unittest.TestCase):
    '''
    Rigged meshes to one skeleton, many geoms
    '''

    def setUp(self):
        self.path_mesh = 'tests/samples/skinnedmesh/kits/ru/meshes/ru_kits.skinnedmesh'
    
    def test_can_read_geomnum(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            self.assertEqual(vmesh.geomnum, 22)
    
    def test_can_read_rignum(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            lod = vmesh.geoms[0].lods[0]
            self.assertEqual(lod.rignum, 1)
            self.assertEqual(len(lod.rigs), 1)

    def test_can_read_bonenum(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            rig = vmesh.geoms[0].lods[0].rigs[0]
            self.assertEqual(rig.bonenum, 6)
            self.assertEqual(len(rig.bones), 6)
    
    def test_can_read_bones_id(self):
        with VisibleMesh(self.path_mesh) as vmesh:
            bones = vmesh.geoms[0].lods[0].rigs[0].bones
            self.assertEqual(bones[0].id, 0)
            self.assertEqual(bones[1].id, 12)
            self.assertEqual(bones[2].id, 13)
            self.assertEqual(bones[3].id, 47)
            self.assertEqual(bones[4].id, 79)
            self.assertEqual(bones[5].id, 11)
    