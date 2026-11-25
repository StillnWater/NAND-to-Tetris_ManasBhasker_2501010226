# Q1 – Waveform / signal trace

Honest note: the stock Nand2Tetris Hardware Simulator has no true waveform viewer — it shows pin values
step by step and writes them to an `.out` file. Two ways to cover this question:
1. Run `ComputerWave.tst` in the Hardware Simulator (tick/tock logged separately, so you can see values
   before and after each clock edge) and screenshot it.
2. Use `tools/hack_wave.py` to get a real waveform picture: `waveform_sample.png` + `trace_table.md`
   (10 cycles of Sample.asm, each cycle annotated with its instruction).

Regenerate: `python tools/hack_wave.py Q1_waveform/Sample.asm --cycles 10 --png waveform_sample.png`

Table columns: A, D, M(in) are values *during* the cycle (before the falling edge commits the result).
ALU out / zr / ng show `-` for A-instructions (ALU output is ignored since writeM=0, D/A not loaded from it).
