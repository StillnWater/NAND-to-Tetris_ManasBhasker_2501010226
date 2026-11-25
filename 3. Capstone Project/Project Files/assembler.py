#!/usr/bin/env python3
"""Hack assembler (Nand to Tetris) - Capstone, K = 26.

Usage: python assembler.py Prog.asm [Prog.hack]

Pass 1: strip comments/blank lines, record label addresses.
Pass 2: translate every instruction to 16 bits; new variables get RAM 16, 17, ...

Extra feature (K mod 3 = 2): warn if the same label is written twice.
Bad lines are reported as "Line N: message" instead of crashing.
"""
import sys

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011", "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101",
}
# Commutative forms the official assembler also accepts
for a, b in (("A+D", "D+A"), ("M+D", "D+M"), ("A&D", "D&A"),
             ("M&D", "D&M"), ("A|D", "D|A"), ("M|D", "D|M"),
             ("1+D", "D+1"), ("1+A", "A+1"), ("1+M", "M+1")):
    COMP[a] = COMP[b]

DEST = {"": "000", "M": "001", "D": "010", "MD": "011", "DM": "011",
        "A": "100", "AM": "101", "MA": "101", "AD": "110", "DA": "110",
        "AMD": "111"}
JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

PREDEFINED = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
              "SCREEN": 16384, "KBD": 24576}
PREDEFINED.update({f"R{i}": i for i in range(16)})


class AsmError(Exception):
    pass


def clean(line):
    """Remove comments and all whitespace."""
    return line.split("//", 1)[0].replace(" ", "").replace("\t", "").strip()


def first_pass(lines):
    """Return (instructions, symbols). instructions = [(line_no, text)]."""
    symbols = dict(PREDEFINED)
    labels_seen = {}
    instructions = []
    for no, raw in enumerate(lines, 1):
        line = clean(raw)
        if not line:
            continue
        if line.startswith("("):
            if not line.endswith(")") or len(line) < 3:
                print(f"Line {no}: invalid label '{line}'", file=sys.stderr)
                continue
            label = line[1:-1]
            if label in labels_seen:  # ---- extra feature for K=26 ----
                print(f"Warning (line {no}): label '{label}' already defined "
                      f"on line {labels_seen[label]}; using the new address",
                      file=sys.stderr)
            else:
                labels_seen[label] = no
            symbols[label] = len(instructions)
        else:
            instructions.append((no, line))
    return instructions, symbols


def encode_a(value, symbols, state):
    if value.isdigit():
        n = int(value)
    else:
        if value not in symbols:
            symbols[value] = state["next_var"]
            state["next_var"] += 1
        n = symbols[value]
    if n > 32767:
        raise AsmError(f"address {n} too large (max 32767)")
    return format(n, "016b")


def encode_c(line):
    dest, comp, jump = "", line, ""
    if "=" in line:
        dest, comp = line.split("=", 1)
    if ";" in comp:
        comp, jump = comp.split(";", 1)
    if dest not in DEST:
        raise AsmError(f"invalid destination '{dest}'")
    if comp not in COMP:
        raise AsmError(f"invalid instruction '{line}'")
    if jump not in JUMP:
        raise AsmError(f"invalid jump '{jump}'")
    return "111" + COMP[comp] + DEST[dest] + JUMP[jump]


def assemble(lines):
    instructions, symbols = first_pass(lines)
    state = {"next_var": 16}
    out, errors = [], 0
    for no, line in instructions:
        try:
            if line.startswith("@"):
                if len(line) == 1:
                    raise AsmError("empty @ instruction")
                out.append(encode_a(line[1:], symbols, state))
            else:
                out.append(encode_c(line))
        except AsmError as e:
            print(f"Line {no}: {e}", file=sys.stderr)
            errors += 1
    return out, errors


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python assembler.py Prog.asm [Prog.hack]")
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else src.rsplit(".", 1)[0] + ".hack"
    with open(src) as f:
        out, errors = assemble(f.read().splitlines())
    if errors:
        sys.exit(f"{errors} error(s); no output written.")
    with open(dst, "w") as f:
        f.write("\n".join(out) + "\n")
    print(f"Wrote {len(out)} instructions to {dst}")


if __name__ == "__main__":
    main()
