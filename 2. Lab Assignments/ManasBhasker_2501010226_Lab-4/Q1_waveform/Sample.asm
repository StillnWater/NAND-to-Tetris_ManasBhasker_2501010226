// Lab 4 sample: exercises A-load, ALU sub, memory write, zero flag and a conditional jump
@5
D=A        // D = 5
@3
D=D-A      // D = 2
@0
M=D        // RAM[0] = 2
@2
D=D-A      // D = 0  -> zr = 1
@SKIP
D;JEQ      // taken because zr = 1
@1
M=-1       // skipped when the flags are right
(SKIP)
@SKIP2
0;JMP
(SKIP2)
@SKIP2
0;JMP
