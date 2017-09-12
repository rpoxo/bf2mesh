import bf2
import modmesh
import modmath

class Triangle:

    def __init__(self):
        self.vmesh = modmesh.StdMesh()
        self._create_header(self.vmesh)
        self._create_u1_bfp4f_version(self.vmesh)
        self._create_geomnum(self.vmesh)
        self._create_geomtable(self.vmesh)
        self._create_vertattribnum(self.vmesh)
        self._create_vertattrib_table(self.vmesh)
        self._create_vertformat(self.vmesh)
        self._create_vertstride(self.vmesh)
        self._create_vertnum(self.vmesh)
        self._create_vertices(self.vmesh)
        self._create_index(self.vmesh)
        self._create_u2(self.vmesh)
        self._create_nodes(self.vmesh)
        self._create_materials(self.vmesh)
        

    def _create_header(self, vmesh):
        vmesh.head = modmesh.bf2head()
        vmesh.head.u1 = 0
        vmesh.head.version = 11
        vmesh.head.u3 = 0
        vmesh.head.u4 = 0
        vmesh.head.u5 = 0

    def _create_u1_bfp4f_version(self, vmesh):
        vmesh.u1 = 0
    
    def _create_geomnum(self, vmesh):
        vmesh.geomnum = 1
        
    def _create_geomtable(self, vmesh):
        vmesh.geoms = [modmesh.bf2geom() for i in range(vmesh.geomnum)]
        vmesh.geoms[0].lodnum = 1
        for geom in vmesh.geoms:
            for i in range(geom.lodnum):
                geom.lods = [modmesh.bf2lod() for i in range(geom.lodnum)]

    def _create_vertattribnum(self, vmesh):
        vmesh.vertattribnum = 6 # +1 for unused? xD
    
    def _create_vertattrib_table(self, vmesh):
        dumb_array = [
            (0, 0, 2, 0), # used, offset=0, float3, position
            (0, 12, 2, 3), # used, offset=12\4, float3, normal
            (0, 24, 4, 2), # used, offset=24\4, d3dcolor, blend indice
            (0, 28, 1, 5), # used, offset=28\4, float2, uv1
            (0, 32, 2, 6), # used, offset=0, float3, tangent
            (255, 0, 17, 0), # not used, offset=0, unused, unused
            ]
        vmesh.vertattrib = [modmesh.vertattrib() for i in range(vmesh.vertattribnum)]
        for i in range(vmesh.vertattribnum):
            vmesh.vertattrib[i].flag = dumb_array[i][0]
            vmesh.vertattrib[i].offset = dumb_array[i][1]
            vmesh.vertattrib[i].vartype = dumb_array[i][2]
            vmesh.vertattrib[i].usage = dumb_array[i][3]
            #print('{}: \n{}'.format(i, vmesh.vertattrib[i]))
    
    def _create_vertformat(self, vmesh):
        vmesh.vertformat = 4
    
    def _create_vertstride(self, vmesh):
        vmesh.vertstride = sum([modmath.d3dtypes_lenght[attrib.vartype]*vmesh.vertformat for attrib in vmesh.vertattrib])
    
    def _create_vertnum(self, vmesh):
        vmesh.vertnum = 3
    
    def _create_vertices(self, vmesh):
            positions = [
                (0.5, 0.0, 0.5), # right front
                (-0.5, 0.0, -0.5), # left back
                (-0.5, 0.0, 0.5), # left front
                ]
            normals = [
                (0.0, 1.0, 0.0),
                (0.0, 1.0, 0.0),
                (0.0, 1.0, 0.0),
                ]
            blendices = [
                (0.0,),
                (0.0,),
                (0.0,),
                ]
            uv1 = [
                (1.0, 0.0),
                (0.0, 1.0),
                (0.0, 0.0)
                ]
            tangents = [
                (1.0, 0.0, 0.0), # (0.9999999403953552, 0.0, 0.0)
                (1.0, 0.0, 0.0), # (0.9999999403953552, 0.0, 0.0)
                (1.0, 0.0, 0.0), # (0.9999999403953552, 0.0, 0.0)
                ]
            vertlist = []
            for i in range(3):
                vertlist.extend(positions[i])
                vertlist.extend(normals[i])
                vertlist.extend(blendices[i])
                vertlist.extend(uv1[i])
                vertlist.extend(tangents[i])
            vmesh.vertices = tuple(vertlist) 
    
    def _create_index(self, vmesh):
        vmesh.index = (0, 1, 2)
        vmesh.indexnum = len(vmesh.index)

    def _create_u2(self, vmesh):
        vmesh.u2 = 8
    
    def _create_nodes(self, vmesh):
        for geom in vmesh.geoms:
            for lod in geom.lods:
                lod.version = 11
                lod.min = (-0.5, 0.0, -0.5)
                lod.max = (0.5, 0.0, 0.5)
                #lod.pivot = None # already assigned to None for new modmesh
                lod.nodenum = 1
                lod.nodes = [
                    1.0, 0.0, 0.0, 0.0,
                    0.0, 1.0, 0.0, 0.0,
                    0.0, 0.0, 1.0, 0.0,
                    0.0, 0.0, 0.0, 1.0] # no idea what is this shit in matrix4 ?
                lod.polycount = 0
                
    def _create_materials(self, vmesh):
        for geom in vmesh.geoms:
            for lod in geom.lods:
                lod.matnum = 20
                lod.materials = [modmesh.bf2mat() for i in range(lod.matnum)]
                for matid, material in enumerate(lod.materials):
                    material.alphamode = 0
                    material.fxfile = b'StaticMesh.fx'
                    material.technique = b'Base'
                    material.mapnum = 1
                    material.maps = []
                    for i in range(material.mapnum):
                        material.maps.insert(i, b'objects/staticobjects/test/evil_box/textures/evil_box_c.dds')
                    material.vstart = 0
                    material.istart = 0
                    material.inum = 3
                    material.vnum = 3
                    material.u4 = 0
                    material.u5 = 0
                    material.nmin = (-0.5, 0.0, -0.5)
                    material.nmax = (0.5, 0.0, 0.5)
                    lod.polycount = lod.polycount + material.inum / 3

class Plane:

    def __init__(self):
        self.vmesh = modmesh.StdMesh()
        self._create_header(self.vmesh)
        self._create_u1_bfp4f_version(self.vmesh)
        self._create_geomnum(self.vmesh)
        self._create_geomtable(self.vmesh)
        self._create_vertattribnum(self.vmesh)
        self._create_vertattrib_table(self.vmesh)
        self._create_vertformat(self.vmesh)
        self._create_vertstride(self.vmesh)
        self._create_vertnum(self.vmesh)
        self._create_vertices(self.vmesh)
        self._create_index(self.vmesh)
        self._create_u2(self.vmesh)
        self._create_nodes(self.vmesh)
        self._create_materials(self.vmesh)
        

    def _create_header(self, vmesh):
        vmesh.head = modmesh.bf2head()
        vmesh.head.u1 = 0
        vmesh.head.version = 11
        vmesh.head.u3 = 0
        vmesh.head.u4 = 0
        vmesh.head.u5 = 0

    def _create_u1_bfp4f_version(self, vmesh):
        vmesh.u1 = 0
    
    def _create_geomnum(self, vmesh):
        vmesh.geomnum = 1
        
    def _create_geomtable(self, vmesh):
        vmesh.geoms = [modmesh.bf2geom() for i in range(vmesh.geomnum)]
        vmesh.geoms[0].lodnum = 1
        for geom in vmesh.geoms:
            for i in range(geom.lodnum):
                geom.lods = [modmesh.bf2lod() for i in range(geom.lodnum)]

    def _create_vertattribnum(self, vmesh):
        vmesh.vertattribnum = 6 # +1 for unused? xD
    
    def _create_vertattrib_table(self, vmesh):
        dumb_array = [
            (0, 0, 2, 0), # used, offset=0, float3, position
            (0, 12, 2, 3), # used, offset=12\4, float3, normal
            (0, 24, 4, 2), # used, offset=24\4, d3dcolor, blend indice
            (0, 28, 1, 5), # used, offset=28\4, float2, uv1
            (0, 32, 2, 6), # used, offset=0, float3, tangent
            (255, 0, 17, 0), # not used, offset=0, unused, unused
            ]
        vmesh.vertattrib = [modmesh.vertattrib() for i in range(vmesh.vertattribnum)]
        for i in range(vmesh.vertattribnum):
            vmesh.vertattrib[i].flag = dumb_array[i][0]
            vmesh.vertattrib[i].offset = dumb_array[i][1]
            vmesh.vertattrib[i].vartype = dumb_array[i][2]
            vmesh.vertattrib[i].usage = dumb_array[i][3]
            #print('{}: \n{}'.format(i, vmesh.vertattrib[i]))
    
    def _create_vertformat(self, vmesh):
        vmesh.vertformat = 4
    
    def _create_vertstride(self, vmesh):
        vmesh.vertstride = sum([modmath.d3dtypes_lenght[attrib.vartype]*vmesh.vertformat for attrib in vmesh.vertattrib])
    
    def _create_vertnum(self, vmesh):
        vmesh.vertnum = 3
    
    def _create_vertices(self, vmesh):
        positions = [
            (0.5, 0.0, 0.5), # right front
            (-0.5, 0.0, -0.5), # left back
            (-0.5, 0.0, 0.5), # left front
            ]
        normals = [
            (0.0, 1.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 1.0, 0.0),
            ]
        blendices = [
            (0.0,),
            (0.0,),
            (0.0,),
            ]
        uv1 = [
            (1.0, 0.0),
            (0.0, 1.0),
            (0.0, 0.0)
            ]
        tangents = [
            (1.0, 0.0, 0.0), # (0.9999999403953552, 0.0, 0.0)
            (1.0, 0.0, 0.0), # (0.9999999403953552, 0.0, 0.0)
            (1.0, 0.0, 0.0), # (0.9999999403953552, 0.0, 0.0)
            ]
        vertlist = []
        for i in range(3):
            vertlist.extend(positions[i])
            vertlist.extend(normals[i])
            vertlist.extend(blendices[i])
            vertlist.extend(uv1[i])
            vertlist.extend(tangents[i])
        vmesh.vertices = tuple(vertlist) 
    
    def _create_index(self, vmesh):
        vmesh.index = (0, 1, 2)
        vmesh.indexnum = len(vmesh.index)

    def _create_u2(self, vmesh):
        vmesh.u2 = 8
    
    def _create_nodes(self, vmesh):
        for geom in vmesh.geoms:
            for lod in geom.lods:
                lod.version = 11
                lod.min = (-0.5, 0.0, -0.5)
                lod.max = (0.5, 0.0, 0.5)
                #lod.pivot = None # already assigned to None for new modmesh
                lod.nodenum = 1
                lod.nodes = [
                    1.0, 0.0, 0.0, 0.0,
                    0.0, 1.0, 0.0, 0.0,
                    0.0, 0.0, 1.0, 0.0,
                    0.0, 0.0, 0.0, 1.0] # no idea what is this shit in matrix4 ?
                lod.polycount = 0
                
    def _create_materials(self, vmesh):
        for geom in vmesh.geoms:
            for lod in geom.lods:
                lod.matnum = 1
                lod.materials = [modmesh.bf2mat() for i in range(lod.matnum)]
                for material in lod.materials:
                    material.alphamode = 0
                    material.fxfile = b'StaticMesh.fx'
                    material.technique = b'Base'
                    material.mapnum = 1
                    material.maps = []
                    for i in range(material.mapnum):
                        material.maps.insert(i, b'objects/staticobjects/test/evil_box/textures/evil_box_c.dds')
                    material.vstart = 0
                    material.istart = 0
                    material.inum = 3
                    material.vnum = 3
                    material.u4 = 0
                    material.u5 = 0
                    material.nmin = (-0.5, 0.0, -0.5)
                    material.nmax = (0.5, 0.0, 0.5)
                    lod.polycount = lod.polycount + material.inum / 3
                    

class Box:

    def __init__(self):
        self.vmesh = modmesh.StdMesh()
        self._create_header(self.vmesh)
        self._create_u1_bfp4f_version(self.vmesh)
        self._create_geomnum(self.vmesh)
        self._create_geomtable(self.vmesh)
        self._create_vertattribnum(self.vmesh)
        self._create_vertattrib_table(self.vmesh)
        self._create_vertformat(self.vmesh)
        self._create_vertstride(self.vmesh)
        self._create_vertices(self.vmesh)
        self._create_index(self.vmesh)
        self._create_u2(self.vmesh)
        self._create_nodes(self.vmesh)
        self._create_materials(self.vmesh)
        

    def _create_header(self, vmesh):
        vmesh.head = modmesh.bf2head()
        vmesh.head.u1 = 0
        vmesh.head.version = 11
        vmesh.head.u3 = 0
        vmesh.head.u4 = 0
        vmesh.head.u5 = 0

    def _create_u1_bfp4f_version(self, vmesh):
        vmesh.u1 = 0
    
    def _create_geomnum(self, vmesh):
        vmesh.geomnum = 1
        
    def _create_geomtable(self, vmesh):
        vmesh.geoms = [modmesh.bf2geom() for i in range(vmesh.geomnum)]
        vmesh.geoms[0].lodnum = 1
        for geom in vmesh.geoms:
            for i in range(geom.lodnum):
                geom.lods = [modmesh.bf2lod() for i in range(geom.lodnum)]

    def _create_vertattribnum(self, vmesh):
        vmesh.vertattribnum = 6 # +1 for unused? xD
    
    def _create_vertattrib_table(self, vmesh):
        dumb_array = [
            (0, 0, 2, 0), # used, offset=0, float3, position
            (0, 12, 2, 3), # used, offset=12\4, float3, normal
            (0, 24, 4, 2), # used, offset=24\4, d3dcolor, blend indice
            (0, 28, 1, 5), # used, offset=28\4, float2, uv1
            (0, 32, 2, 6), # used, offset=0, float3, tangent
            (255, 0, 17, 0), # not used, offset=0, unused, unused
            ]
        vmesh.vertattrib = [modmesh.vertattrib() for i in range(vmesh.vertattribnum)]
        for i in range(vmesh.vertattribnum):
            vmesh.vertattrib[i].flag = dumb_array[i][0]
            vmesh.vertattrib[i].offset = dumb_array[i][1]
            vmesh.vertattrib[i].vartype = dumb_array[i][2]
            vmesh.vertattrib[i].usage = dumb_array[i][3]
            #print('{}: \n{}'.format(i, vmesh.vertattrib[i]))
    
    def _create_vertformat(self, vmesh):
        vmesh.vertformat = 4
    
    def _create_vertstride(self, vmesh):
        vmesh.vertstride = sum([modmath.d3dtypes_lenght[attrib.vartype]*vmesh.vertformat for attrib in vmesh.vertattrib])

    def _create_vertices(self, vmesh):
        positions = [
            (0.5, 0.0, 0.5),
            (-0.5, 0.0, 0.5),
            (-0.5, 0.0, -0.5),
            (0.5, 0.0, -0.5),
            (0.5, 1.0, 0.5),
            (0.5, 1.0, -0.5),
            (-0.5, 1.0, -0.5),
            (-0.5, 1.0, 0.5),
            (0.5, 1.0, -0.5),
            (0.5, 0.0, -0.5),
            (-0.5, 0.0, -0.5),
            (-0.5, 1.0, -0.5),
            (0.5, 1.0, 0.5),
            (0.5, 0.0, 0.5),
            (0.5, 0.0, -0.5), # 14
            (0.5, 1.0, -0.5),
            (-0.5, 1.0, 0.5),
            (-0.5, 0.0, 0.5),
            (0.5, 0.0, 0.5),
            (0.5, 1.0, 0.5),
            (-0.5, 1.0, -0.5),
            (-0.5, 0.0, -0.5),
            (-0.5, 0.0, 0.5),
            (-0.5, 1.0, 0.5),
            
            (0.5, 0.0, -0.5), # 14
            ]
        normals = [
            (0.0, -1.0, 0.0),
            (0.0, -1.0, 0.0),
            (0.0, -1.0, 0.0),
            (0.0, -1.0, 0.0),
            
            (0.0, 1.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 1.0, 0.0),
            
            (0.0, 0.0, -1.0),
            (0.0, 0.0, -1.0),
            (0.0, 0.0, -1.0),
            (0.0, 0.0, -1.0),
            
            (1.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (1.0, 0.0, 0.0), # 14
            (1.0, 0.0, 0.0),
            
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
            
            (-1.0, 0.0, 0.0),
            (-1.0, 0.0, 0.0),
            (-1.0, 0.0, 0.0),
            (-1.0, 0.0, 0.0),
            
            (1.0, 0.0, 0.0), # 14
            ]
        blendices = [ # 24 blendices
            (0.0,),
            (0.0,),
            (0.0,),
            
            (0.0,),
            (0.0,),
            (0.0,),
            
            (0.0,),
            (0.0,),
            (0.0,),
            
            (0.0,),
            (0.0,),
            (0.0,),
            
            (0.0,),
            (0.0,),
            (0.0,),
            
            (0.0,),
            (0.0,),
            (0.0,),
            
            (0.0,),
            (0.0,),
            (0.0,),
            
            (0.0,),
            (0.0,),
            (0.0,),
            
            (0.0,),
            (0.0,),
            (0.0,),
            
            (0.0,),
            ]
        uv1 = [ # 24 uv1
            (1.0, 0.0),
            (0.0, 1.0),
            (0.0, 0.0),
            
            (1.0, 0.0),
            (0.0, 1.0),
            (0.0, 0.0),
            
            (1.0, 0.0),
            (0.0, 1.0),
            (0.0, 0.0),
            
            (1.0, 0.0),
            (0.0, 1.0),
            (0.0, 0.0),
            
            (1.0, 0.0),
            (0.0, 1.0),
            (0.0, 0.0),
            
            (1.0, 0.0),
            (0.0, 1.0),
            (0.0, 0.0),
            
            (1.0, 0.0),
            (0.0, 1.0),
            (0.0, 0.0),
            
            (1.0, 0.0),
            (0.0, 1.0),
            (0.0, 0.0),
            
            (0.5, 1.0),
            ]
        tangents = [ # 24 tangents
            # left
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),

            # back
            (1.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),

            # right
            (1.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),

            # front
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),
            (0.0, 0.0, 1.0),

            # top
            (-1.0, 0.0, 0.0),
            (-1.0, 0.0, 0.0),
            (-1.0, 0.0, 0.0),
            (-1.0, 0.0, 0.0),

            # bottom
            (0.0, 0.0, -1.0),
            (0.0, 0.0, -1.0),
            (0.0, 0.0, -1.0),
            (0.0, 0.0, -1.0),

            # 24 random vert
            (0.0, 0.0, 1.0),
            ]
        vertlist = []
        for i in range(len(positions)):
            vertlist.extend(positions[i])
            vertlist.extend(normals[i])
            vertlist.extend(blendices[i])
            vertlist.extend(uv1[i])
            vertlist.extend(tangents[i])
        vmesh.vertices = tuple(vertlist)
        vmesh.vertnum = len(positions)
    
    def _create_index(self, vmesh):
        vmesh.index = (
            # left
            22,
            23,
            20,
            20,
            21,
            22,

            # back
            18,
            19,
            16,
            16,
            17,
            18,

            # right
            # using random 24 vertice
            14,
            15,
            12,
            12,
            13,
            14,

            # front
            10,
            11,
            8,
            8,
            9,
            10,

            # top
            6,
            7,
            4,
            4,
            5,
            6,

            # bottom
            2,
            3,
            0,
            0,
            1,
            2,
            )
        vmesh.indexnum = len(vmesh.index)

    def _create_u2(self, vmesh):
        vmesh.u2 = 8
    
    def _create_nodes(self, vmesh):
        for geom in vmesh.geoms:
            for lod in geom.lods:
                lod.version = 11
                lod.min = (-1.0, -1.0, -1.0)
                lod.max = (1.0, 1.0, 1.0)
                #lod.pivot = None # already assigned to None for new modmesh
                lod.nodenum = 1
                lod.nodes = [
                    1.0, 0.0, 0.0, 0.0,
                    0.0, 1.0, 0.0, 0.0,
                    0.0, 0.0, 1.0, 0.0,
                    0.0, 0.0, 0.0, 1.0] # no idea what is this shit in matrix4 ?
                lod.polycount = 0
                
    def _create_materials(self, vmesh):
        for geom in vmesh.geoms:
            for lod in geom.lods:
                lod.matnum = 1
                lod.materials = [modmesh.bf2mat() for i in range(lod.matnum)]
                for material in lod.materials:
                    material.alphamode = 0
                    material.fxfile = b'StaticMesh.fx'
                    material.technique = b'Base'
                    material.mapnum = 1
                    material.maps = []
                    for i in range(material.mapnum):
                        material.maps.insert(i, b'default.dds')
                    material.vstart = 0
                    material.istart = 0
                    material.inum = 24
                    material.vnum = 24
                    material.u4 = 0
                    material.u5 = 0
                    material.nmin = (-1.0, -1.0, -1.0)
                    material.nmax = (1.0, 1.0, 1.0)
                    lod.polycount = lod.polycount + material.inum / 3




