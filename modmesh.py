import modmath

def offset_vertices(vmesh, position_offset):
    vmesh.vertices = list(vmesh.vertices)
    for attrib_id, attrib in enumerate(vmesh.vertattrib):
        usage = modmath.d3dusage[attrib.usage]
        offset = int(attrib.offset / vmesh.vertformat)
        vartype = modmath.d3dtypes[attrib.vartype]
        vnum = modmath.d3dtypes_lenght[attrib.vartype]

        if usage == 'POSITION' and vartype != 'UNUSED':
            for i in range(vmesh.vertnum):
                vstart = offset + i * int(vmesh.vertstride / vmesh.vertformat)
                #data = vmesh.vertices[vstart:vstart+vnum]
                #print('[{}] [{}({})] = {}'.format(i, usage, vartype, data))

                for id, item in enumerate(position_offset):
                    vmesh.vertices[vstart+id] += item

                #data = vmesh.vertices[vstart:vstart+vnum]
                #print('[{}] [{}({})] = {}'.format(i, usage, vartype, data))

def offset_UV1(vmesh, uv1_offset):
    vmesh.vertices = list(vmesh.vertices)
    for attrib_id, attrib in enumerate(vmesh.vertattrib):
        usage = modmath.d3dusage[attrib.usage]
        offset = int(attrib.offset / vmesh.vertformat)
        vartype = modmath.d3dtypes[attrib.vartype]
        vnum = modmath.d3dtypes_lenght[attrib.vartype]

        if usage == 'UV1' and vartype != 'UNUSED':
            for i in range(vmesh.vertnum):
                vstart = offset + i * int(vmesh.vertstride / vmesh.vertformat)
                #data = vmesh.vertices[vstart:vstart+vnum]
                #print('[{}] [{}({})] = {}'.format(i, usage, vartype, data))

                for id, item in enumerate(uv1_offset):
                    vmesh.vertices[vstart+id] += item

                #data = vmesh.vertices[vstart:vstart+vnum]
                #print('[{}] [{}({})] = {}'.format(i, usage, vartype, data))
