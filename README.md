## A repo for various bf2 tools.
  
  
# mesh-merger
This is tool for merging bf2 staticmeshes into single one. Includes .staticmesh parser written in python3.  
  
In Project Reality mod we're often struggling with new maps being too heavy on staticobjects, and as old bf2 engine doesn't batch objects to make less drawcalls, we're ending up with huge numbers like 2500-3000 drawcalls on maps like Fallujah and Grozny. This places very specific requirements on clients hardware to have fast single threaded CPU.
  
``import mesher`` in your scripts to read bf2 staticmeshes. 
TODO : MUCH SHIT  
  
  
# lm_sizes
This is tool for generating lightmap sizes based on their samples sizes.
  
run script from any place under mod dir, grab output from stout  
```$ python lm_sizes.py > lm_sizes.log```