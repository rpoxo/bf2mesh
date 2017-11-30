import unittest
import tempfile
import os
import sys
import struct
import shutil
import filecmp

import bf2
import modmesh

class TestStdMeshReading(unittest.TestCase):

    def setUp(self):
        # NOTE: THIS IS VERY SPECIFIC TESTS AGAINST PREPARED OBJECT
        self.path_object_std = os.path.join(*['tests', 'samples', 'evil_box', 'meshes', 'evil_box.staticmesh'])
        self.path_object_dest = os.path.join(*['tests', 'samples', 'evil_box_destroyable', 'meshes', 'evil_box_destroyable.staticmesh'])

    def test_can_read_header(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_head(meshfile)
            
        self.assertTrue(vmesh.head.u1 == 0)
        self.assertTrue(vmesh.head.version in [10, 6, 11]) # statics usuallly being 11, old ones is 4
        self.assertTrue(vmesh.head.u3 == 0)
        self.assertTrue(vmesh.head.u4 == 0)
        self.assertTrue(vmesh.head.u5 == 0)

    def test_can_read_u1_bfp4f_version(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_u1_bfp4f_version(meshfile)
            
        self.assertTrue(vmesh.u1 == 0)

    def test_can_read_geomnum_mesh_std(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_geomnum(meshfile)
            
        self.assertTrue(vmesh.geomnum == 1)

    # destroyables have secondary geom for destroyed state
    def test_can_read_geomnum_mesh_dest(self):
        with open(self.path_object_dest, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_geomnum(meshfile)

        self.assertTrue(vmesh.geomnum == 2)

    def test_can_read_geom_table_mesh_std(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_geom_table(meshfile)

        self.assertTrue(len(vmesh.geoms) == vmesh.geomnum == 1)
        self.assertTrue(vmesh.geoms[0].lodnum == 1)
    
    def test_can_read_geom_table_mesh_dest(self):
        with open(self.path_object_dest, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_geom_table(meshfile)

        self.assertTrue(len(vmesh.geoms) == vmesh.geomnum == 2)
        # test mesh i exported have 2 lods per each geom
        self.assertTrue(vmesh.geoms[0].lodnum == 2)
        self.assertTrue(vmesh.geoms[1].lodnum == 2)

    def test_can_read_vertattribnum_mesh_std(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertattribnum(meshfile)

        # by default 3dsmax exporter gives 5 attribs + 4 empty UV maps
        self.assertTrue(vmesh.vertattribnum == 9)

    def test_can_read_vertattribnum_mesh_dest(self):
        with open(self.path_object_dest, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertattribnum(meshfile)
        self.assertTrue(vmesh.vertattribnum == 9)
    
    def test_can_read_vertex_attribute_table(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertattrib_table(meshfile)
        
        # refer to 'Include/d3d9types.h' from DX SDK
        self.assertTrue(vmesh.vertattrib[0] == (0, 0, 2, 0)) # flag:used, offset=0, float3, position
        self.assertTrue(vmesh.vertattrib[1] == (0, 12, 2, 3)) # flag:used, offset=12\4, float3, normal
        self.assertTrue(vmesh.vertattrib[2] == (0, 24, 4, 2)) # flag:used, offset=24\4, d3dcolor, blend indice
        self.assertTrue(vmesh.vertattrib[3] == (0, 28, 1, 5)) # flag:used, offset=28\4, float2, uv1
        self.assertTrue(vmesh.vertattrib[4] == (0, 36, 1, 261)) # flag:used, offset=36\4, float2, uv2
        self.assertTrue(vmesh.vertattrib[5] == (0, 44, 1, 517)) # flag:used, offset=44\4, float2, uv3
        self.assertTrue(vmesh.vertattrib[6] == (0, 52, 1, 773)) # flag:used, offset=52\4, float2, uv4
        self.assertTrue(vmesh.vertattrib[7] == (0, 60, 2, 6)) # flag:used, offset=60\4, float3, tangent
        self.assertTrue(vmesh.vertattrib[8] == (255, 0, 17, 0)) # flag:unused, offset=0, unused, position

    def test_can_read_vertformat(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertformat(meshfile)
        self.assertTrue(vmesh.vertformat == 4) # 4 bytes per data

    def test_can_read_vertstride(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertstride(meshfile)
        self.assertTrue(vmesh.vertstride == 72) # 72 bytes for whole vertice chunk

    def test_can_read_vertnum(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertnum(meshfile)
        self.assertTrue(vmesh.vertnum == 25) # 3dsmax exported box have additional vertex

    def test_can_read_vertex_block(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertex_block(meshfile)
        self.assertTrue(len(vmesh.vertices) == vmesh.vertnum * vmesh.vertstride / vmesh.vertformat == 450)

    def test_can_read_indexnum(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_indexnum(meshfile)

        self.assertTrue(vmesh.indexnum == 36)

    def test_can_read_index_block(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_index_block(meshfile)

        self.assertTrue(len(vmesh.index) == vmesh.indexnum == 36)

    def test_can_read_u2(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_u2(meshfile)

        self.assertTrue(vmesh.u2 is 8) # some weirdo bfp4f stuff

    def test_can_read_nodes(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_nodes(meshfile)

        self.assertTrue(vmesh.geoms[0].lods[0].min == (-0.5, 0, -0.5))
        self.assertTrue(vmesh.geoms[0].lods[0].max == (0.5, 1.0, 0.5))
        #self.assertTrue(vmesh.geoms[0].lod[0].pivot == (0.5, 1.0, 0.5)) # some old bundleds?
        self.assertTrue(vmesh.geoms[0].lods[0].nodenum == 1)

    def test_can_read_materials(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
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
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].u4 == 8064)
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].u5 == 65535)
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].nmin == (-0.5, 0.0, -0.5))
        self.assertTrue(vmesh.geoms[0].lods[0].materials[0].nmax == (0.5, 1.0, 0.5))
        self.assertTrue(vmesh.geoms[0].lods[0].polycount == 12)

    def test_can_load_bf2_mesh(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(isinstance(vmesh, modmesh.StdMesh))
        self.assertTrue(vmesh.isStaticMesh)


#@unittest.skip('testing failed mesh load')
class TestBundleMeshReading(unittest.TestCase):

    def setUp(self):
        # test for vehicle depot
        # objects\common\vehicle_depot\modmesh
        self.path_object_std = os.path.join(*['tests', 'samples', 'vehicle_depot', 'meshes', 'vehicle_depot.bundledmesh'])

    def test_can_read_header(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_head(meshfile)

        self.assertTrue(vmesh.head.u1 == 0)
        self.assertTrue(vmesh.head.version in [10, 6, 11])
        self.assertTrue(vmesh.head.u3 == 0)
        self.assertTrue(vmesh.head.u4 == 0)
        self.assertTrue(vmesh.head.u5 == 0)

    def test_can_read_u1_bfp4f_version(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_u1_bfp4f_version(meshfile)
            
        self.assertTrue(vmesh.u1 == 0)

    def test_can_read_geomnum_mesh_std(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_geomnum(meshfile)
            
        self.assertTrue(vmesh.geomnum == 1)

    def test_can_read_geom_table_mesh_std(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_geom_table(meshfile)

        self.assertTrue(len(vmesh.geoms) == 1)
        self.assertTrue(vmesh.geoms[0].lodnum == 6)

    def test_can_read_vertattribnum_mesh_std(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertattribnum(meshfile)

        self.assertTrue(vmesh.vertattribnum == 6)
    
    def test_can_read_vertex_attribute_table(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertattrib_table(meshfile)

        self.assertTrue(vmesh.vertattrib[0] == (0, 0, 2, 0)) # flag:used, offset=0, float3, position
        self.assertTrue(vmesh.vertattrib[1] == (0, 12, 2, 3)) # flag:used, offset=12\4, float3, normal
        self.assertTrue(vmesh.vertattrib[2] == (0, 24, 4, 2)) # flag:used, offset=24\4, d3dcolor, blend indice
        self.assertTrue(vmesh.vertattrib[3] == (0, 28, 1, 5)) # flag:used, offset=28\4, float2, uv1
        self.assertTrue(vmesh.vertattrib[4] == (0, 36, 2, 6)) # flag:used, offset=36\4, float3, tangent
        self.assertTrue(vmesh.vertattrib[5] == (255, 0, 17, 0)) # flag:unused, offset=0, unused, position
        self.assertTrue(len(vmesh.vertattrib) == vmesh.vertattribnum)

    def test_can_read_vertformat(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertformat(meshfile)
        self.assertTrue(vmesh.vertformat == 4)

    def test_can_read_vertstride(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertstride(meshfile)
        self.assertTrue(vmesh.vertstride == 48)

    def test_can_read_vertnum(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertnum(meshfile)
        self.assertTrue(vmesh.vertnum == 131383) # lots of vertices

    def test_can_read_vertex_block(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertex_block(meshfile)

        self.assertTrue(len(vmesh.vertices) == vmesh.vertnum * vmesh.vertstride / vmesh.vertformat == 1576596)

    def test_can_read_indexnum(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_indexnum(meshfile)

        self.assertTrue(vmesh.indexnum == 278436)

    def test_can_read_index_block(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_index_block(meshfile)

        self.assertTrue(len(vmesh.index) == vmesh.indexnum == 278436)

    def test_can_read_u2(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_u2(meshfile)

        self.assertTrue(vmesh.u2 is 8)

    def test_can_read_nodes(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh.isBundledMesh = True
            vmesh._read_nodes(meshfile)

        self.assertTrue(vmesh.geoms[0].lods[0].nodenum == 1)

    def test_can_read_materials(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh.isBundledMesh = True
            vmesh._read_materials(meshfile)

        # fuck off, not gonna add tests for each material
        self.assertTrue(vmesh.geoms[0].lods[0].matnum == 14)
        self.assertTrue(vmesh.geoms[0].lods[1].matnum == 13)
        self.assertTrue(vmesh.geoms[0].lods[2].matnum == 12)
        self.assertTrue(vmesh.geoms[0].lods[3].matnum == 12)
        self.assertTrue(vmesh.geoms[0].lods[4].matnum == 10)
        self.assertTrue(vmesh.geoms[0].lods[5].matnum == 8)

    def test_can_load_bf2_bundled_mesh(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(isinstance(vmesh, modmesh.StdMesh))
        self.assertTrue(vmesh.isBundledMesh)
        
        
#@unittest.skip('testing failed mesh load')
class TestSkinnedMeshReading(unittest.TestCase):

    def setUp(self):
        # test for vehicle depot
        # objects\kits\Mec
        # \tests\samples\kits\mec\Meshes
        self.path_object_std = os.path.join(*['tests', 'samples', 'kits', 'mec', 'Meshes', 'mec_kits.skinnedMesh'])

    def test_can_read_header(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_head(meshfile)

        self.assertTrue(vmesh.head.u1 == 0)
        self.assertTrue(vmesh.head.version in [10, 6, 11])
        self.assertTrue(vmesh.head.u3 == 0)
        self.assertTrue(vmesh.head.u4 == 0)
        self.assertTrue(vmesh.head.u5 == 0)

    def test_can_read_u1_bfp4f_version(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_u1_bfp4f_version(meshfile)
            
        self.assertTrue(vmesh.u1 == 0)

    def test_can_read_geomnum_mesh_std(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_geomnum(meshfile)

        self.assertTrue(vmesh.geomnum == 20)

    def test_can_read_geom_table_mesh_std(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_geom_table(meshfile)

        self.assertTrue(len(vmesh.geoms) == 20)
        
        # for some reason mec kits have only 2 lods for 2? dropkits
        for id_geom in range(0,17):
            self.assertTrue(vmesh.geoms[id_geom].lodnum == 3)
        for id_geom in [17, 18]:
            self.assertTrue(vmesh.geoms[id_geom].lodnum == 2)
        self.assertTrue(vmesh.geoms[19].lodnum == 3)

    def test_can_read_vertattribnum_mesh_std(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertattribnum(meshfile)

        self.assertTrue(vmesh.vertattribnum == 7)

    def test_can_read_vertex_attribute_table(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertattrib_table(meshfile)

        self.assertTrue(vmesh.vertattrib[0] == (0,
                                                0,
                                                modmesh.D3DDECLTYPE.FLOAT3,
                                                modmesh.D3DDECLUSAGE.POSITION))
        self.assertTrue(vmesh.vertattrib[1] == (0,
                                                12,
                                                modmesh.D3DDECLTYPE.FLOAT3,
                                                modmesh.D3DDECLUSAGE.NORMAL))
        self.assertTrue(vmesh.vertattrib[2] == (0,
                                                24,
                                                modmesh.D3DDECLTYPE.FLOAT1,
                                                modmesh.D3DDECLUSAGE.BLENDWEIGHT))
        self.assertTrue(vmesh.vertattrib[3] == (0,
                                                28,
                                                modmesh.D3DDECLTYPE.D3DCOLOR,
                                                modmesh.D3DDECLUSAGE.BLENDINDICES))
        self.assertTrue(vmesh.vertattrib[4] == (0,
                                                32,
                                                modmesh.D3DDECLTYPE.FLOAT2,
                                                modmesh.D3DDECLUSAGE.UV1))
        self.assertTrue(vmesh.vertattrib[5] == (0,
                                                40,
                                                modmesh.D3DDECLTYPE.FLOAT3,
                                                modmesh.D3DDECLUSAGE.TANGENT))
        self.assertTrue(vmesh.vertattrib[6] == (255,
                                                0,
                                                modmesh.D3DDECLTYPE.UNUSED,
                                                modmesh.D3DDECLUSAGE.POSITION))
        self.assertTrue(len(vmesh.vertattrib) == vmesh.vertattribnum)

    def test_can_read_vertformat(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertformat(meshfile)

        self.assertTrue(vmesh.vertformat == 4)

    def test_can_read_vertstride(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertstride(meshfile)
        
        vertstride = 0
        for attrib in vmesh.vertattrib:
            vertstride += len(modmesh.D3DDECLTYPE(attrib.vartype))*4
        self.assertTrue(vmesh.vertstride == (vertstride))

    def test_can_read_vertnum(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertnum(meshfile)

        self.assertTrue(vmesh.vertnum == 118168)

    def test_can_read_vertex_block(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_vertex_block(meshfile)

        self.assertTrue(len(vmesh.vertices) == vmesh.vertnum * vmesh.vertstride / vmesh.vertformat == 1536184) # vertices buffer array

    def test_can_read_indexnum(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_indexnum(meshfile)

        print(vmesh.indexnum )
        self.assertTrue(vmesh.indexnum == 249279)

    def test_can_read_index_block(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_index_block(meshfile)

        self.assertTrue(len(vmesh.index) == vmesh.indexnum)

    def test_can_read_nodes(self):
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
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
        with open(self.path_object_std, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh.isSkinnedMesh = True
            vmesh._read_materials(meshfile)

        for geom in vmesh.geoms:
            for lod in geom.lods:
                lod.matnum = 1
                for material in lod.materials:
                    self.assertTrue(material.maps[0] == b'objects/kits/mec/textures/mec_kits_c.dds')

    def test_can_load_bf2_skinned_mesh(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        self.assertTrue(isinstance(vmesh, modmesh.StdMesh))
        self.assertTrue(vmesh.isSkinnedMesh)

#@unittest.skip('testing failed mesh load')
class TestMeshReading_Specials(unittest.TestCase):

    # objects\staticobjects\Bridges\EoD_Bridge_Big\modmesh\eod_bridge_big.staticmesh
    # it has version 4 and inum and vnum in material
    #@unittest.skip('memory issues')
    def test_can_read_not_skinned_mesh_version_4(self):
        path_mesh = os.path.join(*['tests', 'samples', 'EoD_Bridge_Big', 'meshes', 'eod_bridge_big.staticmesh'])
        #vmesh = modmesh.LoadBF2Mesh(path_mesh)
        with open(path_mesh, 'rb') as meshfile:
            vmesh = modmesh.StdMesh()
            vmesh._read_materials(meshfile)
            
    @unittest.skip('i\o intensive, depends on local meshes...')
    def test_can_read_PR_modmesh_REPO(self):
        counter = 0
        for dir, dirnames, filenames in os.walk(os.path.join(bf2.Mod().root, 'objects')):
            for filename in filenames:
                ext = filename.split('.')[-1].lower()
                if ext[-4:] == 'mesh' and ext not in ['collisionmesh', 'skinnedmesh'] and 'test' not in dir:
                    counter += 1
                    try:
                        vmesh = modmesh.LoadBF2Mesh(os.path.join(bf2.Mod().root, dir, filename))
                    except struct.error:
                        print('Failed to load {}'.format(os.path.join(bf2.Mod().root, dir, filename)))
                        raise
            print(counter)
        #raise

class TestStdMeshWriting(unittest.TestCase):

    def setUp(self):
        self.path_object_std = os.path.join(*['tests', 'samples', 'evil_box', 'meshes', 'evil_box.staticmesh'])
        self.path_object_dest = os.path.join(*['tests', 'samples', 'evil_box_destroyable', 'meshes', 'evil_box_destroyable.staticmesh'])

        self.path_object_clone = os.path.join(*['tests', 'generated', 'write', 'evil_box_clone', 'meshes', 'evil_box_clone.staticmesh'])

    # disable when investigating results
    @classmethod
    def tearDownClass(cls):
        try:
            path_clear = os.path.join(*['tests', 'generated', 'write'])
            shutil.rmtree(path_clear, ignore_errors=True)
        except FileNotFoundError:
            print('Nothing to clean up')

    def test_can_write_header(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_header(self.path_object_clone)
        
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_head(meshfile)

        self.assertTrue(vmesh2.head.u1 == vmesh.head.u1)
        self.assertTrue(vmesh2.head.version == vmesh.head.version)
        self.assertTrue(vmesh2.head.u3 is vmesh.head.u3)
        self.assertTrue(vmesh2.head.u4 is vmesh.head.u4)
        self.assertTrue(vmesh2.head.u5 is vmesh.head.u5)

    def test_can_write_u1_bfp4f_version(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_u1_bfp4f_version(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_u1_bfp4f_version(meshfile)

        self.assertTrue(vmesh2.u1 == vmesh.u1)

    def test_can_write_geomnum_mesh_std(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_geomnum(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_geomnum(meshfile)

        self.assertTrue(vmesh2.geomnum == vmesh.geomnum)

    def test_can_write_geomnum_mesh_dest(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_dest)
        vmesh._write_geomnum(self.path_object_clone)
    
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_geomnum(meshfile)
            
        self.assertTrue(vmesh2.geomnum == vmesh.geomnum)

    def test_can_write_geom_table_mesh_std(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_geom_table(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_geom_table(meshfile)

        self.assertTrue(len(vmesh2.geoms) == len(vmesh.geoms))
        self.assertTrue(vmesh2.geoms[0].lodnum == vmesh.geoms[0].lodnum)

    def test_can_write_geom_table_mesh_dest(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_dest)
        vmesh._write_geom_table(self.path_object_clone)
        
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_geom_table(meshfile)

        self.assertTrue(len(vmesh2.geoms) == len(vmesh.geoms))
        self.assertTrue(vmesh2.geoms[0].lodnum == vmesh.geoms[0].lodnum)
        self.assertTrue(vmesh2.geoms[1].lodnum == vmesh.geoms[1].lodnum)

    def test_can_write_vertattribnum_mesh_std(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertattribnum(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_vertattribnum(meshfile)

        self.assertTrue(vmesh2.vertattribnum == vmesh.vertattribnum)

    def test_can_write_vertex_attribute_table(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertattrib_table(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_vertattrib_table(meshfile)

        for attrib_id, attrib in enumerate(vmesh.vertattrib):
            self.assertTrue(attrib == vmesh2.vertattrib[attrib_id])

    def test_can_write_vertformat(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertformat(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_vertformat(meshfile)

        self.assertTrue(vmesh2.vertformat == vmesh.vertformat)

    def test_can_write_vertstride(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertstride(self.path_object_clone)
    
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_vertstride(meshfile)

        self.assertTrue(vmesh2.vertstride == vmesh.vertstride)

    def test_can_write_vertnum(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertnum(self.path_object_clone)
    
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_vertnum(meshfile)

        self.assertTrue(vmesh2.vertnum == vmesh.vertnum)

    def test_can_write_vertex_block(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_vertex_block(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_vertex_block(meshfile)

        self.assertTrue(len(vmesh2.vertices) == len(vmesh2.vertices))

    def test_can_write_indexnum(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_indexnum(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_indexnum(meshfile)

        self.assertTrue(vmesh2.indexnum == vmesh.indexnum)

    def test_can_write_index_block(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_index_block(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_index_block(meshfile)

        self.assertTrue(len(vmesh2.index) == len(vmesh2.index))

    def test_can_write_u2(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_u2(self.path_object_clone)
        
        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_u2(meshfile)

        self.assertTrue(vmesh2.u2 == vmesh.u2)

    def test_can_write_nodes(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_nodes(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_nodes(meshfile)

        self.assertTrue(vmesh2.geoms[0].lods[0].min == vmesh.geoms[0].lods[0].min)
        self.assertTrue(vmesh2.geoms[0].lods[0].max == vmesh.geoms[0].lods[0].max)
        #self.assertTrue(vmesh.geoms[0].lods[0].pivot == (0.5, 1.0, 0.5)) # some old bundleds?
        self.assertTrue(vmesh2.geoms[0].lods[0].nodenum == vmesh.geoms[0].lods[0].nodenum)
        self.assertTrue(vmesh2.geoms[0].lods[0].nodes == vmesh.geoms[0].lods[0].nodes)

    def test_can_write_materials(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_materials(self.path_object_clone)

        with open(self.path_object_clone, 'rb') as meshfile:
            vmesh2 = modmesh.StdMesh()
            vmesh2._read_materials(meshfile)

        for geom_id, geom in enumerate(vmesh.geoms):
            for lod_id, lod in enumerate(geom.lods):
                self.assertTrue(lod.matnum == vmesh2.geoms[geom_id].lods[lod_id].matnum)
                #for material_id, material in enumerate(lod.materials):
                    #for key, value in material.__dict__.items():
                    #    print('"{:.10}" : {}'.format(key, value))
                    #for key, value in vmesh2.geoms[geom_id].lods[lod_id].materials[material_id].__dict__.items():
                    #    print('"{:.10}" : {}'.format(key, value))
                    #self.assertTrue(material == vmesh2.geoms[geom_id].lods[lod_id].materials[material_id])
                self.assertTrue(lod.polycount == vmesh2.geoms[geom_id].lods[lod_id].polycount)
    
    def test_verify_filedata_to_be_identical(self):
        vmesh = modmesh.LoadBF2Mesh(self.path_object_std)
        vmesh._write_materials(self.path_object_clone)
        
        self.assertTrue(filecmp.cmp(self.path_object_std, self.path_object_clone))

#@unittest.skip('testing failed mesh load')
class TestSamplesReading(unittest.TestCase):

    def setUp(self):
        self.path_object_std = self.path_object_std = os.path.join(*['tests', 'samples', 'evil_box', 'meshes', 'evil_box.samples'])

    def test_can_read_header(self):
        with open(self.path_object_std, 'rb') as samplefile:
            sample = modmesh.StdSample()
            sample._read_head(samplefile)

        self.assertTrue(sample.fourcc == b'SMP2')
        self.assertTrue(sample.width == 256)
        self.assertTrue(sample.height == 256)

    def test_can_read_smp_samples(self):
        with open(self.path_object_std, 'rb') as samplefile:
            sample = modmesh.StdSample()
            sample._read_data(samplefile)

        self.assertTrue(sample.datanum == sample.width * sample.height)
        self.assertTrue(len(sample.data) == sample.datanum)
        self.assertTrue(isinstance(sample.data[0], modmesh.smp_sample))

    def test_can_read_smp_faces(self):
        with open(self.path_object_std, 'rb') as samplefile:
            sample = modmesh.StdSample()
            sample._read_faces(samplefile)

        self.assertTrue(sample.facenum == 12)
        self.assertTrue(len(sample.faces) == sample.facenum)
        self.assertTrue(isinstance(sample.faces[0], modmesh.smp_face))
    
    def test_can_load_samplefile(self):
        sample = modmesh.LoadBF2Sample(self.path_object_std)
        self.assertTrue(isinstance(sample, modmesh.StdSample))

    def test_can_load_bf2_mesh_with_samples(self):
        meshpath = self.path_object_std.replace('.samples', '.staticmesh')
        vmesh = modmesh.LoadBF2Mesh(meshpath, loadSamples=True)
        self.assertTrue(isinstance(vmesh.geoms[0].lods[0].sample, modmesh.StdSample))
    

