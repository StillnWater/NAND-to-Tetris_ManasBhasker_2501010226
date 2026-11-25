// Q1(a) Arithmetic: inputs RAM[0]=x, RAM[1]=y
// RAM[2]=x+y  RAM[3]=x-y  RAM[4]=2*x  RAM[5]=-x
@0
D=M
@1
D=D+M
@2
M=D        // x+y
@0
D=M
@1
D=D-M
@3
M=D        // x-y
@0
D=M
D=D+M
@4
M=D        // 2x
@0
D=-M
@5
M=D        // -x
(END)
@END
0;JMP
