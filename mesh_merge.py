import os

import modmesh
        
def display_lods_data(vmesh1):
    #vnum = sum([sum([sum([material.vnum for material in lod.materials]) for lod in geom.lods]) for geom in vmesh1.geoms])
    #print('index len = {}'.format(len(vmesh1.index)))
    for id_geom, geom in enumerate(vmesh1.geoms):
        for id_lod, lod in enumerate(geom.lods):
            max_index = 10000
            for id_mat, material in enumerate(lod.materials):
                print('geom{} lod{} material[{}].vnum = {} + {}'.format(id_geom, id_lod, id_mat, material.vstart, material.vnum))
                print('geom{} lod{} material[{}].inum = {} + {}'.format(id_geom, id_lod, id_mat, material.istart, material.inum))


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
    vmesh = modmesh.LoadBF2Mesh('tests\\samples\\kits\\cf\\Meshes\\cf_kits1.skinnedMesh')
    vmesh2 = modmesh.LoadBF2Mesh('tests\\samples\\kits\\cf\\Meshes\\cf_kits2.skinnedMesh')
    
    copy_geom_table(vmesh, vmesh2)
    # cleanup
    #print(vmesh.geoms[24].lods[0].materials[0].vstart)
    modmesh.VisMeshTransform(vmesh).delete_geom_id(24)
    modmesh.VisMeshTransform(vmesh).delete_geom_id(23)
    modmesh.VisMeshTransform(vmesh).delete_geom_id(22)
    modmesh.VisMeshTransform(vmesh).delete_geom_id(14)
    modmesh.VisMeshTransform(vmesh).delete_geom_id(13)
    modmesh.VisMeshTransform(vmesh).delete_geom_id(8)
    modmesh.VisMeshTransform(vmesh).delete_geom_id(7)

    vmesh.save('tests\\samples\\kits\\cf\\Meshes\\cf_kits3.skinnedMesh')
    

if __name__ == '__main__':
    main()