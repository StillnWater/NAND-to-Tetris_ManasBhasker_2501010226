# Lab 3 – CPU Architecture and Diagnostic Testing (Nand to Tetris I)

| Folder | Question | Tool |
|---|---|---|
| Q1_assembly | Arithmetic / Branching / Loop `.asm` + `.tst` scripts + expected output | CPU Emulator (Project 4) |
| Q2_hand_encoding | Two programs, `.hack`, field-by-field breakdown (encoding.md) | paper / assembler to check |
| Q3_CPU | `CPU.hdl` | Hardware Simulator (Project 5) |
| Q4_Computer | `Memory.hdl`, `Computer.hdl`, Add/Max/Rect `.asm`+`.hack`+`.tst` | Hardware Simulator |
| Q5_trace | Fetch-Decode-Execute trace, 3 consecutive instructions | manual |
| tools | `hack_asm.py` (assembler), `hack_emu.py` (reference emulator) | Python 3 |

## How to run
- **Q1:** open CPU Emulator → load each `.tst`. Compare with `expected_output.txt`.
- **Q3:** put `CPU.hdl` in your Project 5 folder with your Project 1-3 chips (ALU, PC, ARegister, DRegister, Mux16...). Run the official `CPU.tst` and `CPU-external.tst`.
- **Q4:** copy `Memory.hdl`, `Computer.hdl`, the `.hack` files and `.tst` files to the same folder. Load each `ComputerXxx.tst`, run, screenshot. `Max` and `Add` print values you can compare to `expected_output.txt`; `Rect` should fill the first 3 rows of the screen (RAM[0]=3).
- Official `Add.hack` / `Max.hack` / `Rect.hack` from the course also work, so you can swap them in.

## Notes
- Expected values were produced by my own Python reference emulator, not the official simulator — confirm in the real tools before submitting and take your own screenshots.
- No `.cmp` files are included for the Computer tests; use the official ones if you have them (add `compare-to` back into the `.tst`).
- Push all this into the `Lab 3` folder of your GitHub repo.
