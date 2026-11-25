// Program 2: counts RAM[0] down from 5 to 0 (loop with conditional jump)
@5
D=A
@0
M=D
(LOOP)
@0
M=M-1
D=M
@LOOP
D;JGT
(END)
@END
0;JMP
