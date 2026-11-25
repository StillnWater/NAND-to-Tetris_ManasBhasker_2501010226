# Lab 4 – Waveform Analysis and Instruction Cycle (Nand to Tetris I)

| Folder | Question | Contents |
|---|---|---|
| Q1_waveform | 5+ cycle ALU/control trace | `Sample.asm/.hack`, `ComputerWave.tst`, `trace_table.md`, `waveform_sample.png` |
| Q2_timing | Fetch/Decode/Execute timing | `timing.md` |
| Q3_flags | zr/ng criticality + buggy logic | `FlagDemo.asm`, `Skip.asm`, `CPU_correct.hdl`, `CPU_buggy.hdl`, `flags.md`, waveforms |
| Q4_io | I/O program + memory-mapped I/O | `IO.asm/.hack`, `ComputerIO.tst`, `io_trace.md` |
| Q5_toolchain | Hack vs real toolchain | `toolchain.md` (with Mermaid), `toolchain_diagram.png` |
| tools | | `hack_asm.py`, `hack_wave.py` (tracer + waveform plotter) |

Run (Python 3 + matplotlib): `python tools/hack_wave.py Q1_waveform/Sample.asm --cycles 10 --png out.png`

Notes
- The stock Hardware Simulator has no real waveform viewer; the `.tst` scripts log pins per tick/tock for screenshots,
  and `hack_wave.py` draws the waveforms. Be upfront about this in your report.
- Values come from my Python model of the Hack CPU, not the official simulator. Confirm in the real tools
  (needs your Lab 3 `Computer.hdl`) and take your own screenshots.
- Q3 `CPU_buggy.hdl` needs your Project 5 chips in the same folder, like Lab 3.
