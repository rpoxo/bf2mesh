# #####
import os

import bf2
import mesher


test_object_std = os.path.join(*['objects',
                                 'staticobjects',
                                 'test',
                                 'evil_box1',
                                 'meshes',
                                 'evil_box1.staticmesh'])
test_object_merged = os.path.join(
    *['objects', 'staticobjects', 'test', 'evil_box5', 'meshes', 'evil_box5.staticmesh'])
test_object_generated = os.path.join(*['objects',
                                       'staticobjects',
                                       'test',
                                       'evil_box_generated',
                                       'meshes',
                                       'evil_box_generated.staticmesh'])
test_object_tris = os.path.join(*['objects',
                                  'staticobjects',
                                  'test',
                                  'evil_box8',
                                  'meshes',
                                  'evil_box8.staticmesh'])
test_object_poly = os.path.join(*['objects',
                                  'staticobjects',
                                  'test',
                                  'evil_box9',
                                  'meshes',
                                  'evil_box9.staticmesh'])
test_object_poly_merged = os.path.join(*['objects',
                                         'staticobjects',
                                         'test',
                                         'evil_box_2xplane',
                                         'meshes',
                                         'evil_box_2xplane.staticmesh'])

path_object_std = os.path.join(bf2.Mod().root, test_object_std)
path_object_merged = os.path.join(bf2.Mod().root, test_object_merged)
path_object_generated = os.path.join(bf2.Mod().root, test_object_generated)
path_object_tris = os.path.join(bf2.Mod().root, test_object_tris)
path_object_poly = os.path.join(bf2.Mod().root, test_object_poly)
path_object_poly_merged = os.path.join(bf2.Mod().root, test_object_poly_merged)


vmesh = mesher.LoadBF2Mesh(path_object_poly_merged)
print(vmesh.index)
for index, vertex in enumerate(vmesh.vertices_attributes):
    print(
        'merged[{}] {} {}'.format(
            index,
            vertex['position'],
            vertex['normal']))
vmesh = mesher.LoadBF2Mesh(path_object_generated)
print(vmesh.index)
for index, vertex in enumerate(vmesh.vertices_attributes):
    print(
        'merged[{}] {} {}'.format(
            index,
            vertex['position'],
            vertex['normal']))
