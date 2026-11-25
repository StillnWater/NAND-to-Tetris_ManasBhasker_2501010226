// Q1(b) Branching: sign of x.  RAM[1] = 1 if x>0, 0 if x==0, -1 if x<0
@0
D=M
@POS
D;JGT
@ZERO
D;JEQ
@1
M=-1       // negative
@END
0;JMP
(POS)
@1
M=1
@END
0;JMP
(ZERO)
@1
M=0
(END)
@END
0;JMP
