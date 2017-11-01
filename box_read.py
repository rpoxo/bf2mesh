import os

import modmesh

def display_mesh_data(vmesh):
    for attrib in vmesh.vertattrib:
        usage = modmesh.D3DDECLUSAGE(attrib.usage).name
        offset = int(attrib.offset / vmesh.vertformat)
        vartype = modmesh.D3DDECLTYPE(attrib.vartype).name
        vlen = len(modmesh.D3DDECLTYPE(attrib.vartype))
        
        print('\n### {} {} ###'.format(usage, vartype))
        for i in range(vmesh.vertnum):
            vstart = offset + i * int(vmesh.vertstride / vmesh.vertformat)
            data = vmesh.vertices[vstart:vstart+vlen]

            print('[{}] [{}] {},'.format(i, vstart, tuple(data)))

    print('\n### INDICES ###\n')
    face_vid = 0
    for id_vertex in vmesh.index:
        face_vid += 1

        vstart = id_vertex * int(vmesh.vertstride / vmesh.vertformat)
        vdata = vmesh.vertices[vstart:vstart+3]
        print('[{}] {},'.format(id_vertex, tuple(vdata)))
        if face_vid == 3:
            face_vid = 0
            print('')

vmesh = modmesh.LoadBF2Mesh(os.getcwd() + '\\tests\\samples\\evil_box\\Meshes\\evil_box.staticmesh')
#vmesh = modmesh.LoadBF2Mesh(os.getcwd() + '/generated/generated_box/meshes/generated_box_edit.staticmesh')
#vmesh = modmesh.LoadBF2Mesh('C:\Program Files\Blender Foundation\Blender\generated\generated_box\meshes\generated_box.staticmesh')
#vmesh = modmesh.LoadBF2Mesh(os.getcwd() + '\\..\\..\\..\\..\\..\\objects\\vehicles\\land\\us_tnk_m1a2\\Meshes\\us_tnk_m1a2.bundledmesh')

display_mesh_data(vmesh)