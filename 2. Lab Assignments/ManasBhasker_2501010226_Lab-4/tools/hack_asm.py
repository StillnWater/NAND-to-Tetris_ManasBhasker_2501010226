"""Minimal Hack assembler.  usage: python hack_asm.py prog.asm [--explain]"""
import sys, re
COMP = {'0':'101010','1':'111111','-1':'111010','D':'001100','A':'110000','!D':'001101','!A':'110001',
 '-D':'001111','-A':'110011','D+1':'011111','A+1':'110111','D-1':'001110','A-1':'110010','D+A':'000010',
 'D-A':'010011','A-D':'000111','D&A':'000000','D|A':'010101'}
JUMP = {'':'000','JGT':'001','JEQ':'010','JGE':'011','JLT':'100','JNE':'101','JLE':'110','JMP':'111'}
SYM = {'SP':0,'LCL':1,'ARG':2,'THIS':3,'THAT':4,'SCREEN':16384,'KBD':24576}
SYM.update({f'R{i}':i for i in range(16)})

def assemble(text):
    sym = dict(SYM); lines = []
    for raw in text.splitlines():
        l = re.sub(r'//.*', '', raw).replace(' ', '').strip()
        if not l: continue
        if l.startswith('('): sym[l[1:-1]] = len(lines)
        else: lines.append(l)
    nxt, out = 16, []
    for addr, l in enumerate(lines):
        if l[0] == '@':
            v = l[1:]
            if v.isdigit(): n = int(v)
            else:
                if v not in sym: sym[v] = nxt; nxt += 1
                n = sym[v]
            out.append((addr, l, format(n, '016b'), {'type': 'A', 'value': n}))
        else:
            dest, rest = (l.split('=', 1) if '=' in l else ('', l))
            comp, jmp = (rest.split(';', 1) if ';' in rest else (rest, ''))
            a = '1' if 'M' in comp else '0'
            c = COMP[comp.replace('M', 'A')]
            d = ''.join('1' if ch in dest else '0' for ch in 'ADM')
            out.append((addr, l, '111' + a + c + d + JUMP[jmp],
                        {'type': 'C', 'a': a, 'comp': c, 'dest': d, 'jump': JUMP[jmp]}))
    return out

def explain(prog):
    rows = ['| Addr | Instruction | Binary | Breakdown |', '|---|---|---|---|']
    for addr, l, b, f in prog:
        if f['type'] == 'A':
            br = f"`0` + 15-bit value `{b[1:]}` (= {f['value']})"
        else:
            br = f"`111` a=`{f['a']}` comp=`{f['comp']}` dest=`{f['dest']}` jump=`{f['jump']}`"
        rows.append(f'| {addr} | `{l}` | `{b}` | {br} |')
    return '\n'.join(rows)

if __name__ == '__main__':
    src = sys.argv[1]
    prog = assemble(open(src).read())
    open(src.rsplit('.', 1)[0] + '.hack', 'w').write('\n'.join(p[2] for p in prog) + '\n')
    if '--explain' in sys.argv: print(explain(prog))
