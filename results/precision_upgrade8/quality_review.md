# Eight-bit NEQR and expanded preparation review

The user explicitly requested eight brightness qubits instead of four in the current NEQR edge detector, then added actual expanded preparation circuits for each QPIE, FRQI and NEQR case. The implementation changes the live NEQR configuration to 8-bit brightness, preserves historical 4-bit results, and adds source-derived preparation viewers to all three apps.

## Plan and implementation checkpoints

Jev reviewed the precision upgrade plan and the added preparation-view scope. Both returned generic investigate signals about requirements clarity and evidence sufficiency, with no specific concerns. Scope was made concrete: 16 qubits per 16×16 NEQR block; exhaustive preservation of all 256 grayscale values; a separate neqr8 output directory; actual decomposition of the representative first block; full downloads, gate selection, angle inspection and paging rather than an unexplained preparation box.

The actual code diff and new helper/viewer/tests were reviewed at implementation. Jev returned investigate for generic requirement coverage (0.62), regression risk (0.47) and unnecessary changes (0.30), with no concrete defect. Targeted investigation covered integer quantization, actual measured uploads, source/asset consistency, stale output prevention, preparation-prefix state equivalence, browser behavior and independent count replay.

The live encoder now uses INTENSITY_BITS=8 and multiplies before dividing in its quantizer. The previous floating-point order could floor a value slightly below an exact grayscale integer. The new exhaustive test prepares all 256 levels and checks their exact basis-state locations. A 100→101 neighbor change now survives encoding. The operator remains inequality, not contrast magnitude.

NEQR writes to results/variants/neqr8/row0; historical four-bit output remains in results/variants/neqr/row0. The saved prechange encoder source matches the hash in the original frozen four-bit BSDS protocol. Historical benchmark scores and the old circuit atlas are not reinterpreted as eight-bit results; the atlas is marked as a historical NEQR snapshot.

The actual representative inference circuit was already transpiled to U/CX. The new exporter takes its prefix before the first barrier, writes all U/CX/reset instructions and precise parameters, and excludes the subsequent edge shift/H/measurement. It does not alter image inference. The first default block may also be exported separately without full-image detection; this is marked example_only in metadata and on screen. Completed uploads regenerate their own exports and input hashes.

The new viewer shows twenty primitive instructions per page, every qubit wire, exact selected rotation angles, page navigation and full preparation QASM/JSON downloads. It describes the circuit as an equivalent decomposition of native Initialize, not per-gate hardware telemetry. For the default sample, QPIE has 510 preparation instructions, FRQI 1,022 and eight-bit NEQR 131,070. These are sample/compiler-specific, unoptimized primitive counts, not universal resource bounds.

## Measured verification

- Full NEQR unit suite: 37 tests passed in 22.503 seconds. This includes the three new eight-bit precision/inference tests and two preparation-export tests.
- Preparation-export tests reconstruct the exported U/CX/reset gate list and verify that it prepares the native Initialize state, up to global phase. Export without a preparation barrier is rejected.
- Browser testing passed for all three viewers: 8 QPIE qubits, 9 FRQI qubits, 16 NEQR qubits, page movement, last-page gate selection, exact angle display, full-download digests and current input hashes. Desktop/mobile layouts passed with no JavaScript page errors.
- An actual 16×16 NEQR upload completed using 16 circuits, 131,072 shots, 8 brightness bits and 16 total qubits. All four recorded trace circuits have 16 qubits and eight brightness bits. The amplitude grid renders sparse nonzero entries over one background instead of over 131,000 rectangles.
- Additional new uploads in QPIE and FRQI also regenerated preparation exports. Independent measurement replay checked 48 circuits and 393,216 shots across all three cases. Maximum discrepancy was zero for QPIE/NEQR and 7.105427357601002e-15 for FRQI.
- Shared viewer/helper source bytes match across all three repositories. Compilation and whitespace checks passed. Screenshots were visually inspected for actual gates, readable parameters and correct 16-qubit labels.

## Issues found and repaired

The browser test initially dispatched a synthetic input-change event followed by a click; the ensuing native blur change redrew the selected gate. The test was corrected to perform the real blur interaction. Gate selection then passed.

The download-digest check found a real Windows newline issue: write_text translated QASM LF characters to CRLF while the digest was computed on LF bytes. The exporter now writes the exact UTF-8 bytes being hashed. All three existing exports were normalized to those bytes, and the preparation-export tests were rerun successfully (2 tests in 0.423 seconds) with an added byte-digest assertion.

One source-copy helper initially omitted an explicit UTF-8 read and failed before mutation. It was rerun with UTF-8; shared-source equality was verified afterward.

## Limits

The full 512×512 lunar image has not been rerun at eight-bit precision during this change; actual inference was verified on a small uploaded image using the normal 16×16 block size and shot budget. Native default preparation examples are real first-block decompositions, explicitly labeled as examples. Preparation viewing does not execute a gate-by-gate hardware preparation or provide snapshots after each decomposed gate. The live backend remains ideal Aer simulation. Four-bit versus eight-bit model quality has not been benchmarked by this change.

Jev verification and delivery results are appended after final checks. Raw checkpoint responses and measured JSON/log evidence are retained beside this review.

Jev verification returned investigate for generic relevance (0.79) and missing-check (0.52) uncertainty, with claim support 0.87 and no concrete concerns. Targeted follow-up reconstructed fresh exported primitive lists for all three families on an asymmetric 2×2 image with a vertical shifted edge circuit. QPIE, FRQI and eight-bit NEQR exports all prepare the native Initialize state up to global phase, with numerical fidelity within 3.6e-14 of one. Their QASM byte digests match. This separately exercises each encoding's prefix boundary and parameter serialization. See preparation_state_qpie.json, preparation_state_frqi.json and preparation_state_neqr.json.

All three servers were returned to their native 512×512 default image contexts. Final HTTP checks confirm current QPIE/FRQI/NEQR preparation widths 8/9/16 and NEQR eight-bit brightness. The fresh NEQR default is ready/idle with correctly labeled first-block preparation examples, rather than displaying old four-bit inference as new. Each default preparation input hash matches the served native image. See final_readiness.json. The verification follow-up is retained; no more than two cycles were used.

The verification follow-up still returned generic investigate signals for check relevance (0.76) and missing checks (0.46), with claim support 0.83 and no specific concerns. These unexplained advisory uncertainties remain unresolved; no Jev pass is claimed. Native 512×512 eight-bit inference and eight-bit-versus-four-bit quality benchmarking remain outside the measured checks in this change.

Jev delivery reviewed the actual final response and measured results, returning generic investigate signals for completeness (0.70), claim support (0.70) and formatting (0.61), with no concrete concerns. Final targeted inspection confirmed all four response HTTP links return 200, all current encoding widths and NEQR brightness bits match live metadata, and the final list/paragraph formatting is valid. The response claims only the measured unit/browser/small-upload/replay results and identifies the preparation as a representative block decomposition. Generic service uncertainty is retained rather than reported as a pass. See jev_delivery.json and final_response_verification.json.
