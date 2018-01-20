import os
import enum  # python 3.4+
import struct
import math

# reference for mesh struct:
# https://github.com/ByteHazard/BfMeshView/blob/master/source/modVisMeshLoad.bas


PI = math.pi
RADTODEG = (180 / PI)
DEGTORAD = (PI / 180)


# copypasta from DX SDK 'Include/d3d9types.h' enum _D3DDECLTYPE to address
# vert attribute vartype variable
class D3DDECLTYPE(enum.IntEnum):
    FLOAT1 = 0  # 1D float expanded to (value, 0., 0., 1.)
    FLOAT2 = 1  # 2D float expanded to (value, value, 0., 1.)
    FLOAT3 = 2  # 3D float expanded to (value, value, value, 1.)
    FLOAT4 = 3  # 4D float
    D3DCOLOR = 4  # 4D packed unsigned bytes mapped to 0. to 1. range
                # Input is in D3DCOLOR format (ARGB) expanded to (R, G, B, A)
    UBYTE4 = 5  # 4D unsigned byte
    UNUSED = 17,  # When the type field in a decl is unused.

    def __len__(d3dtype):
        return {
            0: 1,  # D3DDECLTYPE_FLOAT1
            1: 2,  # D3DDECLTYPE_FLOAT2
            2: 3,  # D3DDECLTYPE_FLOAT3
            4: 1,  # D3DDECLTYPE_D3DCOLOR
            5: 3,  # D3DDECLTYPE_UBYTE4
            17: 0,  # D3DDECLTYPE_UNUSED
        }[d3dtype]


# copypasta from DX SDK 'Include/d3d9types.h' enum _D3DDECLUSAGE to
# address vert attribute usage variable
class D3DDECLUSAGE(enum.IntEnum):
    POSITION = 0
    BLENDWEIGHT = 1
    BLENDINDICES = 2
    NORMAL = 3
    PSIZE = 4
    UV1 = 5  # TEXCOORD in d3d9 enums
    TANGENT = 6
    BINORMAL = 7
    TESSFACTOR = 8
    POSITIONT = 9
    COLOR = 10
    FOG = 11
    DEPTH = 12
    SAMPLE = 13
    # bf2 enums much larger than dx to avoid collisions?
    UV2 = 261
    UV3 = 517
    UV4 = 773
    UV5 = 1029
    

class Vec3:
    
    def __init__(self, float3=(0.0, 0.0, 0.0)):
        self.x = float3[0]
        self.y = float3[1]
        self.z = float3[2]
    
    def __str__(self):
        return ', '.join([str(value) for value in [self.x, self.y, self.z]])
    
    def __iter__(self):
        for value in [self.x, self.y, self.z]:
            yield value
        
def LoadBF2Mesh(
        filepath,
        loadTextures=False,
        loadSamples=False,
        loadCon=False):
    with open(filepath, 'rb') as meshfile:
        file_extension = os.path.splitext(filepath)[1].lower()

        isSkinnedMesh = (file_extension == '.skinnedmesh')
        isBundledMesh = (file_extension == '.bundledmesh')
        isStaticMesh = (file_extension == '.staticmesh')

        vmesh = VisMesh(isSkinnedMesh, isBundledMesh, isStaticMesh)
        vmesh.open(meshfile)

        if loadSamples:
            dir = os.path.dirname(filepath)
            for filename in os.listdir(dir):
                filepath = os.path.join(dir, filename)
                name = os.path.splitext(filename)[0]
                ext = os.path.splitext(filename)[1]
                if ext[:5] == '.samp':
                    if ext == '.samples':
                        vmesh.geoms[
                            0].lods[
                            0].sample = LoadBF2Sample(filepath)
                    else:
                        geom = int(ext.split('_')[1][0])
                        lod = int(ext.split('_')[1][1])
                        vmesh.geoms[
                            geom].lods[
                            lod].sample = LoadBF2Sample(filepath)
    return vmesh


def LoadBF2Sample(filepath):
    with open(filepath, 'rb') as samplefile:
        sample = StdSample()
        sample.open(samplefile)
    return sample


def read_int(fo):
    fmt = 'i'
    size = struct.calcsize(fmt)
    return struct.Struct(fmt).unpack(fo.read(size))[0]


def read_float(fo):
    fmt = 'f'
    size = struct.calcsize(fmt)
    return struct.Struct(fmt).unpack(fo.read(size))[0]


def read_float3(fo):
    fmt = '3f'
    size = struct.calcsize(fmt)
    return tuple(struct.Struct(fmt).unpack(fo.read(size)))


def read_long(fo):
    fmt = 'l'
    size = struct.calcsize(fmt)
    return struct.Struct(fmt).unpack(fo.read(size))[0]


def read_short(fo):
    fmt = 'h'
    size = struct.calcsize(fmt)
    return struct.Struct(fmt).unpack(fo.read(size))[0]


def read_string(fo, lenght=1):
    fmt = '{}s'.format(lenght)
    size = struct.calcsize(fmt)
    return struct.Struct(fmt).unpack(fo.read(size))[0]


def read_byte(fo):
    fmt = 'b'
    size = struct.calcsize(fmt)
    return struct.Struct(fmt).unpack(fo.read(size))[0]
    
def read_matrix4(fo):
    fmt = '16f'
    size = struct.calcsize(fmt)
    return struct.Struct(fmt).unpack(fo.read(size))


class bf2lod:

    def __init__(self):
        self.version = None

        self.min = None
        self.max = None
        self.pivot = None # just some unknown float3 for .version <=6

        # rigs, only for skinned meshes
        self.rignum = None
        self.rigs = []
        
        # nodes for bundled and staticmeshes
        # apparently those a geomPart objects for animating sprints\rotbundles etc
        self.nodenum = None
        self.nodes = [] # matrix4
        
        self.matnum = None
        self.materials = []
        
        # internal for calculating total lod tris(yes, that weird)
        self.polycount = 0
        # StdSample object for LMing statics
        self.sample = None


class bf2rig:
    
    def __init__(self):
        self.bonenum = None
        self.bones = []
    

class bf2bone:
    
    def __init__(self):
        self.id = None
        self.matrix = []
        
        self.skinmat = []


class bf2mat:

    def __init__(self):
        self.alphamode = None
        self.fxfile = None
        self.technique = None
        self.mapnum = None
        self.maps = None
        self.vstart = None
        self.istart = None
        self.inum = None
        self.vnum = None
        self.u4 = None
        self.u5 = None
        self.mmin = None
        self.mmax = None

    def __get_string(self, fo):
        string_len = read_long(fo)
        return read_string(fo, string_len)

    def __get_maps(self, fo):
        mapnames = []
        for i in range(self.mapnum):
            mapname = self.__get_string(fo)
            mapnames.append(mapname)
        return mapnames

    def read(self, fo, isSkinnedMesh, version):
        #print('>> starting reading material at {}'.format(fo.tell()))
        if not isSkinnedMesh:
            self.alphamode = read_long(fo)
        self.fxfile = self.__get_string(fo)
        self.technique = self.__get_string(fo)
        self.mapnum = read_long(fo)
        self.maps = self.__get_maps(fo)
        self.vstart = read_long(fo)
        self.istart = read_long(fo)
        self.inum = read_long(fo)
        self.vnum = read_long(fo)
        self.u4 = read_long(fo)
        self.u5 = read_long(fo)
        if not isSkinnedMesh and version == 11:
            self.mmin = read_float3(fo)
            self.mmax = read_float3(fo)


class bf2head:

    def __init__(self):
        self.u1 = None
        self.version = None
        self.u3 = None
        self.u4 = None
        self.u5 = None

    def read(self, fo):
        self.u1 = read_long(fo)
        self.version = read_long(fo)
        self.u3 = read_long(fo)
        self.u4 = read_long(fo)
        self.u5 = read_long(fo)

    def __eq__(self, other):
        if self.u1 != other.u1:
            return False
        if self.version != other.version:
            return False
        if self.u3 != other.u3:
            return False
        if self.u4 != other.u4:
            return False
        if self.u5 != other.u5:
            return False
        return True


class bf2geom:

    def __init__(self):
        self.lodnum = None
        self.lods = []

    def read_lodnum(self, fo):
        self.lodnum = read_long(fo)
        self.lods = [bf2lod() for i in range(self.lodnum)]


class vertattrib:

    def __init__(self):
        self.flag = None
        self.offset = None
        self.vartype = None
        self.usage = None

    def read_vertattrib(self, fo):
        self.flag = read_short(fo)  # some bool, never used
        self.offset = read_short(fo)  # offset from vertex data start in bytes
        # DX SDK 'Include/d3d9types.h' enum _D3DDECLTYPE
        self.vartype = read_short(fo)
        # DX SDK 'Include/d3d9types.h' enum _D3DDECLUSAGE
        self.usage = read_short(fo)

    def __str__(self):
        return str((self.flag, self.offset, self.vartype, self.usage))

    def __eq__(self, other_tuple):
        if (self.flag, self.offset, self.vartype, self.usage) == other_tuple:
            return True
        else:
            return False


class VisMeshTransform:

    def __init__(self, vmesh):
        self.vmesh = vmesh

    def copy_geom_id(self, id_copy, id_new):
        self.vmesh.geomnum += 1
        self.vmesh.geoms.insert(id_new, self.vmesh.geoms[id_copy])
    
    def delete_geom_id(self, id_delete):
        geom_vnum, geom_inum = [sum(x) for x in zip(*[(material.vnum,
                                        material.inum) for lod in self.vmesh.geoms[id_delete].lods for material in lod.materials])]

        # remove vertex data
        vstart = int(self.vmesh.vertstride / self.vmesh.vertformat * self.vmesh.geoms[id_delete].lods[0].materials[0].vstart)
        vnum = int(self.vmesh.vertstride / self.vmesh.vertformat * geom_vnum)
        del self.vmesh.vertices[vstart:vstart+vnum]
        self.vmesh.vertnum -= geom_vnum
        
        # remove index data
        istart = self.vmesh.geoms[id_delete].lods[0].materials[0].istart
        #print('old index len = {}, deleting {} from {}'.format(
        #    len(self.vmesh.index),
        #    geom_inum,
        #    istart))
        del self.vmesh.index[istart:istart+geom_inum]
        self.vmesh.indexnum -= geom_inum
        #print('new index len = {}'.format(len(self.vmesh.index)))
        
        # remove geom from geom table
        for id_geom, geom in enumerate(self.vmesh.geoms):
            if id_geom > id_delete:
                for lod in geom.lods:
                    for material in lod.materials:
                        material.vstart -= geom_vnum
                        material.istart -= geom_inum

        self.vmesh.geomnum -= 1
        del self.vmesh.geoms[id_delete]
    
    def edit_geoms_order(self, order):
        raise NotImplementedError
        self.vmesh.geoms = [self.vmesh.geoms[id_geom] for id_geom in order]
    
    def edit_vertex(self, id_vertex, vattribute, vdata):
        for attrib_id, attrib in enumerate(self.vmesh.vertattrib):
            usage = D3DDECLUSAGE(attrib.usage).name
            offset = int(attrib.offset / self.vmesh.vertformat)
            vartype = D3DDECLTYPE(attrib.vartype).name
            vlen = len(D3DDECLTYPE(attrib.vartype))

            if usage == vattribute:
                #print('SETTING DATA for v[{}] {}'.format(id_vertex, vattribute))
                for vertid in range(self.vmesh.vertnum - 1, -1, -1):
                    vstart = offset + vertid * \
                        int(self.vmesh.vertstride / self.vmesh.vertformat)
                    if vertid == id_vertex:
                        for i, data in enumerate(vdata):
                            self.vmesh.vertices[vstart + i] = data
    
    def offset_mesh_vertices(self, offset):
        for id_vertex in range(self.vmesh.vertnum):
            position_old = self.vmesh.get_vertex_data(id_vertex, 'POSITION')
            position_new = tuple(sum(i) for i in zip(position_old, offset))
            self.edit_vertex(id_vertex, 'POSITION', position_new)
    
    def merge_mesh(self, other):
        # need to correct index before vertices due to vertnum adjustment
        index = list(self.vmesh.index)
        for idx in other.index:
            index.append(idx+self.vmesh.vertnum)
        self.vmesh.index = tuple(index) # convert back
        self.vmesh.indexnum += other.indexnum

        self.vmesh.vertnum += other.vertnum
        self.vmesh.vertices.extend(other.vertices)
        
        for i, geom in enumerate(self.vmesh.geoms):
            for j, lod in enumerate(self.vmesh.geoms[i].lods):
                for k, material in enumerate(self.vmesh.geoms[i].lods[j].materials):
                    self.vmesh.geoms[i].lods[j].materials[k].vnum += other.geoms[i].lods[j].materials[k].vnum
                    self.vmesh.geoms[i].lods[j].materials[k].inum += other.geoms[i].lods[j].materials[k].inum
                    self.vmesh.geoms[i].lods[j].materials[k].mmin = tuple(sum(i) for i in zip(self.vmesh.geoms[i].lods[j].materials[k].mmin, other.geoms[i].lods[j].materials[k].mmin))
                    self.vmesh.geoms[i].lods[j].materials[k].mmax = tuple(sum(i) for i in zip(self.vmesh.geoms[i].lods[j].materials[k].mmax, other.geoms[i].lods[j].materials[k].mmax))
    
    def rename_texture(self, geom, lod, material, map, path):
        self.vmesh.geoms[geom].lods[lod].materials[material].maps[map] = bytes(path, 'ascii')
    
    def rotate_mesh(self, rotation_euler):
        
        def rotate_vertex(position, rotation, center):
            yaw = rotation[0]
            pitch = rotation[1]
            roll = rotation[2]
            
            sx = math.sin(yaw)
            cx = math.cos(yaw)
            sy = math.sin(pitch)
            cy = math.cos(pitch)
            sz = math.sin(roll)
            cz = math.cos(roll)

            x1 =  position.x * cz +  position.y * sz
            y1 =  position.y * cz -  position.x * sz
            z1 =  position.z

            x2 = x1 * cy + z1 * sy
            y2 = z1
            z2 = z1 * cy - x1 * sy

            x3 = x2
            y3 = y2 * cx + z1 * sx
            z3 = z2 * cx - x1 * sx

            xr = x3 + center.x
            yr = y3 + center.y
            zr = z3 + center.z
            
            return (xr, yr, zr)
            
        vattribute = 'POSITION'
        for vid in range(self.vmesh.vertnum):
            for attrib_id, attrib in enumerate(self.vmesh.vertattrib):
                usage = D3DDECLUSAGE(attrib.usage).name
                offset = int(attrib.offset / self.vmesh.vertformat)
                vartype = D3DDECLTYPE(attrib.vartype).name
                vlen = len(D3DDECLTYPE(attrib.vartype))

                if usage == vattribute and vartype != 'UNUSED':
                    vstart = offset + vid * int(self.vmesh.vertstride / self.vmesh.vertformat)
                    vdata = self.vmesh.vertices[vstart:vstart + vlen]

                    rotated_vertex = rotate_vertex(Vec3(vdata), rotation_euler, Vec3((0.0, 0.0, 0.0)))
                    for i, value in enumerate(rotated_vertex):
                        self.vmesh.vertices[vstart + i] = value
        
        

class VisMesh:

    def __init__(
            self,
            isSkinnedMesh=False,
            isBundledMesh=False,
            isStaticMesh=False):
        # setting some flags
        # perhaps should at least one by default?
        self.isSkinnedMesh = isSkinnedMesh
        self.isBundledMesh = isBundledMesh
        self.isStaticMesh = isStaticMesh

        # mesh data
        self.head = None  # header contains version and some bfp4f data
        self.u1 = None  # version flag for bfp4f
        self.geomnum = None  # amount of geoms
        self.geoms = None  # geometry struct, hold materials info etc
        self.vertattribnum = None  # amount of vertex attributes
        self.vertattrib = None  # vertex attributes table, struct info
        self.vertformat = None  # bytes lenght? seems to be always 4
        self.vertstride = None  # bytes len for vertex data chunk
        self.vertnum = None  # number of vertices
        self.vertices = None  # geom data, parse using attrib table
        self.indexnum = None  # number of indices
        # !!! indices aligned per material !!!
        self.index = None  # indices array
        self.u2 = None  # some another bfp4f garbage..

    # TODO: Move to seperate class
    def get_vertex_data(self, vid, vattribute):
        for attrib_id, attrib in enumerate(self.vertattrib):
            usage = D3DDECLUSAGE(attrib.usage).name
            offset = int(attrib.offset / self.vertformat)
            vartype = D3DDECLTYPE(attrib.vartype).name
            vlen = len(D3DDECLTYPE(attrib.vartype))

            if usage == vattribute and vartype != 'UNUSED':
                vstart = offset + vid * int(self.vertstride / self.vertformat)
                vdata = self.vertices[vstart:vstart + vlen]
        return tuple(vdata)

    # just a wrappers for better function name
    def open(self, fo):
        # materials read will read everything inb4
        self._read_filedata(fo)

    def save(self, fo):
        self._write_materials(fo)

    #-----------------------------
    # READING FILEDATA
    #-----------------------------
    def _read_head(self, fo):
        header = bf2head()
        header.read(fo)
        self.head = header
        #print('head ends at {}'.format(fo.tell()))

    def _read_u1_bfp4f_version(self, fo):
        self._read_head(fo)

        self.u1 = read_byte(fo)

    def _read_geomnum(self, fo):
        self._read_u1_bfp4f_version(fo)

        self.geomnum = read_long(fo)

    def _read_geom_table(self, fo):
        self._read_geomnum(fo)

        self.geoms = [bf2geom() for i in range(self.geomnum)]
        for i in range(self.geomnum):
            self.geoms[i].read_lodnum(fo)

    def _read_vertattribnum(self, fo):
        self._read_geom_table(fo)

        self.vertattribnum = read_long(fo)
        #print('.vertattribnum = {}'.format(self.vertattribnum))

    def _read_vertattrib_table(self, fo):
        self._read_vertattribnum(fo)

        self.vertattrib = [vertattrib() for i in range(self.vertattribnum)]
        for i in range(self.vertattribnum):
            self.vertattrib[i].read_vertattrib(fo)
            #print('>> [{}]{}'.format(i, fo.tell()))

    def _read_vertformat(self, fo):
        self._read_vertattrib_table(fo)

        self.vertformat = read_long(fo)

    def _read_vertstride(self, fo):
        self._read_vertformat(fo)
        #print('>> {}'.format(fo.tell()))

        self.vertstride = read_long(fo)

    def _read_vertnum(self, fo):
        self._read_vertstride(fo)
        #print('>> {}'.format(fo.tell()))

        self.vertnum = read_long(fo)

    def _read_vertex_block(self, fo):
        self._read_vertnum(fo)
        #print('>> {}'.format(fo.tell()))
        #print('self.vertnum = {}'.format(self.vertnum))

        vertices_num = int(self.vertstride / self.vertformat * self.vertnum)
        #print('vertices_num = {}'.format(vertices_num))
        # TODO: refactor
        fmt = '{}f'.format(vertices_num)
        size = struct.calcsize(fmt)

        self.vertices = list(struct.Struct(fmt).unpack(fo.read(size))) # TODO: remove conversions everywhere
        #print('>> {}'.format(fo.tell()))

    def _read_indexnum(self, fo):
        self._read_vertex_block(fo)
        #print('>> vertex block end at {}'.format(fo.tell()))

        self.indexnum = read_long(fo)
        #print('self.indexnum = {}'.format(self.indexnum))

    def _read_index_block(self, fo):
        self._read_indexnum(fo)

        # TODO: refactor
        fmt = '{}H'.format(self.indexnum)
        size = struct.calcsize(fmt)

        self.index = list(struct.Struct(fmt).unpack(fo.read(size))) # TODO: remove conversions everywhere

    def _read_u2(self, fo):
        self._read_index_block(fo)

        if not self.isSkinnedMesh:
            self.u2 = read_long(fo)

    def _read_nodes(self, fo):
        self._read_u2(fo)

        for geom in self.geoms:
            for lod in geom.lods:
                #lod.version = self.head.version
                lod.min = read_float3(fo)
                lod.max = read_float3(fo)
                if self.head.version <= 6:
                    lod.pivot = read_float3(fo)
                if not self.isSkinnedMesh:
                    lod.nodenum = read_long(fo)
                    # reading nodes matrix
                    if not self.isBundledMesh:
                        for i in range(lod.nodenum):
                            lod.nodes = read_matrix4(fo)
                else:
                    lod.rignum = read_long(fo)
                    if lod.rignum > 0:
                        lod.rigs = [bf2rig() for i in range(lod.rignum)]
                        for rig in lod.rigs:
                            rig.bonenum = read_long(fo)
                            if rig.bonenum > 0:
                                rig.bones = [bf2bone() for i in range(rig.bonenum)]
                                for bone in rig.bones:
                                    bone.id = read_long(fo)
                                    bone.matrix = read_matrix4(fo)

    def _read_materials(self, fo):
        self._read_nodes(fo)

        for geom in self.geoms:
            for lod in geom.lods:
                lod.matnum = read_long(fo)
                lod.materials = [bf2mat() for i in range(lod.matnum)]
                for material in lod.materials:
                    material.read(fo, self.isSkinnedMesh, self.head.version)
                lod.polycount = lod.polycount + material.inum / 3

    def _read_filedata(self, fo):
        self._read_materials(fo)

    #-----------------------------
    # WRITING FILEDATA
    #-----------------------------
    def _write_header(self, filepath):
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filepath, 'wb+') as fo:
            fmt = '5l'
            head = (self.head.u1,
                       self.head.version,
                       self.head.u3,
                       self.head.u4,
                       self.head.u5)
            fo.write(struct.Struct(fmt).pack(*head))

    def _write_u1_bfp4f_version(self, filepath):
        self._write_header(filepath)

        with open(filepath, 'ab+') as fo:
            fmt = 'b'
            fo.write(struct.Struct(fmt).pack(self.u1))

    def _write_geomnum(self, filepath):
        self._write_u1_bfp4f_version(filepath)

        with open(filepath, 'ab+') as fo:
            fmt = 'l'
            fo.write(struct.Struct(fmt).pack(self.geomnum))

    def _write_geom_table(self, filepath):
        self._write_geomnum(filepath)

        with open(filepath, 'ab+') as fo:
            for geomnum in range(self.geomnum):
                fmt = 'l'
                fo.write(struct.Struct(fmt).pack(self.geoms[geomnum].lodnum))

    def _write_vertattribnum(self, filepath):
        self._write_geom_table(filepath)

        with open(filepath, 'ab+') as fo:
            fmt = 'l'
            fo.write(struct.Struct(fmt).pack(self.vertattribnum))

    def _write_vertattrib_table(self, filepath):
        self._write_vertattribnum(filepath)

        with open(filepath, 'ab+') as fo:
            for vertattribnum in range(self.vertattribnum):
                fmt = '4h'
                data = (self.vertattrib[vertattribnum].flag,
                        self.vertattrib[vertattribnum].offset,
                        self.vertattrib[vertattribnum].vartype,
                        self.vertattrib[vertattribnum].usage)
                fo.write(struct.Struct(fmt).pack(*data))

    def _write_vertformat(self, filepath):
        self._write_vertattrib_table(filepath)

        with open(filepath, 'ab+') as fo:
            fmt = 'l'
            fo.write(struct.Struct(fmt).pack(self.vertformat))

    def _write_vertstride(self, filepath):
        self._write_vertformat(filepath)

        with open(filepath, 'ab+') as fo:
            fmt = 'l'
            fo.write(struct.Struct(fmt).pack(self.vertstride))

    def _write_vertnum(self, filepath):
        self._write_vertstride(filepath)

        with open(filepath, 'ab+') as fo:
            fmt = 'l'
            fo.write(struct.Struct(fmt).pack(self.vertnum))

    def _write_vertex_block(self, filepath):
        self._write_vertnum(filepath)

        #print('writing {} vertices'.format(len(self.vertices)))
        with open(filepath, 'ab+') as fo:
            fmt = '{}f'.format(len(self.vertices))
            fo.write(struct.Struct(fmt).pack(*self.vertices))

    def _write_indexnum(self, filepath):
        self._write_vertex_block(filepath)

        with open(filepath, 'ab+') as fo:
            fmt = 'l'
            fo.write(struct.Struct(fmt).pack(self.indexnum))

    def _write_index_block(self, filepath):
        self._write_indexnum(filepath)

        with open(filepath, 'ab+') as fo:
            fmt = '{}H'.format(len(self.index))
            fo.write(struct.Struct(fmt).pack(*self.index))

    def _write_u2(self, filepath):
        self._write_index_block(filepath)

        if not self.isSkinnedMesh:
            with open(filepath, 'ab+') as fo:
                fmt = 'l'
                fo.write(struct.Struct(fmt).pack(self.u2))

    def _write_nodes(self, filepath):
        self._write_u2(filepath)

        with open(filepath, 'ab+') as fo:
            for geom in self.geoms:
                for lod in geom.lods:
                    fo.write(struct.Struct('3f').pack(*lod.min))
                    fo.write(struct.Struct('3f').pack(*lod.max))
                    if self.head.version <= 6:
                        fo.write(struct.Struct('3f').pack(*lod.pivot))
                    if self.isSkinnedMesh:
                        fo.write(struct.Struct('l').pack(lod.rignum))
                        for rig in lod.rigs:
                            fo.write(struct.Struct('l').pack(rig.bonenum))
                            for bone in rig.bones:
                                fo.write(struct.Struct('l').pack(bone.id))
                                fo.write(struct.Struct('16f').pack(*bone.matrix))
                    else:
                        fo.write(struct.Struct('l').pack(lod.nodenum))
                        # writing nodes matrix
                        if not self.isBundledMesh:
                            for i in range(lod.nodenum):
                                fo.write(struct.Struct('16f').pack(*lod.nodes))

    def _write_materials(self, filepath):
        self._write_nodes(filepath)

        def __write_bin_string(fo, bstring):
            fo.write(struct.Struct('l').pack(len(bstring)))
            fo.write(struct.Struct('{}s'.format(len(bstring))).pack(bstring))

        with open(filepath, 'ab+') as fo:
            for geom in self.geoms:
                for lod in geom.lods:
                    fo.write(struct.Struct('l').pack(lod.matnum))
                    for material in lod.materials:
                        if not self.isSkinnedMesh:
                            fo.write(struct.Struct('l').pack(material.alphamode))
                        __write_bin_string(fo, material.fxfile)
                        __write_bin_string(fo, material.technique)
                        fo.write(struct.Struct('l').pack(material.mapnum))
                        for map in material.maps:
                            __write_bin_string(fo, map)
                        fo.write(struct.Struct('l').pack(material.vstart))
                        fo.write(struct.Struct('l').pack(material.istart))
                        fo.write(struct.Struct('l').pack(material.inum))
                        fo.write(struct.Struct('l').pack(material.vnum))
                        fo.write(struct.Struct('l').pack(material.u4))
                        fo.write(struct.Struct('l').pack(material.u5))
                        if not self.isSkinnedMesh and self.head.version == 11:
                            fo.write(struct.Struct('3f').pack(*material.mmin))
                            fo.write(struct.Struct('3f').pack(*material.mmax))


class smp_sample:

    def __init__(self):
        self.position = None
        self.rotation = None
        self.face = None

    def read(self, fo):
        self.position = read_float3(fo)
        self.rotation = read_float3(fo)
        self.face = read_long(fo)


class smp_face:

    def __init__(self):
        '''
            v1 As float3
            n1 As float3

            v2 As float3
            n2 As float3

            v3 As float3
            n3 As float3
        '''
        self.v1 = None
        self.n1 = None

        self.v2 = None
        self.n2 = None

        self.v3 = None
        self.n3 = None

    def read(self, fo):
        self.v1 = read_float3(fo)
        self.n1 = read_float3(fo)

        self.v2 = read_float3(fo)
        self.n2 = read_float3(fo)

        self.v3 = read_float3(fo)
        self.n3 = read_float3(fo)


class StdSample:

    def __init__(self):
        # header
        self.fourcc = None
        self.width = None
        self.height = None

        self.datanum = None
        self.data = []

        self.facenum = None
        self.faces = []

    def open(self, fo):
        self._read_faces(fo)

    def _read_head(self, fo):
        self.fourcc = read_string(fo, lenght=4)
        self.width = read_long(fo)
        self.height = read_long(fo)

    def _read_data(self, fo):
        self._read_head(fo)

        self.datanum = self.width * self.height
        for i in range(self.datanum):
            sample = smp_sample()
            sample.read(fo)
            self.data.append(sample)

    def _read_faces(self, fo):
        self._read_data(fo)

        self.facenum = read_long(fo)
        for i in range(self.facenum):
            face = smp_face()
            face.read(fo)
            self.faces.append(face)
