"""Exported gate list must prepare the real native image state, not the edge state."""
import json
import hashlib
from pathlib import Path
import tempfile
import unittest
import numpy as np
from PIL import Image
from qiskit import QuantumCircuit,transpile
from qiskit.quantum_info import Statevector
from quantum.variant_circuit import build_variant_circuit
from visualization.state_preparation import export_preparation


class PreparationExport(unittest.TestCase):
    def test_export_is_actual_preparation_prefix_and_state(self):
        image=np.array([[0,85],[170,255]],np.uint8)
        native,_,_=build_variant_circuit(image,'horizontal',1)
        compiled=transpile(native,basis_gates=['u','cx'],optimization_level=0,seed_transpiler=42)
        with tempfile.TemporaryDirectory() as name:
            output=Path(name);Image.fromarray(image).save(output/'input.png')
            data=export_preparation(compiled,output,{'tile_size':2,'encoding':'NEQR','subtract_tile_min':False})
            self.assertEqual(data['qubits'],10)
            self.assertEqual(data['brightness_qubits'],8)
            self.assertEqual(len(data['roles']),10)
            self.assertNotIn('measure',data['counts'])
            restored=QuantumCircuit(data['qubits'])
            for gate,qubits,parameters in data['gates']:
                if gate=='u':restored.u(*parameters,qubits[0])
                elif gate=='cx':restored.cx(*qubits)
                elif gate=='reset':restored.reset(qubits[0])
                else:self.fail('Unexpected primitive')
            prepared=native.copy();prepared.data=prepared.data[:1]
            self.assertTrue(Statevector.from_instruction(prepared).equiv(Statevector.from_instruction(restored),atol=1e-10))
            self.assertEqual(data,json.loads((output/'state_preparation.json').read_text()))
            self.assertTrue((output/'state_preparation.qasm').read_text().startswith('OPENQASM 3.0;'))
            self.assertEqual(hashlib.sha256((output/'state_preparation.qasm').read_bytes()).hexdigest(),data['qasm_sha256'])

    def test_unmarked_prefix_is_rejected(self):
        circuit=QuantumCircuit(2);circuit.h(0)
        with tempfile.TemporaryDirectory() as name:
            with self.assertRaises(ValueError):export_preparation(circuit,name,{'tile_size':2})


if __name__=='__main__':unittest.main()
