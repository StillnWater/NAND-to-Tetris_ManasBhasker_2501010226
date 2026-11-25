# Nand to Tetris Capstone - Make the Computer Draw a Box

- Roll no: 2501010226  ->  **K = 26**
- Box: starts at row 26, 20 rows tall, 48 px wide (16 x ((26 mod 4)+1) = 16 x 3)
- Extra assembler feature: K mod 3 = 2 -> warning on duplicate labels

## Layout
| Path | What |
|---|---|
| `hdl/CPU.hdl, Memory.hdl, Computer.hdl` | Part A (load into the Hardware Simulator) |
| `assembler.py` | Part B, two-pass Hack assembler |
| `Box.asm`, `Box.hack` | Part C, box program + output of *my* assembler |
| `asm/` | Add, Max, Rect sources and their .hack output |
| `tests/test_all.py` | Python self-checks (assembler + Box simulation) |
| `report/` | Report draft |


## Usage
    python assembler.py Box.asm Box.hack
    python tests/test_all.py
