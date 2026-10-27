# Quantum Lunar Edge Detection — NEQR

An independent NEQR live quantum edge-detection variant of [the original QPIE system](https://github.com/SamradhSahni/Quantum_Lunar_Edge_Detection), based on commit `32f49ddf9752a7152508e87f08200f59ec3eb199`. The original repository is unchanged. This repository preserves its Git history and attribution. It is an independent history-preserving copy rather than a GitHub-network fork, because the FRQI variant already occupies the personal account’s fork in that network.

NEQR uses eight position qubits plus eight binary intensity qubits (256 brightness levels), for 16 qubits per 16x16 block. Every integer grayscale value from 0 to 255 is preserved exactly. The state is a uniform superposition of |intensity_i>|position_i>. Position-register Hadamard interference gives p = 0 for equal neighboring intensities and p = 1/N for different values, after summing the intensity register. The runner estimates N p as an inequality signal, not an intensity-gradient magnitude. Historical four-bit results retain their original precision and are not eight-bit results. No measured-image reconstruction or classical gradient supplies the quantum edge map. The 16-qubit statevector is 16 times larger than the prior 12-qubit configuration.

## Quantum Studio: individual-shot circuit visualizer

Open `visualization/circuit-studio/index.html` in a browser, or open it from the live detector. The offline simulator steps through every gate of an individual shot, showing complex amplitudes, probabilities, local Bloch vectors, measurement collapse, and shot counts. It includes Bell, GHZ, phase-interference, QPIE, and a 15-operation quantum-teleportation example with intermediate measurements and classical X/Z feed-forward. The studio is an ideal simulator for 1–6 qubits; it is separate from NEQR inference.

Run `node --test visualization/circuit-studio/test-simulator.cjs` to verify its state evolution and measurement branches. The teleportation preset transfers Alice's arbitrary complex state to Bob in every one of its four measurement branches; its final verification measurement is always zero.

## Run locally

Prerequisites: Git, **64-bit Python 3.12** (the tested version), and internet access for packages and the default dataset. Clone this repository and enter its directory first:

```powershell
git clone https://github.com/Anantgoel2005/Quantum_Lunar_Edge_Detection_NEQR.git
cd Quantum_Lunar_Edge_Detection_NEQR
```

Confirm `python --version` reports Python 3.12. No environment activation, quantum account, API key or GPU is required; inference uses the local ideal Aer simulator.

Eight-bit NEQR simulates 16 qubits per 16×16 block and creates large preparation exports. Start with a small upload (for example 16×16); full 512×512 inference can take considerable CPU time. Historical four-bit benchmarks are not eight-bit results.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-real-case.txt
.\.venv\Scripts\python.exe data/sombench/fetch_case.py --row 0 --revision 20f800becb64a0c7ad314652a683f97f0281fe67
.\.venv\Scripts\python.exe visualization/build_real_case_view.py
.\.venv\Scripts\python.exe visualization/real_case_server.py
```

After setup, `./start_service.ps1` rebuilds the view and starts the service.

Keep the server terminal open; press **Ctrl+C** to stop it. If PowerShell blocks the launcher, use the explicit Python build/server commands above. If the port is occupied, stop the existing server or pass `--port 8771` to the server command. Each version needs its own virtual environment; QPIE uses port 8766, FRQI 8768 and NEQR 8769.

On macOS/Linux, use `python3.12 -m venv .venv` and replace `.\.venv\Scripts\python.exe` with `.venv/bin/python` in the commands. These platforms have not been validated here; compatible wheels for the pinned packages are required. Raw dataset TIFFs are excluded from Git and must be downloaded by the fetch command.

Open `http://127.0.0.1:8769/`. Run the entire native 512x512 lunar tile or upload a PNG, JPEG, WebP, BMP or TIFF. Preprocessing corrects orientation/transparency, fits uploaded images within 512 pixels per side, converts to grayscale, stretches global 2–98 percentile contrast and lightly denoises them. Upload limits are 20 MB and 16 million decoded pixels/samples. Regions are processed automatically using 16x16 blocks with one-pixel halos and four directional/pair-offset circuit passes per block.

The live view includes actual gate checkpoint playback, amplitude/measurement displays, a measured edge map, an overlay, and Sobel/Canny/Robinson comparisons on the identical working input. Catalog boundary metrics appear only for the labeled lunar case. Edge coverage on uploads is not accuracy.

## Execution and scientific limits

Execution is on the local ideal Qiskit Aer simulator, not quantum hardware. Aer-native Initialize prepares the exact NEQR state; the live display shows this as a preparation block. Exported QASM decomposes that preparation into primitive gates. We do not claim that arbitrary image loading is constant time or that this prototype provides a quantum speed advantage. Native Initialize is a simulation convenience, not free state preparation on hardware.

The actual detector is `quantum/variant_circuit.py`, called by `quantum/full_image.py`. Edge maps are reconstructed only from that circuit's measured counts. Classical work handles input preparation, probability calibration, halo stitching and final Otsu thresholding. Saved statevectors are used only for inspection/animation, never for the edge output. Playback shows actual checkpoints from the first inference block in each completed batch; it is slowed playback, not a hardware gate clock.

The NEQR lunar outputs go to `results/variants/neqr8/row0/`. Historical QPIE outputs remain in `results/real_case/row0/` for attribution and reference; they are not served as NEQR outputs. Private uploads and verification fixtures remain excluded from Git. The original QPIE implementation is retained as `quantum/qpie_full_image.py` for regression tests and comparison. The inherited hybrid NEQR demonstration is a historical baseline, not this fork's live detector.

## Validation

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip install playwright
.\.venv\Scripts\python.exe visualization/verify_precision8.py --neqr-only
```

37 tests pass, including all 256 grayscale levels, one-level neighbor differences, 16-qubit measured inference, exact encoded-state checks, both axes and pair offsets, constant-intensity cancellation, halo stitching, and trace/count audit consistency. Browser validation uses installed Microsoft Edge to check eight-bit inference, preparation gates and downloads, live playback, comparison panels and mobile layout. Omit `--neqr-only` with all three servers running to verify QPIE and FRQI preparation views too. `tests/test_full_image.py` retains the original QPIE gradient-calibration tests; `tests/test_variant.py` verifies this variant's inequality operator.

## Provenance

Upstream: [SamradhSahni/Quantum_Lunar_Edge_Detection](https://github.com/SamradhSahni/Quantum_Lunar_Edge_Detection). Variant: [NEQR](https://github.com/Anantgoel2005/Quantum_Lunar_Edge_Detection_NEQR). SomBench dataset and Robbins crater catalog attribution are preserved in the run manifest and report; dataset license is CC BY 4.0. No new source-code license is introduced. See `README_QPIE_HISTORY.md` and inherited `report/` documents for the original analysis, limitations and results.


Expanded preparation is available through the app’s “Inspect expanded state preparation” link. It displays the actual representative block’s Initialize decomposition, paged into U/CX/reset gates with exact angles and full QASM/JSON downloads. Exports are regenerated for each completed input. Historical four-bit results remain in `results/variants/neqr/row0/`.
