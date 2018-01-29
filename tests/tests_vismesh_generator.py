import unittest
import copy
import os

import modmesh
from modmesh import D3DDECLTYPE, D3DDECLUSAGE

import tests.mock_mesh as mock_mesh

class TestVisMeshVertexGenerator(unittest.TestCase):
    
    def test_can_serialize_vertices(self):
        vmesh = mock_mesh.Box()
        vertsize = int(vmesh.vertstride / vmesh.vertformat)
        #vmesh.save('./mockbox.staticmesh')
        
        v_id = 0
        for vertex in vmesh.get_vertices():
            for attrib in vmesh.vertattrib:
                flag = attrib.flag
                offset = int(attrib.offset / vmesh.vertformat)
                vartype = D3DDECLTYPE(attrib.vartype)
                usage = D3DDECLUSAGE(attrib.usage)
                
                self.assertTrue(hasattr(vertex, usage.name))
                value = getattr(vertex, usage.name)
                self.assertTrue(len(value) == len(vartype))
                
                vstart = v_id * vertsize
                datastart = vstart + offset
                datalenght = len(vartype)
                vdata = vmesh.vertices[datastart:datastart + datalenght]
                self.assertEqual(value, vdata)

            v_id += 1
        self.assertEqual(v_id, vmesh.vertnum)
    
    def test_can_deserialize_materials_vertices(self):
        vmesh = mock_mesh.Box()
        vmesh_clone = mock_mesh.Box()
        
        vertices = [vertex for vertex in vmesh.get_vertices()]
        new_vertices = []
        for id_geom, geom in enumerate(vmesh.geoms):
            for id_lod, lod in enumerate(geom.lods):
                for id_mat, material in enumerate(lod.materials):
                    for vertex in vertices[material.vstart:material.vstart + material.vnum]:
                        new_vertices.append(vertex)
        
        vmesh.update_vertices(vertices)
        self.assertEqual(vmesh.vertices, vmesh_clone.vertices)

    def test_can_deserialize_materials_vertices_pavement(self):
        path_pavement = os.path.join(*['tests', 'samples', 'pavement', '24m_1', 'meshes', '24m_1.staticmesh'])
        path_pavement_clone = os.path.join(*['tests', 'generated', 'edit', 'pavement', '24m_1_clone', 'meshes', '24m_1_clone.staticmesh'])
        vmesh = modmesh.LoadBF2Mesh(path_pavement)
        vmesh_clone = modmesh.LoadBF2Mesh(path_pavement)
        
        vertex_objects = [vertex for vertex in vmesh.get_vertices()]
        vertices = []
        for id_geom, geom in enumerate(vmesh.geoms):
            for id_lod, lod in enumerate(geom.lods):
                for id_mat, material in enumerate(lod.materials):
                    for vertex in vertex_objects[material.vstart:material.vstart + material.vnum]:
                        vertices.append(vertex)
        
        vmesh.update_vertices(vertices)
        vmesh.save(path_pavement_clone)
        self.assertEqual(vmesh.vertices, vmesh_clone.vertices)
                
if __name__ == '__main__':
    unittest.main()