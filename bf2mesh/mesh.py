import os
import logging

class BF2Mesh(object):
    def __init__(self, filename=None,
            isSkinnedMesh=False, isBundledMesh=False, isStaticMesh=False, isCollisionMesh=False):
        if filename:
            self.filename = filename
            logging.debug('BF2Mesh::filename %s', filename)
            file_extension = os.path.splitext(filename)[1].lower()

            self.isSkinnedMesh = (file_extension == '.skinnedmesh')
            self.isBundledMesh = (file_extension == '.bundledmesh')
            self.isStaticMesh = (file_extension == '.staticmesh')
            self.isCollisionMesh = (file_extension == '.collisionmesh')
        else:
            self.isSkinnedMesh = isSkinnedMesh
            self.isBundledMesh = isBundledMesh
            self.isStaticMesh = isStaticMesh
            self.isCollisionMesh = isCollisionMesh
        self.isLoaded = False