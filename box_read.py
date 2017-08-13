import os

import modmesh

vmesh = modmesh.LoadBF2Mesh(os.getcwd() + '\\evil_box\\Meshes\\evil_box.staticmesh')

vmesh.vertices = list(vmesh.vertices)
for attrib_id, attrib in enumerate(vmesh.vertattrib):
    usage = modmesh.modmath.d3dusage[attrib.usage]
    offset = int(attrib.offset / vmesh.vertformat)
    vartype = modmesh.modmath.d3dtypes[attrib.vartype]
    vnum = modmesh.modmath.d3dtypes_lenght[attrib.vartype]

    if usage == 'POSITION' and vartype != 'UNUSED':
        print('VERTICES')
        for i in range(vmesh.vertnum):
            vstart = offset + i * int(vmesh.vertstride / vmesh.vertformat)
            data = vmesh.vertices[vstart:vstart+vnum]
            #print('[{}] [{}({})] = {}'.format(i, usage, vartype, data))
            print('[{}] {},'.format(i, tuple(data)))

    if usage == 'NORMAL' and vartype != 'UNUSED':
        print('NORMALS')
        for i in range(vmesh.vertnum):
            vstart = offset + i * int(vmesh.vertstride / vmesh.vertformat)
            data = vmesh.vertices[vstart:vstart+vnum]
            #print('[{}] [{}({})] = {}'.format(i, usage, vartype, data))
            print('{},'.format(tuple(data)))

            #for id, item in enumerate(position_offset):
            #    vmesh.vertices[vstart+id] += item

            #data = vmesh.vertices[vstart:vstart+vnum]
            #print('[{}] [{}({})] = {}'.format(i, usage, vartype, data))

for id_vertex in vmesh.index:
    print('{},'.format(id_vertex))