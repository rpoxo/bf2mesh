BF2Mesh - Battlefield 2 mesh file parser, written in python3

This code documents how to parse mesh files of the DICE/EA games Battlefield 2,
Battlefield 2142, Battlefield Heroes, Battlefield Play4Free, which share the
same internal layout. These files typically have the extension ".StaticMesh",
".BundledMesh" or ".SkinnedMesh".

The code does not include rendering code or otherwise convert or output the data
to file.

For more information from original bfmesh parser developer, visit: http://www.bytehazard.com

## How to offset mesh geometry
```python
import modmesh
from modVec3 import Vec3

# First read mesh files into memory
vmesh = modmesh.LoadBF2Mesh('24m_1.staticmesh')

# calculate offset
# Example from fallujah_west GPO
#
#rem *** 24m_1 ***
#Object.create 24m_1
#Object.absolutePosition 491.567/24.653/495.454

offset = Vec3(491.567, 24.653, 495.454)

# translate mesh geometry
vmesh.translate(offset)

# save changes as new mesh
vmesh.save('24m_1_merged.staticmesh')
```

## How to rotate mesh
```python
import modmesh
from modVec3 import Vec3

# First read mesh files into memory
vmesh = modmesh.LoadBF2Mesh('evil_box.staticmesh')

# define rotation
rotation = (90.0, 0.0, 0.0)

# rotate mesh geometry
vmesh.rotate(rotation)

# save changes as new mesh
vmesh.save('evil_box_rotated.staticmesh')
```

## How to merge meshes  
* Only same objects now - i'm not taking diffirences in materials, geomtable for now...

```python
import modmesh
from modVec3 import Vec3

# First read mesh files into memory
vmesh1 = modmesh.LoadBF2Mesh('24m_1.staticmesh')
vmesh2 = modmesh.LoadBF2Mesh('24m_1.staticmesh')

# calculate offset
# Example from fallujah_west GPO
# ###
#rem *** 24m_1 ***
#Object.create 24m_1
#Object.absolutePosition 491.567/24.653/495.454
#Object.rotation 0.2/0.0/0.0
#
#rem *** 24m_1 ***
#Object.create 24m_1
#Object.absolutePosition 491.416/24.653/443.952
#Object.rotation 0.2/0.0/0.0
# ###

position1 = Vec3(491.567, 24.653, 495.454)
rotation1 = (0.2, 0.0, 0.0)

position2 = Vec3(491.416, 24.653, 443.974)
rotation2 = (0.2, 0.0, 0.0)

# apply rotations
vmesh1.rotate(rotation1)
vmesh2.rotate(rotation2)
# translate second mesh
vmesh2.translate(diff)
# merge with parent mesh
vmesh1.merge(vmesh2)

# save changes made in first mesh
kits1.save('cf_kits3.skinnedMesh')
```
