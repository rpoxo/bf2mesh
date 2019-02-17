import struct 
import logging

def read_int(fo, lenght=1):
    fmt = '{}i'.format(lenght)
    size = struct.calcsize(fmt)

    unpacked = struct.Struct(fmt).unpack(fo.read(size))
    if lenght==1: return unpacked[0]
    return unpacked

def read_float(fo, lenght=1):
    fmt = '{}f'.format(lenght)
    size = struct.calcsize(fmt)

    unpacked = struct.Struct(fmt).unpack(fo.read(size))
    if lenght==1: return unpacked[0]
    return unpacked

def read_float3(fo):
    fmt = '3f'
    size = struct.calcsize(fmt)

    return tuple(struct.Struct(fmt).unpack(fo.read(size)))

def read_long(fo, lenght=1):
    fmt = '{}l'.format(lenght)
    size = struct.calcsize(fmt)

    unpacked = struct.Struct(fmt).unpack(fo.read(size))
    if lenght==1: return unpacked[0]
    return unpacked

def read_short(fo, lenght=1):
    fmt = '{}H'.format(lenght)
    size = struct.calcsize(fmt)

    unpacked = struct.Struct(fmt).unpack(fo.read(size))
    if lenght==1: return unpacked[0]
    return unpacked

def read_string(fo):
    lenght = read_long(fo)
    fmt = '{}s'.format(lenght)
    size = struct.calcsize(fmt)

    unpacked = struct.Struct(fmt).unpack(fo.read(size))
    return unpacked[0]

def read_byte(fo, lenght=1):
    fmt = '{}b'.format(lenght)
    size = struct.calcsize(fmt)

    unpacked = struct.Struct(fmt).unpack(fo.read(size))
    if lenght==1: return unpacked[0]
    return unpacked
    
def read_matrix4(fo):
    fmt = '4f'
    size = struct.calcsize(fmt)

    unpacked = [
        struct.Struct(fmt).unpack(fo.read(size)),
        struct.Struct(fmt).unpack(fo.read(size)),
        struct.Struct(fmt).unpack(fo.read(size)),
        struct.Struct(fmt).unpack(fo.read(size))
    ]
    return unpacked
    

def write_long(fo, value):
    fmt = 'l'
    fo.write(struct.Struct(fmt).pack(value))

def write_short(fo, value):
    fmt = 'H'
    fo.write(struct.Struct(fmt).pack(value))

def write_float3(fo, v1, v2, v3):
    fmt = '3f'
    fo.write(struct.Struct(fmt).pack(v1, v2, v3))

def write_byte(fo, value):
    fmt = 'b'
    fo.write(struct.Struct(fmt).pack(value))

def write_float(fo, value):
    fmt = 'f'
    try:
        fo.write(struct.Struct(fmt).pack(value))
    except struct.error as e:
        logging.error('failed to write %s value as float' % value)
        raise e

def write_matrix4(fo, value):
    fmt = '4f'

    for row in range(4):
        fo.write(struct.Struct(fmt).pack(*value[row]))

def write_string(fo, value):
    lenght = len(value)
    fmt = '{}s'.format(lenght)
    fo.write(struct.Struct('l').pack(lenght))
    fo.write(struct.Struct(fmt).pack(value))