# Q2 – Fetch / Decode / Execute timing

The Hack CPU is **single-cycle**: one instruction per clock cycle (tick + tock). Inside one cycle:

| Phase | When it completes | What happens |
|---|---|---|
| Fetch | Early in the cycle, as soon as PC is stable (after the previous tock) | `ROM32K[pc]` is combinationally read → `instruction` |
| Decode | Immediately after fetch, still in the same cycle | bits 15/12/11-6/5-3/2-0 become control signals (loadA, loadD, writeM, ALU controls, jump logic) |
| Execute | ALU result settles during the high phase (tick); results are **committed on the falling edge (tock)** | A/D/RAM written, PC ← PC+1 or jump target |

So all three phases of instruction *n* finish in clock cycle *n*; the visible state change (A, D, M, PC) appears
**after the tock of that cycle**. The next fetch starts with the new PC at cycle n+1.

## Three instructions from Sample.asm (see Q1_waveform/trace_table.md)

| Instr | Fetch done | Decode done | Execute done (state committed) |
|---|---|---|---|
| `@5`  (PC 0) | cycle 1 (tick) | cycle 1 | end of cycle 1 → A=5, PC=1 |
| `D=A` (PC 1) | cycle 2 (tick) | cycle 2 | end of cycle 2 → D=5, PC=2 |
| `@3`  (PC 2) | cycle 3 (tick) | cycle 3 | end of cycle 3 → A=3, PC=3 |

In the Hardware Simulator: after `tick` the new `instruction`/ALU outputs are visible; after `tock` ARegister/DRegister/PC/RAM
show the committed values. Take a screenshot per half-cycle for your report.
