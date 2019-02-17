# bf2mesh - parser for Battlefield 2 mesh files written in python3

literally a badly rewritten code from bfmeshviewer by http://www.bytehazard.com

## Usage:
### How to change mesh order
```python
import bf2mesh
from bf2mesh.visiblemesh import VisibleMesh

# First read mesh files into memory
filename = 'cf_kits.skinnedMesh'
vmesh = VisibleMesh(filename)

# cf_kits skinnedmesh has 22 geoms
# new order will be
#   dropkit 7->16
#   tanker 13->15
#   pilot  14->17
order = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 16, 17, 13, 7, 14]
vmesh.change_geoms_order(order)

# export to file
vmesh.export(filename)
```
