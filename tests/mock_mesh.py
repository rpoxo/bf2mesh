import modmesh


class Box:

    def __init__(self):
        self.vmesh = modmesh.StdMesh()
        self._create_header(self.vmesh)
        self._create_u1_bfp4f_version(self.vmesh)
        self._create_geomnum(self.vmesh)
        self._create_geom_table(self.vmesh)
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
        
    def _create_geom_table(self, vmesh):
        vmesh.geoms = [modmesh.bf2geom() for i in range(vmesh.geomnum)]
        vmesh.geoms[0].lodnum = 1
        for geom in vmesh.geoms:
            for i in range(geom.lodnum):
                geom.lods = [modmesh.bf2lod() for i in range(geom.lodnum)]
    
    def _create_vertattrib_table(self, vmesh):
        dumb_array = [
            (0, 0, 2, 0), # flag:used, offset=0, float3, position
            (0, 12, 2, 3), # flag:used, offset=12\4, float3, normal
            (0, 24, 4, 2), # flag:used, offset=24\4, d3dcolor, blend indice
            (0, 28, 1, 5), # flag:used, offset=28\4, float2, uv1
            (0, 32, 2, 6), # flag:used, offset=0, float3, tangent
            (255, 0, 17, 0), # flag:unused, offset=0, unused, unused
            ]
        vmesh.vertattribnum = len(dumb_array)
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
        vmesh.vertstride = sum([len(modmesh.D3DDECLTYPE(attrib.vartype))*vmesh.vertformat for attrib in vmesh.vertattrib])

    def _create_vertices(self, vmesh):
        # x/y/z
        # left-to-right/bottom-to-top/back-to-front
        positions = [
            (0.5, 1.0, -0.5),
            (0.5, 0.0, -0.5),
            (-0.5, 0.0, -0.5),
            
            (-0.5, 1.0, -0.5),
            (0.5, 1.0, 0.5),
            (-0.5, 1.0, 0.5),
            
            (-0.5, -0.0, 0.5),
            (0.5, -0.0, 0.5),
            (0.5, 1.0, -0.5),
            
            (0.5, 1.0, 0.5),
            (0.5, -0.0, 0.5),
            (0.5, -0.0, -0.5),
            
            (0.5, -0.0, -0.5),
            (0.5, -0.0, 0.5),
            (-0.5, -0.0, 0.5),
            
            (-0.5, -0.0, -0.5),
            (-0.5, -0.0, -0.5),
            (-0.5, -0.0, 0.5),

            (-0.5, 1.0, 0.5),
            (-0.5, 1.0, -0.5),
            (0.5, 1.0, 0.5),
            
            (0.5, 1.0, -0.5),
            (-0.5, 1.0, -0.5),
            (-0.5, 1.0, 0.5),
            ]
        normals = [
            (0.0, 0.0, -1.0),
            (0.0, 0.0, -1.0),
            (0.0, 0.0, -1.0),
            
            (0.0, 0.0, -1.0),
            (0.0, -0.0, 1.0),
            (0.0, -0.0, 1.0),
            
            (0.0, -0.0, 1.0),
            (0.0, -0.0, 1.0),
            (1.0, -0.0, 0.0),
            
            (1.0, -0.0, 0.0),
            (1.0, -0.0, 0.0),
            (1.0, -0.0, 0.0),
            
            (-0.0, -1.0, -0.0),
            (-0.0, -1.0, -0.0),
            (-0.0, -1.0, -0.0),
            
            (-0.0, -1.0, -0.0),
            (-1.0, 0.0, -0.0),
            (-1.0, 0.0, -0.0),
            
            (-1.0, 0.0, -0.0),
            (-1.0, 0.0, -0.0),
            (0.0, 1.0, 0.0),
            
            (0.0, 1.0, 0.0),
            (0.0, 1.0, 0.0),
            (0.0, 1.0, 0.0),
            ]
        blend_indices = [
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
        uv1 = [
            (0.0, 1.0),
            (1.0, 1.0),
            (1.0, 0.0),
            
            (0.0, 0.0),
            (0.0, 0.5),
            (1.0, 0.5),
            
            (1.0, 1.5),
            (0.0, 1.5),
            (0.5, 0.5),
            
            (0.5, 1.0),
            (0.0, 1.0),
            (0.0, 0.5),
            
            (0.5, 0.0),
            (0.5, 0.5),
            (0.0, 0.5),
            
            (0.0, 0.0),
            (1.0, 0.5),
            (1.0, 0.0),
            
            (0.5, 0.0),
            (0.5, 0.5),
            (0.5, 1.0),
            
            (0.5, 0.5),
            (1.0, 0.5),
            (1.0, 1.0),
            ]
        tangents = [
            (1.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 0.0),
            
            (0.0, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            
            (1.5, 0.0, 0.0),
            (1.5, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            
            (1.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            
            (0.0, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            
            (0.0, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            (0.0, 0.0, 0.0),
            
            (0.0, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            
            (0.5, 0.0, 0.0),
            (0.5, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            ]
        vertlist = []
        for i in range(len(positions)):
            vertlist.extend(positions[i])
            vertlist.extend(normals[i])
            vertlist.extend(blend_indices[i])
            vertlist.extend(uv1[i])
            vertlist.extend(tangents[i])
        vmesh.vertices = tuple(vertlist)
        vmesh.vertnum = len(positions)
    
    def _create_index(self, vmesh):
        vmesh.index = (
            22,
            23,
            20,
            20,
            21,
            22,

            18,
            19,
            16,
            16,
            17,
            18,

            14,
            15,
            12,
            12,
            13,
            14,

            10,
            11,
            8,
            8,
            9,
            10,

            6,
            7,
            4,
            4,
            5,
            6,

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
                        material.maps.insert(i, b'default.dds') # replace with texture path
                    material.vstart = 0
                    material.istart = 0
                    material.inum = 36
                    material.vnum = 24
                    material.u4 = 0
                    material.u5 = 0
                    material.nmin = (-1.0, -1.0, -1.0)
                    material.nmax = (1.0, 1.0, 1.0)
                    lod.polycount = lod.polycount + material.inum / 3




