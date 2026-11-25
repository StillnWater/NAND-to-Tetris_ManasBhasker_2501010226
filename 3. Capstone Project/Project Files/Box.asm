// Box.asm - Capstone, K = 26
// Box: starts at row 26, 20 rows tall, 48 pixels wide (3 words).
// Key pressed -> black box; key released -> box cleared.
// Start address = SCREEN + 32*26 = 16384 + 832 = 17216

(MAIN)
    @color
    M=0            // assume no key -> white
    @KBD
    D=M
    @DRAW
    D;JEQ          // KBD == 0 -> keep white
    @color
    M=-1           // key pressed -> black (all 16 bits = 1)

(DRAW)
    @SCREEN
    D=A
    @832           // 32 * 26
    D=D+A
    @addr
    M=D            // addr = start of row 26
    @20
    D=A
    @rows
    M=D            // rows = 20

(ROW)
    @color
    D=M
    @addr
    A=M
    M=D            // word 0
    A=A+1
    M=D            // word 1
    A=A+1
    M=D            // word 2  (3 words = 48 px)
    @32
    D=A
    @addr
    M=D+M          // next row
    @rows
    M=M-1
    D=M
    @ROW
    D;JGT          // more rows left?
    @MAIN
    0;JMP
