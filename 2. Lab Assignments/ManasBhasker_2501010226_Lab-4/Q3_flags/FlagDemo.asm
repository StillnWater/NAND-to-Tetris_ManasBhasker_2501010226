// Count down: RAM[0] = n, RAM[1] counts loop iterations.  Correct result: RAM[1] = n.
@1
M=0
(LOOP)
@1
M=M+1      // iterations++
@0
M=M-1      // n--
D=M
@LOOP
D;JGT      // repeat while n > 0   (needs correct ng AND zr: JGT = !ng && !zr)
(END)
@END
0;JMP
