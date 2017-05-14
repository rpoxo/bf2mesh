# mesh-merger
This is tool for merging bf2 staticmeshes into single one. Includes .staticmesh parser written in python3.  
  
In Project Reality mod we're often struggling with new maps being too heavy on staticobjects, and as old bf2 engine doesn't batch objects to make less drawcalls, we're ending up with huge numbers like 2500-3000 drawcalls on maps like Fallujah and Grozny. This places very specific requirements on clients hardware to have fast single threaded CPU.
  
``import mesher`` in your scripts to read bf2 staticmeshes.  