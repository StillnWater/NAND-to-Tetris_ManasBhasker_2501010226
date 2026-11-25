// Q1(c) Loop: RAM[1] = 1+2+...+RAM[0]
@1
M=0        // sum = 0
@2
M=1        // i = 1
(LOOP)
@2
D=M
@0
D=D-M      // i - n
@END
D;JGT      // if i > n stop
@2
D=M
@1
M=D+M      // sum += i
@2
M=M+1      // i++
@LOOP
0;JMP
(END)
@END
0;JMP
