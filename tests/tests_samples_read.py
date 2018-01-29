import unittest
import os

import modmesh

class TestSamplesReading(unittest.TestCase):

    def setUp(self):
        self.path_object_samples = os.path.join(*['tests', 'samples', 'evil_box', 'meshes', 'evil_box.samples'])

    def test_can_read_header(self):
        with open(self.path_object_samples, 'rb') as samplefile:
            sample = modmesh.StdSample()
            sample._read_head(samplefile)

        self.assertTrue(sample.fourcc == b'SMP2')
        self.assertTrue(sample.width == 256)
        self.assertTrue(sample.height == 256)

    def test_can_read_smp_samples(self):
        with open(self.path_object_samples, 'rb') as samplefile:
            sample = modmesh.StdSample()
            sample._read_data(samplefile)

        self.assertTrue(sample.datanum == sample.width * sample.height)
        self.assertTrue(len(sample.data) == sample.datanum)
        self.assertTrue(isinstance(sample.data[0], modmesh.smp_sample))

    def test_can_read_smp_faces(self):
        with open(self.path_object_samples, 'rb') as samplefile:
            sample = modmesh.StdSample()
            sample._read_faces(samplefile)

        self.assertTrue(sample.facenum == 12)
        self.assertTrue(len(sample.faces) == sample.facenum)
        self.assertTrue(isinstance(sample.faces[0], modmesh.smp_face))
    
    def test_can_load_samplefile(self):
        sample = modmesh.LoadBF2Sample(self.path_object_samples)
        self.assertTrue(isinstance(sample, modmesh.StdSample))

    def test_can_load_bf2_mesh_with_samples(self):
        meshpath = self.path_object_samples.replace('.samples', '.staticmesh')
        vmesh = modmesh.LoadBF2Mesh(meshpath, loadSamples=True)
        self.assertTrue(isinstance(vmesh.geoms[0].lods[0].sample, modmesh.StdSample))


if __name__ == '__main__':
    unittest.main()