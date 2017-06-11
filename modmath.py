import struct


def float3(fo):
    fmt = '3f'
    size = struct.calcsize(fmt)
    return tuple(struct.Struct(fmt).unpack(fo.read(size)))


def float(fo):
    fmt = 'f'
    size = struct.calcsize(fmt)
    return struct.Struct(fmt).unpack(fo.read(size))[0]


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
