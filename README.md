BF2Mesh - Battlefield 2 mesh file parser, written in python3

This code documents how to parse mesh files of the DICE/EA games Battlefield 2,
Battlefield 2142, Battlefield Heroes, Battlefield Play4Free, which share the
same internal layout. These files typically have the extension ".StaticMesh",
".BundledMesh" or ".SkinnedMesh".

The code does not include rendering code or otherwise convert or output the data
to file.

For more information from original developer, see: http://www.bytehazard.com

## Simple Demo for skinned mesh merging

```python
import modmesh

# First read mesh files into memory
kits1 = modmesh.LoadBF2Mesh('cf_kits1.skinnedMesh')
kits2 = modmesh.LoadBF2Mesh('cf_kits2.skinnedMesh')

# then use merge_mesh method from VisMeshTransform class
# to append kits2 data into kits1
modmesh.VisMeshTransform(kits1).merge_mesh(kits2)

# save changes made in first mesh
kits1.save('cf_kits3.skinnedMesh')
```


## How to delete unnecessary geoms from mesh

```python
import modmesh

# load mesh file
kits = modmesh.LoadBF2Mesh('cf_kits1.skinnedMesh')

# specify geom id you need to delete
modmesh.VisMeshTransform(vmesh).delete_geom_id(3)

# save changes
kits1.save('cf_kits4.skinnedMesh')
```
