import os

import modmesh
def copy_geom_table(vmesh1, vmesh2):
    for id_geom, geom in enumerate(vmesh2.geoms):
        vmesh1.geoms.append(geom)
        for id_lod, lod in enumerate(vmesh1.geoms[id_geom+vmesh1.geomnum].lods):
            for id_mat, material in enumerate(lod.materials):
                vstart = int(material.vstart * (vmesh1.vertstride / vmesh1.vertformat))
                vnum = int(material.vnum * (vmesh1.vertstride / vmesh1.vertformat))
                vmesh1.vertices.extend(vmesh2.vertices[vstart:vstart+vnum])
                material.vstart += int(vmesh1.vertnum)
                for index in vmesh2.index[material.istart:material.istart+material.inum]:
                    vmesh1.index.append(index)
                material.istart += vmesh1.indexnum
    vmesh1.geomnum = len(vmesh1.geoms)
    vmesh1.vertnum = int(len(vmesh1.vertices) / (vmesh1.vertstride / vmesh1.vertformat))
    vmesh1.indexnum = len(vmesh1.index)


def main():
    vmesh = modmesh.LoadBF2Mesh('ch_kits.skinnedmesh')
    
    order = [0,1,2,3,4,5,6,7,9,8,10,11,12,13,14,15,16]
    modmesh.VisMeshTransform(vmesh).order_geoms_by(order)

    vmesh.save('./ch_kits2.skinnedmesh')
    

if __name__ == '__main__':
    main()