# Q3 – Flags zr / ng matter

`zr` (ALU out == 0) and `ng` (ALU out < 0) feed the jump logic: JGT = !ng&!zr, JEQ = zr, JLT = ng, JGE = !ng, JNE = !zr, JLE = ng|zr.

## Case A – loop exit with `D;JGT` (FlagDemo.asm, RAM[0]=3)

- **none** (correct logic): RAM[0]=0, RAM[1]=3 (iterations; correct = 3)
- **jgt_incl_zero** (bug: JGT forgets zr (treats 0 as positive)): RAM[0]=-1, RAM[1]=4 (iterations; correct = 3)
- **ng_stuck0** (bug: ng stuck at 0 (negatives look positive)): RAM[0]=0, RAM[1]=3 (iterations; correct = 3)

## Case B – `D;JEQ` skip (Skip.asm)

- **none** (correct): RAM[1]=0 (correct = 0, the `M=-1` must be skipped)
- **zr_stuck0** (bug: zr never set): RAM[1]=-1 (correct = 0, the `M=-1` must be skipped)

## What goes wrong
- A: if zr is ignored for JGT, the loop jumps once more when n reaches 0, runs again, n becomes -1 (ng=1) and only then stops → off-by-one extra iteration. Real code: wrong loop counts, buffer over-runs by one element (classic off-by-one / bounds bug).
- B: with zr stuck at 0, `JEQ` never fires, so code guarded by a comparison executes anyway.
- With ng stuck at 0 the n=3 demo still looks correct (counter never goes negative) — the bug stays hidden until a test uses a negative value, e.g. run FlagDemo with RAM[0]=-2: a correct CPU exits after 1 iteration, the buggy one keeps looping.

## Demonstrate in the simulator
`CPU_buggy.hdl` differs from `CPU_correct.hdl` in one line (jEQ uses `ng` instead of `zr`). Load each
with Computer.hdl, run `Skip.hack`, compare RAM[1] after ~14 cycles.

Waveforms: `python tools/hack_wave.py Q3_flags/Skip.asm --cycles 12 --png Q3_flags/wave_correct.png` and
`... --bug zr_stuck0 --png Q3_flags/wave_buggy.png` (note jump signal and PC next on the `D;JEQ` cycle).
