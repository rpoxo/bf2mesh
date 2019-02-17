import math
from math import sin, cos, radians, degrees


vertex = (5.0, 0.0, 5.0)
rotation = (90.0, 0.0, 0.0)

# rotate around forward(blue) axis
# roll
def Rx(position, angle):
    x = position[0]
    y = position[1]
    z = position[2]

    newX = x;
    newY = y*cos(angle) - z*sin(angle);
    newZ = y*sin(angle) + z*cos(angle);
    
    return (newX, newY, newZ)


# rotate around vertical(green) axis
# yaw
def Ry(position, angle):
    x = position[0]
    y = position[1]
    z = position[2]

    newX = x*cos(angle) + z*sin(angle);
    newY = y;
    newZ = z*cos(angle) - x*sin(angle);
    
    return (newX, newY, newZ)

# rotate around side(red) axis
# pitch
def Rz(position, angle):
    x = position[0]
    y = position[1]
    z = position[2]

    newX = x*cos(angle) - y*sin(angle);
    newY = x*sin(angle) + y*cos(angle);
    newZ = z
    
    return (newX, newY, newZ)


def rotate_X(position, rotation):
    yaw = radians(rotation[0])
    pitch = rotation[1]
    roll = rotation[2]
    
    angle = yaw
    
    new_position = (Rx(Ry(Rz(position, angle), angle), angle))
    print(new_position)
    
    
    
result = rotate_X(vertex, rotation)
print(result)