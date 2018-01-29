import modmesh
from modmesh import D3DDECLTYPE, D3DDECLUSAGE


class Box(modmesh.VisMesh):

    def __init__(self):
        modmesh.VisMesh.__init__(self)
        self._create_header()
        self._create_u1_bfp4f_version()
        self._create_geomnum()
        self._create_geom_table()
        self._create_vertformat()
        self._create_vertattrib_table()
        self._create_vertstride()
        self._create_vertices()
        self._create_index()
        self._create_u2()
        self._create_nodes()
        self._create_materials()
        

    def _create_header(self):
        self.head = modmesh.bf2head()
        self.head.u1 = 0
        self.head.version = 11
        self.head.u3 = 0
        self.head.u4 = 0
        self.head.u5 = 0

    def _create_u1_bfp4f_version(self):
        self.u1 = 0
    
    def _create_geomnum(self):
        self.geomnum = 1
        
    def _create_geom_table(self):
        self.geoms = [modmesh.bf2geom() for i in range(self.geomnum)]
        self.geoms[0].lodnum = 1
        for geom in self.geoms:
            for i in range(geom.lodnum):
                geom.lods = [modmesh.bf2lod() for i in range(geom.lodnum)]

    def _create_vertformat(self):
        self.vertformat = 4
    
    def _create_vertattrib_table(self):
        USED = 0
        UNUSED = 255
        # flag, offset(bytes), type, usage 
        dumb_array = [
            (USED, D3DDECLTYPE.FLOAT3, D3DDECLUSAGE.POSITION),
            (USED, D3DDECLTYPE.FLOAT3, D3DDECLUSAGE.NORMAL),
            (USED, D3DDECLTYPE.D3DCOLOR, D3DDECLUSAGE.BLENDINDICES),
            (USED, D3DDECLTYPE.FLOAT2, D3DDECLUSAGE.UV1),
            (USED, D3DDECLTYPE.FLOAT3, D3DDECLUSAGE.TANGENT),
            #(UNUSED, D3DDECLTYPE.UNUSED, D3DDECLUSAGE.POSITION), # dice exporter junk
            ]
        self.vertattribnum = len(dumb_array)
        self.vertattrib = [modmesh.vertattrib() for i in range(self.vertattribnum)]
        vertstride = 0
        for i in range(self.vertattribnum):
            self.vertattrib[i].flag = dumb_array[i][0]
            self.vertattrib[i].offset = vertstride
            self.vertattrib[i].vartype = dumb_array[i][1]
            self.vertattrib[i].usage = dumb_array[i][2]
            
            vertstride += len(self.vertattrib[i].vartype)*self.vertformat

    def _create_vertstride(self):
        self.vertstride = sum([len(modmesh.D3DDECLTYPE(attrib.vartype))*self.vertformat for attrib in self.vertattrib])

    def _create_vertices(self):
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
        verts = []
        for i in range(len(positions)):
            verts.extend(positions[i])
            verts.extend(normals[i])
            verts.extend(blend_indices[i])
            verts.extend(uv1[i])
            verts.extend(tangents[i])
        self.vertices = tuple(verts)
        self.vertnum = len(positions)
    
    def _create_index(self):
        self.index = [
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
            ]
        self.indexnum = len(self.index)

    def _create_u2(self):
        self.u2 = 8
    
    def _create_nodes(self):
        for geom in self.geoms:
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
                
    def _create_materials(self):
        for geom in self.geoms:
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
                    material.mmin = (-1.0, -1.0, -1.0)
                    material.mmax = (1.0, 1.0, 1.0)
                    lod.polycount = lod.polycount + material.inum / 3




