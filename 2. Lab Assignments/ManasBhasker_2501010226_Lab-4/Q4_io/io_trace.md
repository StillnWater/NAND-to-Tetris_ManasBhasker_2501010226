# Q4 – Machine-level trace with memory-mapped I/O (IO.asm)

## Address map (15-bit addressM)
| Range | Binary prefix of address | Device |
|---|---|---|
| 0 – 16383 | `0xxxxxxxxxxxxxx` (bit14 = 0) | RAM16K |
| 16384 – 24575 | `10xxxxxxxxxxxxx` (bit14=1, bit13=0) | Screen (8K words) |
| 24576 | `110000000000000` | Keyboard |

`@SCREEN` = 16384 = `100000000000000`, `@KBD` = 24576 = `110000000000000`.

## How memory-mapped I/O works
There are no special I/O instructions. The CPU just puts an address on addressM and (maybe) asserts writeM.
`Memory.hdl` decodes the top address bits: bit14 selects RAM vs I/O, bit13 selects Screen vs Keyboard.
- **Screen write:** `M=-1` with A=16384 → writeM=1, outM=`1111111111111111`, Screen chip's load=1, so the 16 pixels of word 0 (row 0, columns 0-15) turn black (1 bit = 1 pixel).
  Pixel (row r, col c) is bit `c % 16` of word `16384 + r*32 + c/16`.
- **Keyboard read:** `D=M` with A=24576 → Keyboard chip output goes through the Mux16 into inM; it holds the key code of the currently pressed key (0 if none). It is read-only: no load pin.

## Trace – no key pressed (Keyboard = 0)
| Cyc | PC | Instruction | addressM (A during cycle, binary) | Region | Action |
|---|---|---|---|---|---|
| 1 | 0 | `@KBD` | `000000000000000` | RAM | A ← 24576 |
| 2 | 1 | `D=M` | `110000000000000` | KBD | read KBD[24576] = 0 → D |
| 3 | 2 | `@BLACK` | `110000000000000` | KBD | A ← 8 |
| 4 | 3 | `D;JGT` | `000000000001000` | RAM | no jump |
| 5 | 4 | `@SCREEN` | `000000000001000` | RAM | A ← 16384 |
| 6 | 5 | `M=0` | `100000000000000` | SCREEN | write `0000000000000000` to SCREEN[16384] |
| 7 | 6 | `@LOOP` | `100000000000000` | SCREEN | A ← 0 |
| 8 | 7 | `0;JMP` | `000000000000000` | RAM | jump taken (PC ← A) |
| 9 | 0 | `@KBD` | `000000000000000` | RAM | A ← 24576 |
| 10 | 1 | `D=M` | `110000000000000` | KBD | read KBD[24576] = 0 → D |

Result: Screen[0] = 0 (all white)

## Trace – key pressed (Keyboard = 75, i.e. 'K')
| Cyc | PC | Instruction | addressM (A during cycle, binary) | Region | Action |
|---|---|---|---|---|---|
| 1 | 0 | `@KBD` | `000000000000000` | RAM | A ← 24576 |
| 2 | 1 | `D=M` | `110000000000000` | KBD | read KBD[24576] = 75 → D |
| 3 | 2 | `@BLACK` | `110000000000000` | KBD | A ← 8 |
| 4 | 3 | `D;JGT` | `000000000001000` | RAM | jump taken (PC ← A) |
| 5 | 8 | `@SCREEN` | `000000000001000` | RAM | A ← 16384 |
| 6 | 9 | `M=-1` | `100000000000000` | SCREEN | write `1111111111111111` to SCREEN[16384] |
| 7 | 10 | `@LOOP` | `100000000000000` | SCREEN | A ← 0 |
| 8 | 11 | `0;JMP` | `000000000000000` | RAM | jump taken (PC ← A) |
| 9 | 0 | `@KBD` | `000000000000000` | RAM | A ← 24576 |
| 10 | 1 | `D=M` | `110000000000000` | KBD | read KBD[24576] = 75 → D |

Result: Screen[0] = -1 (= 1111111111111111b, 16 black pixels)

## Stack of operations per instruction (machine level)
`@KBD`: fetch → A-instr → A ← 24576 · `D=M`: fetch → C-instr a=1 → addressM=A → inM → ALU(comp=`110000`) → D ← inM ·
`@BLACK`: A ← 8 · `D;JGT`: ALU passes D, ng=0 & zr=0 → jump → PC ← A · `@SCREEN`; `M=-1`: ALU out=-1 → writeM=1 → Screen word written.
(Hack has no call stack in hardware; the "stack" here is the ordered pipeline of micro-operations per instruction.)

## Security link
Because I/O is just memory, any bug that lets a program choose the address (e.g. off-by-one past the end of RAM, or an unchecked pointer) can write to the screen or read the keyboard — in real systems the same idea is why unchecked pointers to memory-mapped device registers are dangerous, and why OSes protect device ranges with privilege/MMU rules.
