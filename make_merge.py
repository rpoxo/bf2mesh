import os

import bf2
import mesher


def get_vertex_copy_with_offset(vmesh, offset): # should be a object method actually
    new_vertices_attributes = []
    for vertice in vmesh.vertices_attributes:
        vertice_clone = dict(vertice)
        new_position_x = vertice_clone['position'][0] + float(offset)
        new_position = (new_position_x, vertice_clone['position'][1], vertice_clone['position'][2])
        vertice_clone['position'] = new_position
        new_vertices_attributes.append(vertice_clone)
    #for index, new_vert in enumerate(new_vertices_attributes):
    #    print('new[{}] {} {}'.format(index+vmesh.indexnum, new_vert['position'], new_vert['normal']))
    # returning correct list
    return new_vertices_attributes

def is_vertex_similar(vert1, vert2):
    for attribute in vert1.keys():
        if vert1[attribute] != vert2[attribute]:# and attribute != 'position':
            return False
    return True

def get_filtered_indices(vmesh):
    new_vbo = []
    new_indices = []
    for index, vertex in enumerate(vmesh.vertices_attributes):
        for similar_vertex in vmesh.vertices_attributes:
            if vertex['position'] == similar_vertex['position']:
                if is_vertex_similar(vertex, similar_vertex):
                    is_selected = False
                    for selected_vertex in new_vbo:
                        if is_vertex_similar(vertex, selected_vertex) and vertex['position'] == selected_vertex['position']:
                            is_selected = True
                            break
                    
                    if not is_selected:
                        new_vbo.append(vertex)
                        new_indices.append(index)
    
    for vert in new_vbo:
        print('vert: {}'.format(vert['position']))
    print(new_indices)
    print(len(new_indices))
    return new_indices



test_object_std = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box', 'meshes', 'evil_box.staticmesh'])
test_object_two_lods = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box3', 'meshes', 'evil_box3.staticmesh'])
test_object_merged = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box5', 'meshes', 'evil_box5.staticmesh'])
test_object_generated = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box_generated', 'meshes', 'evil_box_generated.staticmesh'])
test_object_tri = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box8', 'meshes', 'evil_box8.staticmesh'])
test_object_poly = os.path.join(*['objects', 'staticobjects', 'test', 'evil_box9', 'meshes', 'evil_box9.staticmesh'])

path_object_std = os.path.join(bf2.Mod().root, test_object_std)
path_object_two_lods = os.path.join(bf2.Mod().root, test_object_two_lods)
path_object_merged = os.path.join(bf2.Mod().root, test_object_merged)
path_object_generated = os.path.join(bf2.Mod().root, test_object_generated)
path_object_tri = os.path.join(bf2.Mod().root, test_object_tri)
path_object_poly = os.path.join(bf2.Mod().root, test_object_poly)

path_object_container = os.path.join(bf2.Mod().root, os.path.join(*['objects', 'staticobjects', 'pr', 'containers', 'container', 'meshes', 'container.staticmesh']))
path_object_toilet = os.path.join(bf2.Mod().root, os.path.join(*['objects', 'staticobjects', 'pr', 'toilet', 'meshes', 'toilet.staticmesh']))

vmesh_std = mesher.LoadBF2Mesh(path_object_two_lods)
#for index, vert in enumerate(vmesh_std.vertices_attributes):
    #print(index)
# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================
old_vertnum = vmesh_std.vertnum
for index, new_vertex in enumerate(get_vertex_copy_with_offset(vmesh_std, 1.0)):
    print('new[{}] {} {}'.format(index+vmesh_std.indexnum, new_vertex['position'], new_vertex['normal']))
    vmesh_std.vertices_attributes.append(new_vertex)


vmesh_std._write_vertices_attributes()

for index, vertex in enumerate(vmesh_std.vertices_attributes):
    print('write[{}] {} {}'.format(index, vertex['position'], vertex['normal']))

# correcting vertnum
vmesh_std.vertnum = len(vmesh_std.vertices_attributes)

# correcting boundaries
#bounds = list(vmesh_std.geoms[0].lod[0].max)
#vmesh_std.geoms[0].lod[0].max = tuple([bounds[0] + offset, bounds[1], bounds[2]])

# correcting index 
#new_index = (22, 23, 20, 20, 21, 22, 18, 19, 16, 16, 17, 18, 24, 15, 12, 12, 13, 24, 10, 11, 8, 8, 9, 10, 6, 7, 4, 4, 5, 6, 2, 3, 0, 0, 1, 2)
new_indices = list(vmesh_std.index)
print(vmesh_std.index)
for index in vmesh_std.index:
    new_index = index+old_vertnum
    new_indices.append(new_index)
print('len(vmesh_std.index) = {}'.format(len(vmesh_std.index)))
#for index, vertex in enumerate(vmesh_std.vertices_attributes):
#    new_index.append(index)

vmesh_std.index = tuple(new_indices)
#test_indices = (1, 0, 3, 0, 1, 2, 3, 4, 7, 4, 3, 0)
#vmesh_std.index = test_indices
print(vmesh_std.index)
print('len(vmesh_std.index) = {}'.format(len(vmesh_std.index)))
vmesh_std.indexnum = len(vmesh_std.index)

# correcting material inum vnum
print('vmesh_std.geoms[0].lod[0].mat[0].inum = {}'.format(vmesh_std.geoms[0].lod[0].mat[0].inum))
print('vmesh_std.geoms[0].lod[0].mat[0].vnum = {}'.format(vmesh_std.geoms[0].lod[0].mat[0].vnum))
new_inum_per_mat = int(vmesh_std.indexnum / 2)
new_vnum_per_mat = int(vmesh_std.vertnum / 2)
lod1_istart = int(vmesh_std.indexnum / 4)
lod1_vstart = int(vmesh_std.vertnum / 4)
vmesh_std.geoms[0].lod[0].mat[0].inum = new_inum_per_mat * 2 # seems to be .indexnum
vmesh_std.geoms[0].lod[0].mat[0].vnum = new_vnum_per_mat * 2# == len(vertices)
vmesh_std.geoms[0].lod[1].mat[0].istart = lod1_istart # seems to be .indexnum
vmesh_std.geoms[0].lod[1].mat[0].vstart = lod1_vstart # == len(vertices)
vmesh_std.geoms[0].lod[1].mat[0].inum = new_inum_per_mat # seems to be .indexnum
vmesh_std.geoms[0].lod[1].mat[0].vnum = new_vnum_per_mat # == len(vertices)
print('vmesh_std.geoms[0].lod[0].mat[0].inum = {}'.format(vmesh_std.geoms[0].lod[0].mat[0].inum))
print('vmesh_std.geoms[0].lod[0].mat[0].vnum = {}'.format(vmesh_std.geoms[0].lod[0].mat[0].vnum))

#vmesh_std.polycount = vmesh_std.indexnum / 3



# ============================================================================
# ============================================================================
# ============================================================================
# ============================================================================
vmesh_std.write_file_data(path_object_generated)

# testing load
vmesh_std = mesher.LoadBF2Mesh(path_object_generated)