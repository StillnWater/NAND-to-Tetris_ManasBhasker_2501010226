"""Self-checks for the capstone (K = 26). Run: python tests/test_all.py"""
import sys, io, contextlib, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import assembler

SCREEN, KBD = 16384, 24576
ROOT = os.path.join(os.path.dirname(__file__), "..")

def asm(text):
    return assembler.assemble(text.splitlines())

def run(hack, kbd, steps=3000):
    """Tiny Hack CPU simulator (Python ints, 16-bit)."""
    rom = [int(l, 2) for l in hack]
    ram = [0] * 24577
    ram[KBD] = kbd
    a = d = pc = 0
    s16 = lambda v: v - 65536 if v & 0x8000 else v
    for _ in range(steps):
        if pc >= len(rom):
            break
        ins = rom[pc]
        if not ins & 0x8000:
            a, pc = ins, pc + 1
            continue
        y = ram[a] if ins & 0x1000 else a
        x = d
        if ins & 0x800: x = 0
        if ins & 0x400: x = ~x
        if ins & 0x200: y = 0
        if ins & 0x100: y = ~y
        out = (x + y) if ins & 0x80 else (x & y)
        if ins & 0x40: out = ~out
        out &= 0xFFFF
        mem_a = a
        if ins & 0x20: a = out
        if ins & 0x10: d = out
        if ins & 0x08: ram[mem_a] = out
        v = s16(out)
        jump = ((ins & 4) and v < 0) or ((ins & 2) and v == 0) or ((ins & 1) and v > 0)
        pc = a if jump else pc + 1
    return ram

def test_add():
    out, err = asm("@2\nD=A\n@3\nD=D+A\n@0\nM=D")
    assert err == 0 and out == [
        "0000000000000010", "1110110000010000", "0000000000000011",
        "1110000010010000", "0000000000000000", "1110001100001000"]
    ram = run(out, 0)
    assert ram[0] == 5
    print("PASS Add.asm: matches official Add.hack, R0 = 5")

def test_max():
    for r0, r1 in [(3, 5), (7, 2), (4, 4)]:
        prog, _ = asm(f"@{r0}\nD=A\n@R0\nM=D\n@{r1}\nD=A\n@R1\nM=D\n" +
                      open(f"{ROOT}/asm/Max.asm").read())
        ram = run(prog, 0)
        assert ram[2] == max(r0, r1), (r0, r1, ram[2])
    print("PASS Max.asm: R2 = max(R0, R1)")

def test_rect():
    prog, _ = asm("@5\nD=A\n@R0\nM=D\n" + open(f"{ROOT}/asm/Rect.asm").read())
    ram = run(prog, 0)
    assert [ram[SCREEN + 32 * r] for r in range(6)] == [-1 & 0xFFFF] * 5 + [0]
    print("PASS Rect.asm: 5 rows drawn")

def test_duplicate_label_warning():
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        asm("(LOOP)\n@1\n(LOOP)\n0;JMP")
    assert "label 'LOOP' already defined" in buf.getvalue()
    print("PASS duplicate-label warning:", buf.getvalue().strip())

def test_bad_line():
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        _, err = asm("@1\nD=A\nFOO=BAR")
    assert err == 1 and "Line 3" in buf.getvalue()
    print("PASS bad line message:", buf.getvalue().strip())

def test_box():
    hack = open(f"{ROOT}/Box.hack").read().split()
    FULL = 0xFFFF
    # key pressed
    ram = run(hack, 75)
    for r in range(0, 70):
        row = [ram[SCREEN + 32 * r + w] for w in range(32)]
        if 26 <= r <= 45:
            assert row[:3] == [FULL] * 3 and not any(row[3:]), f"row {r}"
        else:
            assert not any(row), f"row {r} should be empty"
    print("PASS Box.hack key pressed: rows 26-45, words 0-2 black "
          "(48x20 px), nothing else touched")
    # no key -> box stays white
    ram2 = run(hack, 0)
    assert not any(ram2[SCREEN:SCREEN + 32 * 70])
    assert SCREEN + 32 * 26 == 17216
    print("PASS Box.hack no key: screen blank; start address 17216")

if __name__ == "__main__":
    for t in (test_add, test_max, test_rect, test_duplicate_label_warning,
              test_bad_line, test_box):
        t()
    print("\nAll checks passed.")
