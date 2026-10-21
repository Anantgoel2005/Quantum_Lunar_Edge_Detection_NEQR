"""Full grayscale precision and live 16-qubit NEQR regression checks."""
import unittest
import numpy as np
from qiskit.quantum_info import Statevector
from quantum.variant_circuit import INTENSITY_BITS,build_variant_circuit,variant_counts_to_edge_map
from quantum.full_image import run_full_image_qhed


class NEQREightBit(unittest.TestCase):
    def test_all_256_intensities_are_preserved_exactly(self):
        self.assertEqual(INTENSITY_BITS,8)
        image=np.arange(256,dtype=np.uint8).reshape(16,16)
        circuit,qubits,_=build_variant_circuit(image)
        self.assertEqual(qubits,16)
        actual=np.asarray(circuit.data[0].operation.params,dtype=complex)
        expected=np.zeros(65536,complex)
        indices=np.arange(256)
        expected[(indices<<8)+indices]=1/16
        np.testing.assert_array_equal(actual,expected)
        self.assertEqual(circuit.metadata['intensity_qubits'],8)
        self.assertEqual(circuit.metadata['qubit_roles'][-1],'intensity bit 7')

    def test_one_level_change_is_no_longer_merged(self):
        image=np.array([[100,101],[100,101]],np.uint8)
        for direction in ('horizontal','vertical'):
            maps=[]
            for offset in (0,1):
                circuit,_,_=build_variant_circuit(image,direction,offset)
                state=Statevector.from_instruction(circuit.remove_final_measurements(inplace=False))
                maps.append(variant_counts_to_edge_map(state.probabilities_dict(),image.shape,direction,offset))
            expected=np.zeros((2,2))
            if direction=='horizontal':expected[:,1]=.25
            np.testing.assert_allclose(np.maximum(*maps),expected,atol=1e-12)

    def test_live_tile_metadata_and_measured_one_level_edge(self):
        image=np.array([[100,101]],np.uint8)
        maps,metadata,_=run_full_image_qhed(image,tile_size=16,shots=8192,batch_tiles=1,seed=42)
        self.assertEqual(metadata['intensity_bits'],8)
        self.assertEqual(metadata['qubits_per_circuit'],16)
        self.assertEqual(metadata['circuits_executed'],4)
        self.assertEqual(metadata['measurement_shots'],32768)
        self.assertEqual(maps['strength'][0,0],0)
        self.assertGreater(maps['strength'][0,1],0)


if __name__=='__main__':unittest.main()
