
from .visiblemesh import VisibleMesh

class BundledMesh(VisibleMesh):
    def __init__(self, filename):
        VisibleMesh.__init__(self, filename, isBundledMesh=True)