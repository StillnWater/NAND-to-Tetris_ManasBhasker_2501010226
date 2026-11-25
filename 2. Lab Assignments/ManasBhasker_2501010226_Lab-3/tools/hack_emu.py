"""Tiny Hack reference emulator (used to cross-check expected outputs and traces).
usage: python hack_emu.py prog.hack [--trace] [--steps N] [R0=5 R1=3 ...]"""
import sys
M16 = 0xFFFF
def sgn(x): return x - 65536 if x & 0x8000 else x
def alu(x, y, c):
    zx, nx, zy, ny, f, no = (int(b) for b in c)
    if zx: x = 0
    if nx: x ^= M16
    if zy: y = 0
    if ny: y ^= M16
    o = ((x + y) if f else (x & y)) & M16
    return (o ^ M16) if no else o

class CPU:
    def __init__(self, rom):
        self.rom, self.ram = rom, [0] * 24577
        self.A = self.D = self.pc = 0
    def step(self):
        i = self.rom[self.pc]
        if i[0] == '0':
            self.A = int(i, 2); self.pc += 1; return False
        a, c, d, j = i[3], i[4:10], i[10:13], i[13:16]
        addr = self.A & 0x7FFF                       # M uses A *before* the write
        o = alu(self.D, self.ram[addr] if a == '1' else self.A, c)
        target = self.A
        if d[2] == '1': self.ram[addr] = o
        if d[1] == '1': self.D = o
        if d[0] == '1': self.A = o
        v = sgn(o)
        jmp = (j[0]=='1' and v<0) or (j[1]=='1' and v==0) or (j[2]=='1' and v>0)
        old = self.pc
        self.pc = target if jmp else self.pc + 1
        return self.pc == old                        # True => halted in self-loop

def load(path): return [l.strip() for l in open(path) if l.strip()]

if __name__ == '__main__':
    cpu = CPU(load(sys.argv[1])); steps = 5000
    for arg in sys.argv[2:]:
        if arg.startswith('R'): k, v = arg[1:].split('='); cpu.ram[int(k)] = int(v) & M16
        if arg.startswith('--steps'): steps = int(sys.argv[sys.argv.index(arg)+1])
    trace = '--trace' in sys.argv
    for n in range(steps):
        ins = cpu.rom[cpu.pc]; halted = cpu.step()
        if trace: print(f"{n+1:3d} | {ins} | A={sgn(cpu.A):6d} D={sgn(cpu.D):6d} M={sgn(cpu.ram[cpu.A & 0x7FFF]):6d} PC={cpu.pc}")
        if halted: break
    print("RAM[0..5] =", [sgn(x) for x in cpu.ram[:6]])
