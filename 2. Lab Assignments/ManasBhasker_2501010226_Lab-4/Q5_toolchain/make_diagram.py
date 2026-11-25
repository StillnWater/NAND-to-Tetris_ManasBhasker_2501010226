import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
def row(ax, y, title, boxes, colors):
    ax.text(0, y + .62, title, fontsize=11, weight='bold')
    x = 0
    for i, (t, c) in enumerate(zip(boxes, colors)):
        ax.add_patch(FancyBboxPatch((x, y), 1.55, .5, boxstyle='round,pad=0.02', fc=c, ec='k'))
        ax.text(x + .775, y + .25, t, ha='center', va='center', fontsize=8)
        if i < len(boxes) - 1: ax.annotate('', (x + 1.75, y + .25), (x + 1.57, y + .25), arrowprops=dict(arrowstyle='->'))
        x += 1.8
fig, ax = plt.subplots(figsize=(17, 5)); ax.axis('off'); ax.set_xlim(-.1, 16.6); ax.set_ylim(-.3, 3.6)
src, tool, art = '#cfe8ff', '#ffe3b3', '#d6f5d6'
row(ax, 2.3, 'Hack toolchain', ['Jack .jack', 'Compiler', '.vm', 'VM translator', 'Hack .asm', 'ASSEMBLER', '.hack binary', 'ROM load -> CPU'], [src, tool, art, tool, src, tool, art, tool])
row(ax, .6, 'Real toolchain', ['C .c', 'Preproc+Compiler', 'Assembly .s', 'ASSEMBLER', 'Object .o', 'LINKER (+libs)', 'Executable', 'LOADER -> CPU'], [src, tool, src, tool, art, tool, art, tool])
plt.savefig('Q5_toolchain/toolchain_diagram.png', dpi=130, bbox_inches='tight')
