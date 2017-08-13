import os
import modmesh

import tests.mock_mesh as mocks

pbox = mocks.Box()
vbox = pbox.vmesh
vbox.write_file_data('generated/generated_box/meshes/generated_box.staticmesh')