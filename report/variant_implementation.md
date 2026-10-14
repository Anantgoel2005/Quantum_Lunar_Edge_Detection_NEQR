# NEQR live variant

NEQR uses eight position qubits plus four binary intensity qubits by default (16 brightness levels), for 12 qubits per 16x16 block. Pixel values are quantized as floor(15 I/255). The state is a uniform superposition of |quantized_intensity_i>|position_i>. Position-register Hadamard interference gives p = 0 when adjacent quantized values agree, and p = 1/N when they differ, after summing over the intensity register. The runner estimates N p as an inequality signal. It does not compute an intensity-gradient magnitude. No measured image reconstruction or classical gradient supplies the quantum edge map. Four-bit precision is an explicit tradeoff for live simulation; INTENSITY_BITS in quantum/variant_circuit.py can be set to 8 for 16 encoding qubits, with higher simulation and trace costs.

The original QPIE system and its saved results are retained as historical baselines. All variant edge evidence is measured from actual Aer inference circuits. Four passes cover both axes and pair offsets. The state preparation is native Initialize in simulation, with primitive export available.

Validation: 32 unit tests and an end-to-end browser upload run pass. Each uploaded-image check executes 140 actual inference circuits and 1,146,880 shots.

Native lunar validation: all 512x512 pixels, 5,476 inference circuits, 44,859,392 shots, 86 checkpoint batches; all trace counts agree with the inference audit. Desktop and 360px mobile views have no script errors or horizontal overflow. Saved screenshots and the verification JSON are in the variant output directory.
