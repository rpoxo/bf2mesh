import os
import modmesh

import tests.mock_mesh as mocks

pbox = mocks.Box()
vbox = pbox.vmesh
vbox.save('generated/generated_box/meshes/generated_box.staticmesh')