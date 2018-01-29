import unittest
import tempfile
import os
import sys
import struct
import shutil
import filecmp

import bf2
import modmesh
from modmesh import D3DDECLTYPE, D3DDECLUSAGE

import tests.mock_mesh as mocks

class TestVisMeshRead(unittest.TestCase):

    def setUp(self):
        # test for simple static box - static&destoryable
        self.path_object_static = os.path.join(*['tests', 'samples', 'evil_box', 'meshes', 'evil_box.staticmesh'])
        self.path_object_dest = os.path.join(*['tests', 'samples', 'evil_box_destroyable', 'meshes', 'evil_box_destroyable.staticmesh'])

        # test for vehicle depot - bundledmesh
        # objects\common\vehicle_depot\meshes
        self.path_object_bundled = os.path.join(*['tests', 'samples', 'vehicle_depot', 'meshes', 'vehicle_depot.bundledmesh'])
        
        # test for mec kits - skinnedmesh
        # objects\kits\Mec
        self.path_object_skinned = os.path.join(*['tests', 'samples', 'kits', 'mec', 'Meshes', 'mec_kits.skinnedMesh'])

    def test_can_read_header(self):
        with open(self.path_object_static, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_head(meshfile)
    
        self.assertTrue(vmesh.head.u1 == 0)
        self.assertTrue(vmesh.head.version in [10, 6, 11]) # statics usuallly being 11, old ones is 4
        self.assertTrue(vmesh.head.u3 == 0)
        self.assertTrue(vmesh.head.u4 == 0)
        self.assertTrue(vmesh.head.u5 == 0)

    def test_can_read_u1_bfp4f_version(self):
        with open(self.path_object_static, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_u1_bfp4f_version(meshfile)
            
        self.assertTrue(vmesh.u1 == 0)

    def test_can_read_geomnum_mesh_std(self):
        with open(self.path_object_static, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_geomnum(meshfile)
            
        self.assertTrue(vmesh.geomnum == 1)

    # destroyables have secondary geom for destroyed state
    def test_can_read_geomnum_mesh_dest(self):
        with open(self.path_object_dest, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_geomnum(meshfile)

        self.assertTrue(vmesh.geomnum == 2)

    def test_can_read_geom_table_mesh_std(self):
        with open(self.path_object_static, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_geom_table(meshfile)

        self.assertTrue(len(vmesh.geoms) == vmesh.geomnum == 1)
        self.assertTrue(vmesh.geoms[0].lodnum == 1)
    
    def test_can_read_geom_table_mesh_dest(self):
        with open(self.path_object_dest, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_geom_table(meshfile)

        self.assertTrue(len(vmesh.geoms) == vmesh.geomnum == 2)
        # test mesh i exported have 2 lods per each geom
        self.assertTrue(vmesh.geoms[0].lodnum == 2)
        self.assertTrue(vmesh.geoms[1].lodnum == 2)

    def test_can_read_vertattribnum_mesh_std(self):
        with open(self.path_object_static, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_vertattribnum(meshfile)

        # by default 3dsmax exporter gives 5 attribs + 4 empty UV maps
        self.assertTrue(vmesh.vertattribnum == 9)

    def test_can_read_vertattribnum_mesh_dest(self):
        with open(self.path_object_dest, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_vertattribnum(meshfile)
        self.assertTrue(vmesh.vertattribnum == 9)
    
    def test_can_read_vertex_attribute_table(self):
        with open(self.path_object_static, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_vertattrib_table(meshfile)
        
        # bf2 flags
        USED = 0
        UNUSED = 255

        offset = 0
        self.assertTrue(vmesh.vertattrib[0] == (USED,
                                                offset,
                                                D3DDECLTYPE.FLOAT3,
                                                D3DDECLUSAGE.POSITION))

        offset += len(D3DDECLTYPE(vmesh.vertattrib[0].vartype)) * 4
        self.assertTrue(vmesh.vertattrib[1] == (USED,
                                                offset,
                                                D3DDECLTYPE.FLOAT3,
                                                D3DDECLUSAGE.NORMAL))

        offset += len(D3DDECLTYPE(vmesh.vertattrib[1].vartype)) * 4
        self.assertTrue(vmesh.vertattrib[2] == (USED,
                                                offset,
                                                D3DDECLTYPE.D3DCOLOR,
                                                D3DDECLUSAGE.BLENDINDICES))

        offset += len(D3DDECLTYPE(vmesh.vertattrib[2].vartype)) * 4
        self.assertTrue(vmesh.vertattrib[3] == (USED,
                                                offset,
                                                D3DDECLTYPE.FLOAT2,
                                                D3DDECLUSAGE.UV1))

        offset += len(D3DDECLTYPE(vmesh.vertattrib[3].vartype)) * 4
        self.assertTrue(vmesh.vertattrib[4] == (USED,
                                                offset,
                                                D3DDECLTYPE.FLOAT2,
                                                D3DDECLUSAGE.UV2))

        offset += len(D3DDECLTYPE(vmesh.vertattrib[4].vartype)) * 4
        self.assertTrue(vmesh.vertattrib[5] == (USED,
                                                offset,
                                                D3DDECLTYPE.FLOAT2,
                                                D3DDECLUSAGE.UV3))

        offset += len(D3DDECLTYPE(vmesh.vertattrib[5].vartype)) * 4
        self.assertTrue(vmesh.vertattrib[6] == (USED,
                                                offset,
                                                D3DDECLTYPE.FLOAT2,
                                                D3DDECLUSAGE.UV4))

        offset += len(D3DDECLTYPE(vmesh.vertattrib[6].vartype)) * 4
        self.assertTrue(vmesh.vertattrib[7] == (USED,
                                                offset,
                                                D3DDECLTYPE.FLOAT3,
                                                D3DDECLUSAGE.TANGENT))

        self.assertTrue(vmesh.vertattrib[8] == (UNUSED,
                                                0, # some unused value
                                                D3DDECLTYPE.UNUSED,
                                                D3DDECLUSAGE.POSITION))

        self.assertTrue(len(vmesh.vertattrib) == vmesh.vertattribnum)

    def test_can_read_vertformat(self):
        with open(self.path_object_static, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_vertformat(meshfile)
        self.assertTrue(vmesh.vertformat == 4) # 4 bytes per data

    def test_can_read_vertstride(self):
        with open(self.path_object_static, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_vertstride(meshfile)

        _vertstride = 0
        for attrib in vmesh.vertattrib:
            _vertstride += len(D3DDECLTYPE(attrib.vartype))*4
        self.assertTrue(vmesh.vertstride == (_vertstride))

    def test_can_read_vertnum(self):
        with open(self.path_object_static, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_vertnum(meshfile)
        self.assertTrue(vmesh.vertnum == 25) # 3dsmax exported box have additional vertex

    def test_can_read_vertex_block(self):
        with open(self.path_object_static, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_vertex_block(meshfile)
        self.assertTrue(len(vmesh.vertices) == vmesh.vertnum * vmesh.vertstride / vmesh.vertformat)

    def test_can_read_indexnum(self):
        with open(self.path_object_static, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_indexnum(meshfile)

        self.assertTrue(vmesh.indexnum == 36)

    def test_can_read_index_block(self):
        with open(self.path_object_static, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_index_block(meshfile)

        self.assertTrue(len(vmesh.index) == vmesh.indexnum == 36)

    def test_can_read_u2(self):
        with open(self.path_object_static, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_u2(meshfile)

        self.assertTrue(vmesh.u2 is 8) # some weirdo bfp4f stuff

    def test_can_read_nodes(self):
        with open(self.path_object_static, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_nodes(meshfile)

        self.assertTrue(vmesh.geoms[0].lods[0].min == (-0.5, 0, -0.5))
        self.assertTrue(vmesh.geoms[0].lods[0].max == (0.5, 1.0, 0.5))
        #self.assertTrue(vmesh.geoms[0].lod[0].pivot == (0.5, 1.0, 0.5)) # some old bundleds?
        self.assertTrue(vmesh.geoms[0].lods[0].nodenum == 1)
    
    def test_can_read_nodes_bundledmesh(self):
        with open(self.path_object_bundled, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh.isBundledMesh = True
            vmesh._read_nodes(meshfile)

        self.assertTrue(vmesh.geoms[0].lods[0].nodenum == 1)
    
    def test_can_read_nodes_skinnedmesh(self):
        with open(self.path_object_skinned, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh.isSkinnedMesh = True
            vmesh._read_nodes(meshfile)
            
        for geom in vmesh.geoms:
            for lod in geom.lods:
                self.assertTrue(lod.rignum == 1)

        # debugging
        '''
        for id_geom in range(vmesh.geomnum):
            print('\ngeom{}'.format(id_geom))
            for id_lod in range(vmesh.geoms[id_geom].lodnum):
                print('  lod{}'.format(id_lod))
                for id_rig in range(vmesh.geoms[id_geom].lods[id_lod].rignum):
                    print('    rig{}'.format(id_rig))
                    for id_bone in range(vmesh.geoms[id_geom].lods[id_lod].rigs[id_rig].bonenum):
                        print('      bone{}'.format(id_bone))
                        print('        id = {}'.format(vmesh.geoms[id_geom].lods[id_lod].rigs[id_rig].bones[id_bone].id))
        '''

    def test_can_read_materials(self):
        with open(self.path_object_static, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_materials(meshfile)

        self.assertTrue(vmesh.geoms[0].lods[0].matnum == 1)
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].alphamode == 0)
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].fxfile == b'StaticMesh.fx')
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].technique == b'Base')
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].mapnum == 2)
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].maps[0] == b'objects/staticobjects/test/evil_box/textures/evil_box_c.dds')
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].maps[1] == b'Common\Textures\SpecularLUT_pow36.dds')
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].vstart == 0)
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].istart == 0)
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].inum == 36)
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].vnum == 25)
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].u4 == 8064) # no idea what this shit is
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].u5 == 65535)
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].mmin == (-0.5, 0.0, -0.5))
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].mmax == (0.5, 1.0, 0.5))
        self.assertTrue(vmesh.geoms[0].lods[0].polycount == 12)
    
    def test_can_read_materials_skinnedmesh(self):
        with open(self.path_object_skinned, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh.isSkinnedMesh = True
            vmesh._read_materials(meshfile)

        for geom in vmesh.geoms:
            for lod in geom.lods:
                lod.matnum = 1
                for material in lod.materials:
                    self.assertTrue(material.maps[0] == b'objects/kits/mec/textures/mec_kits_c.dds')

    def test_can_load_bf2_staticmesh(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_static)
        self.assertTrue(isinstance(vmesh, modmesh.VisMesh))
        self.assertTrue(vmesh.isStaticMesh)
    
    def test_can_load_bf2_bundled_mesh(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_bundled)
        self.assertTrue(isinstance(vmesh, modmesh.VisMesh))
        self.assertTrue(vmesh.isBundledMesh)
    
    def test_can_load_bf2_skinned_mesh(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_skinned)
        self.assertTrue(isinstance(vmesh, modmesh.VisMesh))
        self.assertTrue(vmesh.isSkinnedMesh)


class TestVisMesh_Special(unittest.TestCase):

    # objects\staticobjects\Bridges\EoD_Bridge_Big\modmesh\eod_bridge_big.staticmesh
    # it has version 4 and inum and vnum in material
    #@unittest.skip('memory issues')
    @unittest.skip('enable if have mesh')
    def test_can_read_mesh_version_4(self):
        path_mesh = os.path.join(*['tests', 'samples', 'EoD_Bridge_Big', 'meshes', 'eod_bridge_big.staticmesh'])
        #vmesh = modmesh.LoadBF2Mesh(path_mesh)
        with open(path_mesh, 'rb') as meshfile:
            vmesh = modmesh.VisMesh()
            vmesh._read_materials(meshfile)
            
    @unittest.skip('bad i\o intensive test, depends on local meshes...')
    def test_can_read_PR_modmesh_REPO(self):
        counter = 0
        for dir, dirnames, filenames in os.walk(os.path.join(bf2.Mod().root, 'objects')):
            for filename in filenames:
                ext = filename.split('.')[-1].lower()
                if ext[-4:] == 'mesh' and ext not in ['collisionmesh'] and 'test' not in dir:
                    counter += 1
                    try:
                        vmesh = modmesh.LoadBF2Mesh(os.path.join(bf2.Mod().root, dir, filename))
                    except struct.error:
                        print('Failed to load {}'.format(os.path.join(bf2.Mod().root, dir, filename)))
                        raise
            print(counter)
        #raise

    
if __name__ == '__main__':
    unittest.main()
