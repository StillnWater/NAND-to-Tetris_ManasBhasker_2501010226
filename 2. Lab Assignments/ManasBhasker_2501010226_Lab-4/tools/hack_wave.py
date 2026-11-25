"""Cycle-accurate Hack CPU tracer: records ALU + control signals every clock cycle,
prints a table, and draws a waveform PNG.  Optional flag-bug modes for Lab 4 Q3.
usage: python hack_wave.py prog.asm [--cycles N] [--ram 0=5,1=3] [--bug MODE] [--png out.png] [--md]
bug modes: none | zr_stuck0 (zr never 1) | jgt_incl_zero (JGT also jumps on 0) | ng_stuck0"""
import sys, argparse
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from hack_asm import assemble
M = 0xFFFF
sg = lambda x: x - 65536 if x & 0x8000 else x

def alu(x, y, c):
    zx, nx, zy, ny, f, no = (int(b) for b in c)
    if zx: x = 0
    if nx: x ^= M
    if zy: y = 0
    if ny: y ^= M
    o = ((x + y) if f else (x & y)) & M
    return (o ^ M) if no else o

def run(prog, cycles, ram_init=None, bug='none'):
    rom = [p[2] for p in prog]; txt = [p[1] for p in prog]
    ram = [0] * 24577
    for k, v in (ram_init or {}).items(): ram[k] = v & M
    A = D = pc = 0; rows = []
    for n in range(1, cycles + 1):
        if pc >= len(rom): break
        ins = rom[pc]; isC = ins[0] == '1'
        a, comp, d, j = ins[3], ins[4:10], ins[10:13], ins[13:16]
        inM = ram[A & 0x7FFF]
        out = alu(D, inM if a == '1' else A, comp)       # ALU is combinational: also runs for A-instr
        zr = int(out == 0); ng = int(out >> 15)
        if bug == 'zr_stuck0': zr = 0
        if bug == 'ng_stuck0': ng = 0
        ps = int(not (zr or ng))
        if bug == 'jgt_incl_zero': ps = int(not ng)
        jump = int(isC and ((j[0] == '1' and ng) or (j[1] == '1' and zr) or (j[2] == '1' and ps)))
        loadA = int((not isC) or (isC and d[0] == '1')); loadD = int(isC and d[1] == '1')
        writeM = int(isC and d[2] == '1')
        rows.append(dict(cycle=n, pc=pc, asm=txt[pc], ins=ins, A=sg(A), D=sg(D), inM=sg(inM),
                         out=sg(out) if isC else None, zr=zr if isC else None, ng=ng if isC else None,
                         loadA=loadA, loadD=loadD, writeM=writeM, jump=jump, addr=A & 0x7FFF))
        # falling edge: commit state
        newA = int(ins, 2) if not isC else (out if d[0] == '1' else A)
        if writeM: ram[A & 0x7FFF] = out
        if loadD: D = out
        pcn = A if jump else pc + 1
        A = newA; pc = pcn
        rows[-1].update(A_next=sg(A), D_next=sg(D), pc_next=pc)
    return rows, ram

def table(rows):
    h = "| Cyc | PC | Instruction | A | D | M(in) | ALU out | zr | ng | loadA | loadD | writeM | jump | PC next |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"
    f = lambda v: '-' if v is None else v
    return h + '\n' + '\n'.join(
        f"| {r['cycle']} | {r['pc']} | `{r['asm']}` | {r['A']} | {r['D']} | {r['inM']} | {f(r['out'])} | {f(r['zr'])} | {f(r['ng'])} | {r['loadA']} | {r['loadD']} | {r['writeM']} | {r['jump']} | {r['pc_next']} |"
        for r in rows)

def plot(rows, path, title):
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    n = len(rows); xs = range(n + 1)
    sigs = [('clock', None), ('PC', 'pc'), ('ALU out', 'out'), ('zr', 'zr'), ('ng', 'ng'),
            ('loadA', 'loadA'), ('loadD', 'loadD'), ('writeM', 'writeM'), ('jump', 'jump')]
    fig, axs = plt.subplots(len(sigs), 1, figsize=(max(9, n * 0.9), 1.0 * len(sigs) + 1), sharex=True)
    for ax, (name, key) in zip(axs, sigs):
        ax.set_ylabel(name, rotation=0, ha='right', va='center', fontsize=9)
        ax.set_yticks([]); [s.set_visible(False) for s in ax.spines.values()]
        if key is None:
            for i in range(n):
                ax.step([i, i + .5, i + 1], [1, 0, 0], where='post', color='k', lw=1.2)
            ax.set_ylim(-.3, 1.3)
        elif key in ('pc', 'out'):
            for i, r in enumerate(rows):
                ax.plot([i + .05, i + .95], [0, 0], color='C0'); ax.plot([i + .05, i + .95], [1, 1], color='C0')
                ax.plot([i, i + .05], [.5, 0], color='C0'); ax.plot([i, i + .05], [.5, 1], color='C0')
                v = r[key]; ax.text(i + .5, .5, '-' if v is None else str(v), ha='center', va='center', fontsize=8)
            ax.set_ylim(-.2, 1.2)
        else:
            vals = [(r[key] or 0) for r in rows]
            ax.step(list(xs), vals + [vals[-1]], where='post', color='C3', lw=1.6); ax.set_ylim(-.3, 1.3)
    axs[-1].set_xticks([i + .5 for i in range(n)])
    axs[-1].set_xticklabels([f"{i+1}\n{r['asm']}" for i, r in enumerate(rows)], fontsize=8)
    axs[0].set_title(title, fontsize=10); plt.tight_layout(); plt.savefig(path, dpi=130); plt.close()

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('asm'); ap.add_argument('--cycles', type=int, default=20)
    ap.add_argument('--ram', default=''); ap.add_argument('--bug', default='none'); ap.add_argument('--png'); ap.add_argument('--md', action='store_true')
    o = ap.parse_args()
    ram = {int(k): int(v) for k, v in (kv.split('=') for kv in o.ram.split(',') if kv)}
    rows, mem = run(assemble(open(o.asm).read()), o.cycles, ram, o.bug)
    print(table(rows)); print('\nRAM[0..4] =', [sg(x) for x in mem[:5]])
    if o.png: plot(rows, o.png, f"{o.asm.split('/')[-1]}  (bug={o.bug})")
