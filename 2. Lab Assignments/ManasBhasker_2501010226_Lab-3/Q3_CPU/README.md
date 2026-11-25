# Q3 – CPU.hdl

Load `CPU.hdl` in the Hardware Simulator (Project 5 folder), then run the **supplied** scripts
`CPU.tst` (with `CPU.cmp`) and `CPU-external.tst` (with `CPU-external.cmp`) from the nand2tetris
project 5 download — those are the "supplied CPU test ROMs". Screenshot the
"End of script – Comparison ended successfully" message for your report.

Needs built-in/own chips: Mux16, ARegister, DRegister, ALU, PC, And, Or, Not.

Control word summary
| Signal | Source |
|---|---|
| A mux select | instruction[15] (C-instr → ALU out, A-instr → instruction) |
| loadA | !i15 OR d1 (bit 5) |
| loadD | i15 AND d2 (bit 4) |
| writeM | i15 AND d3 (bit 3) |
| ALU y select | a-bit (bit 12): 0 → A, 1 → M |
| ALU ctrl | bits 11..6 |
| jump | i15 AND ((j1·ng) + (j2·zr) + (j3·!ng·!zr)) |
