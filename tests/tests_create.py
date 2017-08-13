import unittest
import os
import struct

import mock_mesh

import bf2
import modmesh
import modmath

@unittest.skip('temporary disabled until refactor')
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
        tri = mock_mesh.Triangle()
        trimesh = tri.vmesh
        trimesh.write_file_data(self.path_object_generated)

        vmesh = meshes.LoadBF2Mesh(self.path_object_generated)
    
