import os

import modmesh

def print_vertex_data(vmesh, vid, vattribute):
    for attrib_id, attrib in enumerate(vmesh.vertattrib):
        usage = modmesh.modmath.d3dusage[attrib.usage]
        offset = int(attrib.offset / vmesh.vertformat)
        vartype = modmesh.modmath.d3dtypes[attrib.vartype]
        vlen = modmesh.modmath.d3dtypes_lenght[attrib.vartype]
        
        if usage == vattribute:
            vstart = offset + vid * int(vmesh.vertstride / vmesh.vertformat)
            vdata = vmesh.vertices[vstart:vstart+vlen]
            print('[{}]{} = {}'.format(vid, vattribute, vdata))

def remove_vertice_id(vmesh, id):
    vmesh.vertices = list(vmesh.vertices)

    for vertid in range(vmesh.vertnum):
        if vertid == 24:
            vsize = int(vmesh.vertstride / vmesh.vertformat)
            vstart = vertid * vsize
            print('removing {}:{} from vertices'.format(vstart, vstart+vsize))
            del vmesh.vertices[vstart:vstart+vsize]

    
    vmesh.vertnum = int(len(vmesh.vertices) / int(vmesh.vertstride / vmesh.vertformat))
    print('new .vertnum = {}'.format(vmesh.vertnum))
    

def replace_index_id(vmesh, id_original, id_replace):
    # fix for index 24 --> 14
    vmesh.index = list(vmesh.index)
    for i, id_vertex in enumerate(vmesh.index):
        if id_vertex == 24:
            vmesh.index[i] = 14

def remove_attribute(vmesh, attrib_to_remove):
    print('start size vmesh.vertices = {}'.format(len(vmesh.vertices)))
    vsize = int(vmesh.vertstride / vmesh.vertformat)
    
    offset_attrib = 0
    attrib_id_to_remove = 0
    total_data_removed = 0

    for attrib_id, attrib in enumerate(vmesh.vertattrib):
        usage = modmesh.modmath.d3dusage[attrib.usage]
        offset = int(attrib.offset / vmesh.vertformat)
        vartype = modmesh.modmath.d3dtypes[attrib.vartype]
        vlen = modmesh.modmath.d3dtypes_lenght[attrib.vartype]
        
        if usage == attrib_to_remove:
            print('REMOVING DATA for {}'.format(usage))
            offset_attrib = vlen * vmesh.vertformat
            attrib_id_to_remove = attrib_id

            for vertid in range(vmesh.vertnum-1, -1, -1):
                vstart = offset + vertid * vsize
                total_data_removed += vlen
                print('removing [{}]{}:{} from vertices, {} removed total, current len = {}'.format(vertid, vstart, vstart+vlen, total_data_removed, len(vmesh.vertices)))
                del vmesh.vertices[vstart:vstart+vlen]

        if offset_attrib != 0 and offset != 0:
            new_attrib_offset = attrib.offset - offset_attrib
            print('MOVING {} offset from {} to {} by {} bytes'.format(usage, attrib.offset, new_attrib_offset, offset_attrib))
            attrib.offset = new_attrib_offset


    # remove attribute from table
    if attrib_id_to_remove !=0:
        # fix vertstride
        reduce_stride_by = modmesh.modmath.d3dtypes_lenght[vmesh.vertattrib[attrib_id_to_remove].vartype] * vmesh.vertformat
        print('REDUCING STRIDE from {} to {} by {} bytes'.format(vmesh.vertstride, vmesh.vertstride - reduce_stride_by, reduce_stride_by))
        vmesh.vertstride = vmesh.vertstride - reduce_stride_by
        
        del vmesh.vertattrib[attrib_id_to_remove]

        # fix attrib table len
        vmesh.vertattribnum = len(vmesh.vertattrib)
        print('vmesh.vertattribnum = {}'.format(vmesh.vertattribnum))
        print('new vertices array len = {} after {} removed'.format(len(vmesh.vertices), total_data_removed))

        
        
def rename_texture(vmesh, geom, lod, material, map, path):
    vmesh.geoms[geom].lods[lod].materials[material].maps[map] = bytes(path, 'ascii')
    

def edit_vertex(vmesh, vid, vattribute, vdata):
    for attrib_id, attrib in enumerate(vmesh.vertattrib):
        usage = modmesh.modmath.d3dusage[attrib.usage]
        offset = int(attrib.offset / vmesh.vertformat)
        vartype = modmesh.modmath.d3dtypes[attrib.vartype]
        vlen = modmesh.modmath.d3dtypes_lenght[attrib.vartype]
        
        if usage == vattribute:
            print('SETTING DATA for v[{}] {}'.format(vid, vattribute))
            for vertid in range(vmesh.vertnum-1, -1, -1):
                vstart = offset + vertid * int(vmesh.vertstride / vmesh.vertformat)
                if vertid == vid:
                    for i, data in enumerate(vdata):
                        vmesh.vertices[vstart+i] = data
                        
def main():
    # ############################################################################ #
    # box exported from 3dsmax9 have weird additional vertex
    # for comparison with blender export data i need to remove it, aswell as remove addional UV maps that isn't used
    vmesh = modmesh.LoadBF2Mesh(os.getcwd() + '\\tests\\samples\\evil_box\\Meshes\\evil_box.staticmesh')
    print_vertex_data(vmesh, 24, 'UV1')

    remove_vertice_id(vmesh, 24)
    replace_index_id(vmesh, 24, 14)
    remove_attribute(vmesh, 'UV2')
    remove_attribute(vmesh, 'UV3')
    remove_attribute(vmesh, 'UV4')
    #rename_texture(vmesh, geom=0, lod=0, material=0, map=0, path='readme/assets/apps/python3/mesher/tests/samples/evil_box/textures/evil_box_c.dds')
    edit_vertex(vmesh, 14, 'UV1', (0.5, 1.0))

    vmesh.save('generated/generated_box/meshes/generated_box_edit.staticmesh')

if __name__ == "__main__":
    main()