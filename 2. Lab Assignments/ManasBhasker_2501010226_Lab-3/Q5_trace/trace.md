# Q5 – Fetch-Decode-Execute trace (program: Add.asm)

```
0: @2      0000000000000010
1: D=A     1110110000010000
2: @3      0000000000000011
3: D=D+A   1110000010010000
4: @0      0000000000000000
5: M=D     1110001100001000
```
Start: A=0, D=0, PC=0, RAM[0]=0. (M = RAM[A], so "M" below is RAM at the address currently in A.)

## Three consecutive instructions (instructions 1-3)

| Step | Fetch (ROM[PC]) | Decode | Execute | A | D | M | PC after |
|---|---|---|---|---|---|---|---|
| 1 | ROM[0] = `0000000000000010` | bit15=0 → A-instruction, value 2 | A ← 2 | 2 | 0 | 0 | 1 |
| 2 | ROM[1] = `1110110000010000` | bit15=1 → C-instr; a=0, comp=`110000` (A), dest=`010` (D), jump=`000` | D ← A = 2 | 2 | 2 | 0 | 2 |
| 3 | ROM[2] = `0000000000000011` | A-instruction, value 3 | A ← 3 | 3 | 2 | 0 | 3 |

## Remaining steps (for completeness)

| Step | Instruction | A | D | M | PC after |
|---|---|---|---|---|---|
| 4 | `D=D+A` (comp=`000010`, dest=`010`) | 3 | 5 | 0 | 4 |
| 5 | `@0` | 0 | 5 | 0 | 5 |
| 6 | `M=D` (comp=`001100`, dest=`001`) | 0 | 5 | 5 | 6 |

Raw emulator trace (tools/hack_emu.py):
```
  1 | 0000000000000010 | A=     2 D=     0 M=     0 PC=1
  2 | 1110110000010000 | A=     2 D=     2 M=     0 PC=2
  3 | 0000000000000011 | A=     3 D=     2 M=     0 PC=3
  4 | 1110000010010000 | A=     3 D=     5 M=     0 PC=4
  5 | 0000000000000000 | A=     0 D=     5 M=     0 PC=5
  6 | 1110001100001000 | A=     0 D=     5 M=     5 PC=6
RAM[0..5] = [5, 0, 0, 0, 0, 0]
```
