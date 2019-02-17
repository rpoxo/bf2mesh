import unittest
import os
import struct
import shutil

import bf2

import modcolmesh

class TestColMeshRead(unittest.TestCase):

    def setUp(self):
        self.path_colmesh = os.path.join(*['tests', 'samples', 'evil_box', 'meshes', 'evil_box.collisionmesh'])

    def test_can_read_header(self):
        with open(self.path_colmesh, 'rb') as meshfile:
            colmesh = modcolmesh.ColMesh()
            colmesh._read_header(meshfile)
            
        self.assertTrue(colmesh.u1 == 0)
        self.assertTrue(colmesh.version == 10)

    def test_can_read_geoms(self):
        with open(self.path_colmesh, 'rb') as meshfile:
            colmesh = modcolmesh.ColMesh()
            colmesh._read_geoms(meshfile)
            self.assertTrue(meshfile.tell() == 1511)
            
        self.assertTrue(len(colmesh.geoms) == colmesh.geomnum == 1)
        
        geom0 = colmesh.geoms[0]
        self.assertTrue(geom0.subgeomnum == 1)
        
        subgeom0 = geom0.subgeoms[0]
        self.assertTrue(subgeom0.lodnum == 3)
        
        lod0 = subgeom0.lods[0]
        lod1 = subgeom0.lods[1]
        lod2 = subgeom0.lods[2]
        self.assertTrue(lod0.coltype == 0)
        self.assertTrue(lod0.facenum == 12)
        self.assertTrue(lod0.u7 == 49)
        self.assertTrue(lod0.ynum == 3)
        self.assertTrue(lod0.znum == 12)
        self.assertTrue(lod0.anum == 36)

    def test_can_read_colmesh(self):
        colmesh = modcolmesh.ColMesh()
        colmesh.load(self.path_colmesh)
    
    # this is specific test for data in sample
    #@unittest.skip('test for sample data')
    def test_for_data(self):
        def __copy_from_export(copy_from, copy_to, objects):
            mod_path = bf2.Mod().root
            export_path = os.path.join(*copy_from)
            samples_path = os.path.join(*copy_to)

            for object_name in objects:
                exported_object_path = os.path.join(
                                        mod_path,
                                        export_path,
                                        object_name,
                                        'meshes',
                                        object_name + '.collisionmesh')
                samples_object_path = os.path.join(
                                        mod_path,
                                        samples_path,
                                        object_name,
                                        'meshes',
                                        object_name + '.collisionmesh')
                
                # raise the 
                shutil.copy(exported_object_path, samples_object_path)

        objects = [
            'evil_box',
            'evil_tri', 
            'evil_plane',
            'evil_plane_90',
            ]
        __copy_from_export(
            ['objects', 'staticobjects', 'test'],
            ['readme', 'assets', 'apps', 'python3', 'mesher', 'tests', 'samples'],
            objects)
        object_name = objects[2]
        path_samples = os.path.join('tests', 'samples')
        path_colmesh = os.path.join(path_samples, object_name, 'meshes', object_name+'.collisionmesh')

        colmesh = modcolmesh.ColMesh()
        colmesh.load(path_colmesh)
        print(path_colmesh)
        
        geom0 = colmesh.geoms[0]
        subgeom0 = geom0.subgeoms[0]
        lod0 = subgeom0.lods[0]
        
        for i in range(lod0.vertnum):
            print('vertex[{}]: {}'.format(i, lod0.vertices[i]))
            pass
        print('vertices({})\n'.format(lod0.vertnum))

        for i in range(lod0.facenum):
            print('face[{}]: {}'.format(i, lod0.faces[i]))
            pass
        print('facenum({})\n'.format(lod0.facenum))
        
        for i in range(lod0.ynum):
            print('ydata[{}]: {}'.format(i, lod0.ydata[i]))
            pass
        print('ynum({})\n'.format(lod0.ynum))

        for i in range(lod0.znum):
            value = lod0.zdata[i]
            face = lod0.faces[value]
            print('zdata[{}]: {}'.format(i, value))
            pass
        print('znum({})\n'.format(lod0.znum))
        
        for i in range(lod0.anum):
            vertex = lod0.vertices
            
            value = lod0.adata[i]
            face = lod0.faces[value]
            print('adata[{}]: {}'.format(i, value))
            pass
        print('anum({})\n'.format(lod0.anum))
        raise

    @unittest.skip('bad i\o intensive test, depends on local meshes...')
    def test_can_read_collisions_PR_REPO(self):
        counter = 0
        for dir, dirnames, filenames in os.walk(os.path.join(bf2.Mod().root, 'objects')):
            for filename in filenames:
                ext = filename.split('.')[-1].lower()
                if ext == 'collisionmesh' and 'test' not in dir:
                    counter += 1
                    filepath = os.path.join(bf2.Mod().root, dir, filename)
                    try:
                        colmesh = modcolmesh.ColMesh()
                        colmesh.load(filepath)
                        
                        for geom in colmesh.geoms:
                            for sub in geom.subgeoms:
                                for lod in sub.lods:
                                    if lod.facenum > 10 and lod.facenum < 30:
                                        print(filepath)
                                        print(lod.facenum)
                                        for face in lod.faces:
                                            print(face)
                                        for zdata in lod.zdata:
                                            print(zdata)
                                        raise
                    except struct.error:
                        print('Failed to load {} struct'.format(filepath))
                        #raise
                    except Exception as e:
                        print('Failed to load {}'.format(filepath))
                        print(e)
                        raise
        print(counter)
        raise
        
if __name__ == '__main__':
    unittest.main()
