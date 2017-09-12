import struct

def int(fo):
    fmt = 'i'
    size = struct.calcsize(fmt)
    return struct.Struct(fmt).unpack(fo.read(size))[0]


def float(fo):
    fmt = 'f'
    size = struct.calcsize(fmt)
    return struct.Struct(fmt).unpack(fo.read(size))[0]


def float3(fo):
    fmt = '3f'
    size = struct.calcsize(fmt)
    return tuple(struct.Struct(fmt).unpack(fo.read(size)))


def long(fo):
    fmt = 'l'
    size = struct.calcsize(fmt)
    return struct.Struct(fmt).unpack(fo.read(size))[0]


def short(fo):
    fmt = 'h'
    size = struct.calcsize(fmt)
    return struct.Struct(fmt).unpack(fo.read(size))[0]


def string(fo, lenght=1):
    fmt = '{}s'.format(lenght)
    size = struct.calcsize(fmt)
    return struct.Struct(fmt).unpack(fo.read(size))[0]


def byte(fo):
    fmt = 'b'
    size = struct.calcsize(fmt)
    return struct.Struct(fmt).unpack(fo.read(size))[0]

# copypasta from DX SDK 'Include/d3d9types.h' enum _D3DDECLTYPE to address vert attribute vartype variable
d3dtypes_lenght = {
    0 : 1, # D3DDECLTYPE_FLOAT1    =  0,  // 1D float expanded to (value, 0., 0., 1.)
    1 : 2, # D3DDECLTYPE_FLOAT2    =  1,  // 2D float expanded to (value, value, 0., 1.)
    2 : 3, # D3DDECLTYPE_FLOAT3    =  2,  // 3D float expanded to (value, value, value, 1.)
    4 : 1, # D3DDECLTYPE_D3DCOLOR  =  4,  // 4D packed unsigned bytes mapped to 0. to 1. range
    5 : 3, # D3DDECLTYPE_UBYTE4    =  5,  // 4D unsigned byte
    17 : 0, # D3DDECLTYPE_UNUSED = 17, // When the type field in a decl is unused.
    }

d3dtypes = {
    0 : 'FLOAT1',
    1 : 'FLOAT2',
    2 : 'FLOAT3',
    4 : 'D3DCOLOR',
    5 : 'UBYTE4',
    17 : 'UNUSED',
    }

# copypasta from DX SDK 'Include/d3d9types.h' enum _D3DDECLUSAGE to address vert attribute usage variable
d3dusage = {
    0 : 'POSITION',
    1 : 'BLENDWEIGHT',
    2 : 'BLENDINDICES',
    3 : 'NORMAL',
    4 : 'PSIZE',
    5 : 'UV1', # TEXCOORD in d3d enums
    6 : 'TANGENT',
    7 : 'BINORMAL',
    8 : 'TESSFACTOR',
    9 : 'POSITIONT', # wat
    10 : 'COLOR',
    11 : 'FOG',
    12 : 'DEPTH',
    13 : 'SAMPLE',
    # bf2 enums much larger than dx to avoid collisions?
    261 : 'UV2',
    517 : 'UV3',
    773 : 'UV4',
    }






