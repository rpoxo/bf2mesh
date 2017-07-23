import unittest
import os
import struct

import bf2
import meshes
import modmath

class Triangle:

    def __init__(self):
        self.vmesh = meshes.StdMesh()
        self._create_header(self.vmesh)
        self._create_u1_bfp4f_version(self.vmesh)
        self._create_geomnum(self.vmesh)
        self._create_geomtable(self.vmesh)
        self._create_vertattribnum(self.vmesh)
        self._create_vertattrib_table(self.vmesh)
        self._create_vertformat(self.vmesh)
        self._create_vertstride(self.vmesh)
        self._create_vertnum(self.vmesh)
        self._create_vertices(self.vmesh)
        self._create_index(self.vmesh)
        self._create_u2(self.vmesh)
        self._create_nodes(self.vmesh)
        self._create_materials(self.vmesh)
        

    def _create_header(self, vmesh):
        vmesh.head = meshes.bf2head()
        vmesh.head.u1 = 0
        vmesh.head.version = 11
        vmesh.head.u3 = 0
        vmesh.head.u4 = 0
        vmesh.head.u5 = 0

    def _create_u1_bfp4f_version(self, vmesh):
        vmesh.u1 = 0
    
    def _create_geomnum(self, vmesh):
        vmesh.geomnum = 1
        
    def _create_geomtable(self, vmesh):
        vmesh.geoms = [meshes.bf2geom() for i in range(vmesh.geomnum)]
        vmesh.geoms[0].lodnum = 1
        for geom in vmesh.geoms:
            for i in range(geom.lodnum):
                geom.lods = [meshes.bf2lod() for i in range(geom.lodnum)]

    def _create_vertattribnum(self, vmesh):
        vmesh.vertattribnum = 6 # +1 for unused? xD
    
    def _create_vertattrib_table(self, vmesh):
        dumb_array = [
            (0, 0, 2, 0), # used, offset=0, float3, position
            (0, 12, 2, 3), # used, offset=12\4, float3, normal
            (0, 24, 4, 2), # used, offset=24\4, d3dcolor, blend indice
            (0, 28, 1, 5), # used, offset=28\4, float2, uv1
            (0, 32, 2, 6), # used, offset=0, float3, tangent
            (255, 0, 17, 0), # not used, offset=0, unused, unused
            ]
        vmesh.vertattrib = [meshes.vertattrib() for i in range(vmesh.vertattribnum)]
        for i in range(vmesh.vertattribnum):
            vmesh.vertattrib[i].flag = dumb_array[i][0]
            vmesh.vertattrib[i].offset = dumb_array[i][1]
            vmesh.vertattrib[i].vartype = dumb_array[i][2]
            vmesh.vertattrib[i].usage = dumb_array[i][3]
            #print('{}: \n{}'.format(i, vmesh.vertattrib[i]))
    
    def _create_vertformat(self, vmesh):
        vmesh.vertformat = 4
    
    def _create_vertstride(self, vmesh):
        vmesh.vertstride = sum([modmath.d3dtypes_lenght[attrib.vartype]*vmesh.vertformat for attrib in vmesh.vertattrib])
    
    def _create_vertnum(self, vmesh):
        vmesh.vertnum = 3
    
    def _create_vertices(self, vmesh):
            positions = [
                (0.5, 0.0, 0.5), # right front
                (-0.5, 0.0, -0.5), # left back
                (-0.5, 0.0, 0.5), # left front
                ]
            normals = [
                (0.0, 1.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 1.0, 0.0),
                ]
            blendices = [
                (0.0,),
                (0.0,),
                (0.0,),
                ]
            uv1 = [
                (1.0, 0.0),
                (0.0, 1.0),
                (0.0, 0.0)
                ]
            tangents = [
                (1.0, 0.0, 0.0), # (0.9999999403953552, 0.0, 0.0)
                (1.0, 0.0, 0.0), # (0.9999999403953552, 0.0, 0.0)
                (1.0, 0.0, 0.0), # (0.9999999403953552, 0.0, 0.0)
                ]
            vertlist = []
            for i in range(3):
                vertlist.extend(positions[i])
                vertlist.extend(normals[i])
                vertlist.extend(blendices[i])
                vertlist.extend(uv1[i])
                vertlist.extend(tangents[i])
            vmesh.vertices = tuple(vertlist) 
    
    def _create_index(self, vmesh):
        vmesh.index = (0, 1, 2)
        vmesh.indexnum = len(vmesh.index)

    def _create_u2(self, vmesh):
        vmesh.u2 = 8
    
    def _create_nodes(self, vmesh):
        for geom in vmesh.geoms:
            for lod in geom.lods:
                lod.version = 11
                lod.min = (-0.5, 0.0, -0.5)
                lod.max = (0.5, 0.0, 0.5)
                #lod.pivot = None # already assigned to None for new meshes
                lod.nodenum = 1
                lod.nodes = [
                    1.0, 0.0, 0.0, 0.0,
                    0.0, 1.0, 0.0, 0.0,
                    0.0, 0.0, 1.0, 0.0,
                    0.0, 0.0, 0.0, 1.0] # no idea what is this shit in matrix4 ?
                lod.polycount = 0
                
    def _create_materials(self, vmesh):
        for geom in vmesh.geoms:
            for lod in geom.lods:
                lod.matnum = 1
                lod.materials = [meshes.bf2mat() for i in range(lod.matnum)]
                for material in lod.materials:
                    material.alphamode = 0
                    material.fxfile = b'StaticMesh.fx'
                    material.technique = b'Base'
                    material.mapnum = 1
                    material.maps = []
                    for i in range(material.mapnum):
                        material.maps.insert(i, b'default.dds')
                    material.vstart = 0
                    material.istart = 0
                    material.inum = 3
                    material.vnum = 3
                    material.u4 = 0
                    material.u5 = 0
                    material.nmin = (-0.5, 0.0, -0.5)
                    material.nmax = (0.5, 0.0, 0.5)
                    lod.polycount = lod.polycount + material.inum / 3

#@unittest.skip('temporary disabled until refactor')
class TestCreatePrimitive_Triangle(unittest.TestCase):

    def setUp(self):
        test_object_generated = os.path.join(*['objects', 'staticobjects', 'test', 'generated', 'generated_tri', 'meshes', 'generated_tri.staticmesh'])

        self.path_object_generated = os.path.join(bf2.Mod().root, test_object_generated)
        
    def test_reading_reference_tri_meshfile(self):
        vmesh_tri_path = os.path.join(bf2.Mod().root, (os.path.join(*['objects', 'staticobjects', 'test', 'evil_tri', 'meshes', 'evil_tri.staticmesh'])))
        vmesh_tri = meshes.LoadBF2Mesh(vmesh_tri_path)
        #print(vmesh_tri.vertices)
        #for id, data in enumerate(vmesh_tri.vertices):
        #    print('[{}] = {}'.format(id, data))
        #print(len(vmesh_tri.vertices))
        for i in range(vmesh_tri.vertnum):
            #print('\nvertex {}'.format(i))
            for attrib in vmesh_tri.vertattrib:
                usage = modmath.d3dusage[attrib.usage]
                offset = int(attrib.offset / vmesh_tri.vertformat) + int(i * vmesh_tri.vertstride / vmesh_tri.vertformat)
                vartype = attrib.vartype
                #print('{}({}) {}:'.format(usage, modmath.d3dtypes[vartype], str(attrib)))

                data = vmesh_tri.vertices[offset:offset+modmath.d3dtypes_lenght[vartype]]
                #print(' [{}+{}] {}'.format(offset, modmath.d3dtypes_lenght[vartype], data))

        for geomnum in range(vmesh_tri.geomnum):
            print('geom {} lodnum = {}'.format(geomnum, vmesh_tri.geoms[geomnum].lodnum))
            for lodnum in range(vmesh_tri.geoms[geomnum].lodnum):
                lod = vmesh_tri.geoms[geomnum].lods[lodnum]
                print('geom[{}].lod[{}].version = {}'.format(geomnum, lodnum, lod.version))
                print('geom[{}].lod[{}].min = {}'.format(geomnum, lodnum, lod.min))
                print('geom[{}].lod[{}].max = {}'.format(geomnum, lodnum, lod.max))
                print('geom[{}].lod[{}].pivot = {}'.format(geomnum, lodnum, lod.pivot))
                print('geom[{}].lod[{}].nodenum = {}'.format(geomnum, lodnum, lod.nodenum))
                print('geom[{}].lod[{}].nodes = {}'.format(geomnum, lodnum, lod.nodes))
                print('geom[{}].lod[{}].polycount = {}'.format(geomnum, lodnum, lod.polycount))
                print('geom[{}].lod[{}].matnum = {}'.format(geomnum, lodnum, lod.matnum))
                for matid, material in enumerate(lod.materials):
                    print('geom[{}].lod[{}].materials[{}].alphamode = {}'.format(geomnum, lodnum, matid, material.alphamode))
                    print('geom[{}].lod[{}].materials[{}].fxfile = {}'.format(geomnum, lodnum, matid, material.fxfile))
                    print('geom[{}].lod[{}].materials[{}].technique = {}'.format(geomnum, lodnum, matid, material.technique))
                    print('geom[{}].lod[{}].materials[{}].mapnum = {}'.format(geomnum, lodnum, matid, material.mapnum))
                    for mapid, map in enumerate(material.maps):
                        print('geom[{}].lod[{}].materials[{}].maps[{}] = {}'.format(geomnum, lodnum, matid, mapid, map))
                    print('geom[{}].lod[{}].materials[{}].vstart = {}'.format(geomnum, lodnum, matid, material.vstart))
                    print('geom[{}].lod[{}].materials[{}].istart = {}'.format(geomnum, lodnum, matid, material.istart))
                    print('geom[{}].lod[{}].materials[{}].inum = {}'.format(geomnum, lodnum, matid, material.inum))
                    print('geom[{}].lod[{}].materials[{}].vnum = {}'.format(geomnum, lodnum, matid, material.vnum))
                    print('geom[{}].lod[{}].materials[{}].u4 = {}'.format(geomnum, lodnum, matid, material.u4))
                    print('geom[{}].lod[{}].materials[{}].u5 = {}'.format(geomnum, lodnum, matid, material.u5))
                    print('geom[{}].lod[{}].materials[{}].nmin = {}'.format(geomnum, lodnum, matid, material.nmin))
                    print('geom[{}].lod[{}].materials[{}].nmax = {}'.format(geomnum, lodnum, matid, material.nmax))

        #raise

    def test_can_generate_valid_tri_meshfile(self):
        tri = Triangle()
        trimesh = tri.vmesh
        trimesh.write_file_data(self.path_object_generated)

        vmesh = meshes.LoadBF2Mesh(self.path_object_generated)
    
