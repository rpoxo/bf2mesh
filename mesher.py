import os
import struct

import bf2

# https://github.com/ByteHazard/BfMeshView/blob/master/source/modStdMesh.bas

def LoadBF2Mesh(filepath):
    with open(filepath, 'rb') as meshfile:
        isSkinnedMesh = False
        isBundledMesh = False
        isStaticMesh = False
        mesh_types = {
            '.skinnedmesh' : isSkinnedMesh,
            '.bundledmesh' : isBundledMesh,
            '.staticmesh' : isStaticMesh
            }
        mesh_types[os.path.splitext(filepath)[0].lower()] = True
        vmesh = StdMeshFile(meshfile, mesh_types)
    return vmesh

class bf2lod:
    def __init__(self, fo, version):
        # some internals
        self.version = version
        
        self.min = None
        self.max = None
        self.pivot = None
        self.nodenum = None

        self.node = []
        self.polycount = 0
        self.matnum = None
        self.mat = []
        
    def __read_bounds(self, fo):
        _fmt = '6f'
        _size = struct.calcsize(_fmt)
        _data = struct.Struct(_fmt).unpack(fo.read(_size))
        
        self.min = tuple(_data[0:3])
        self.max = tuple(_data[3:6])

    def __read_pivot(self, fo):
        if self.version <= 6:
            _fmt = '3f'
            _size = struct.calcsize(_fmt)
            _data = struct.Struct(_fmt).unpack(fo.read(_size))

            self.pivot = tuple(_data)

    def __read_nodenum(self, fo):
        _fmt = 'l'
        _size = struct.calcsize(_fmt)
        _data = struct.Struct(_fmt).unpack(fo.read(_size))

        self.nodenum = int(_data[0])

    
    def read_lod_node_table(self, fo):
        self.__read_bounds(fo)
        self.__read_pivot(fo)
        self.__read_nodenum(fo)
        print('reading nodetable at {}'.format(fo.tell()))
        for i in range(self.nodenum):
            for j in range(16):
                _fmt = 'f'
                _size = struct.calcsize(_fmt)
                _data = struct.Struct(_fmt).unpack(fo.read(_size))
                self.node.append(_data[0])
        print('finished nodetable at {}'.format(fo.tell()))
            
    def read_geom_lod(self, fo, version):
        self._fmt = 'l'
        self._size = struct.calcsize(self._fmt)

        data = struct.Struct(self._fmt).unpack(fo.read(self._size))
        self.matnum = data[0]
        #print('matnum = {}'.format(self.matnum))
        #self.mat.append(bf2mat(fo))
        for i in range(self.matnum):
            material = bf2mat(fo)
            self.mat.append(material)
            self.polycount = self.polycount + material.inum / 3

class bf2mat:
    def __init__(self, fo):
        self.alphamode = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.fxfile = self.__get_string(fo)
        self.technique = self.__get_string(fo)
        self.mapnum = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.map = self.__get_maps(fo)
        self.vstart = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.istart = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.inum = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.vnum = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.u4 = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        self.u5 = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        #if not mesh_types['.skinnedmesh'] and version == 11:
        #    self.nmin = tuple(struct.Struct('3f').unpack(fo.read(struct.calcsize('3f'))))
        #   self.nmax = tuple(struct.Struct('3f').unpack(fo.read(struct.calcsize('3f'))))
        
    def __get_string(self, fo):
        string_len = struct.Struct('l').unpack(fo.read(struct.calcsize('l')))[0]
        string_fmt = str(string_len) + 's'
        return struct.Struct(string_fmt).unpack(fo.read(struct.calcsize(string_fmt)))[0]
    
    def __get_maps(self, fo):
        mapnames = []
        for i in range(self.mapnum):
            mapnames.append(self.__get_string(fo))
        return mapnames
            

class bf2head:
    def __init__(self, fo, offset):
        # some internals
        self._fmt = ('5l')
        self._size = struct.calcsize(self._fmt)

        # reading bin
        data = struct.Struct(self._fmt).unpack(fo.read(self._size))
        self.u1 = data[0]
        self.version = data[1]
        self.u3 = data[2]
        self.u4 = data[3]
        self.u5 = data[4]
    
    def __eq__(self, other):
        if self.u1 != other.u1: return False
        if self.version != other.version : return False
        if self.u3 != other.u3: return False
        if self.u4 != other.u4: return False
        if self.u5 != other.u5: return False
        return True

class bf2geom:
    def __init__(self, fo):
        # some internals
        self._fmt = ('l')
        self._size = struct.calcsize(self._fmt)
        
        # reading bin
        data = struct.Struct(self._fmt).unpack(fo.read(self._size))
        self.lodnum = data[0]
        self.lod = []

class vertattrib:
    def __init__(self, fo):
        # some internals
        self._fmt = ('4h')
        self._size = struct.calcsize(self._fmt)

        # reading bin
        data = struct.Struct(self._fmt).unpack(fo.read(self._size))
        self.flag = data[0]
        self.offset = data[1]
        self.vartype = data[2]
        self.usage = data[3]

    def __str__(self):
        return str((self.flag, self.offset, self.vartype, self.usage))
    
    def __eq__(self, other_tuple):
        if (self.flag, self.offset, self.vartype, self.usage) == other_tuple:
            return True
        else:
            return False



class StdMesh:

    def __init__(self, fo):
        # setting some internals
        self.isSkinnedMesh = False
        self.isBundledMesh = False
        self.isStaticMesh = False
        self._tail = 0

        # mesh data
        self.head = None
        self.u1 = None
        self.geomnum = None
        self.geoms = None
        self.vertattribnum = None
        self.vertattrib = None
        self.vertformat = None
        self.vertstride = None
        self.vertnum = None
        self.vertices = None
        self.indexnum = None
        self.index = None
        self.u2 = None
        print('file len = {}'.format(fo.tell()))

    #-----------------------------
    # READING FILEDATA
    #-----------------------------
    def _read_head(self, fo):
        self.head = bf2head(fo, self._tail)
        self._tail = self.head._size
    
    def _read_u1_bfp4f_version(self, fo):
        self._read_head(fo)
        _fmt = 'b'
        _size = struct.calcsize(_fmt)

        self.u1 = struct.Struct(_fmt).unpack(fo.read(_size))[0]
        self._tail += _size

    def _read_geomnum(self, fo):
        self._read_u1_bfp4f_version(fo)
        _fmt = 'l'
        _size = struct.calcsize(_fmt)

        self.geomnum = struct.Struct(_fmt).unpack(fo.read(_size))[0]
        self._tail += _size
    
    def _read_geoms(self, fo):
        self._read_geomnum(fo)
        self.geoms = [bf2geom(fo) for i in range(self.geomnum)]
        self._tail += self.geoms[0]._size * len(self.geoms)
    
    def _read_vertattribnum(self, fo):
        self._read_geoms(fo)
        _fmt = 'l'
        _size = struct.calcsize(_fmt)

        self.vertattribnum = struct.Struct(_fmt).unpack(fo.read(_size))[0]
        self._tail += _size

    def _read_vertext_attribute_table(self, fo):
        self._read_vertattribnum(fo)
        self.vertattrib = [vertattrib(fo) for i in range(self.vertattribnum)]
        self._tail += self.vertattrib[0]._size * len(self.vertattrib)
        
    def _read_vertformat(self, fo):
        self._read_vertext_attribute_table(fo)
        _fmt = 'l'
        _size = struct.calcsize(_fmt)

        self.vertformat = struct.Struct(_fmt).unpack(fo.read(_size))[0]
        self._tail += _size
        
    def _read_vertstride(self, fo):
        self._read_vertformat(fo)
        _fmt = 'l'
        _size = struct.calcsize(_fmt)

        self.vertstride = struct.Struct(_fmt).unpack(fo.read(_size))[0]
        self._tail += _size
        
    def _read_vertnum(self, fo):
        self._read_vertstride(fo)
        _fmt = 'l'
        _size = struct.calcsize(_fmt)

        self.vertnum = struct.Struct(_fmt).unpack(fo.read(_size))[0]
        self._tail += _size
    
    def _read_vertex_block(self, fo):
        self._read_vertnum(fo)
        _vertices_num = int(self.vertstride/self.vertformat * self.vertnum)
        _fmt = '{}f'.format(_vertices_num)
        _size = struct.calcsize(_fmt)
        
        self.vertices = struct.Struct(_fmt).unpack(fo.read(_size))
        self._tail += _size
    
    def _read_indexnum(self, fo):
        self._read_vertex_block(fo)
        _fmt = 'l'
        _size = struct.calcsize(_fmt)

        self.indexnum = struct.Struct(_fmt).unpack(fo.read(_size))[0]
        self._tail += _size

    def _read_index_block(self, fo):
        self._read_indexnum(fo)
        _fmt = '{}h'.format(self.indexnum)
        _size = struct.calcsize(_fmt)
        
        self.index = struct.Struct(_fmt).unpack(fo.read(_size))
        self._tail += _size

    def _read_u2(self, fo):
        if not self.isSkinnedMesh:
            self._read_index_block(fo)
            _fmt = 'l'.format(self.indexnum)
            _size = struct.calcsize(_fmt)
            
            self.u2 = struct.Struct(_fmt).unpack(fo.read(_size))[0]
            self._tail += _size
    
    def _read_nodes(self, fo):
        self._read_u2(fo)
        for geomnum in range(self.geomnum):
            for lodnum in range(self.geoms[geomnum].lodnum):
                self.geoms[geomnum].lod.insert(lodnum, bf2lod(fo, self.head.version))
                self._tail += fo.tell()
                self.geoms[geomnum].lod[lodnum].read_lod_node_table(fo)
                
                # should have this calculated instead
                self._tail = fo.tell()
                print(self._tail)
                #self.tail += self.geoms[geomnum].lod[lodnum].get_size()?
    
    def _read_node_matrix(self, fo):
        self._read_nodes(fo)
        for geomnum in range(self.geomnum):
            for lodnum in range(self.geoms[geomnum].lodnum):
                self.geoms[geomnum].lod[lodnum].read_geom_lod(fo, self.head.version)

    #-----------------------------
    # WRITING FILEDATA
    #-----------------------------
    def _write_header(self, filepath):
        with open(filepath, 'wb+') as fo:
            dataset = (self.head.u1,
                    self.head.version,
                    self.head.u3,
                    self.head.u4,
                    self.head.u5)
            fo.write(struct.Struct(self.head._fmt).pack(*dataset))
            return fo.tell()

    def _write_u1_bfp4f_version(self, filepath):
        with open(filepath, 'ab+') as fo:
            fmt = 'b'
            fo.write(struct.Struct(fmt).pack(self.u1))
            return fo.tell()


    def _write_geomnum(self, filepath):
        self._write_u1_bfp4f_version(filepath)
        with open(filepath, 'ab+') as fo:
            fmt = 'l'
            fo.write(struct.Struct(fmt).pack(self.geomnum))
            return fo.tell()















