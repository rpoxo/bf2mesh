import struct 

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

def read_string(fo, offset, lenght=1):
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