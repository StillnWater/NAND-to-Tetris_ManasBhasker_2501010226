// Memory-mapped I/O demo: poll keyboard (RAM[24576]); key pressed -> blacken first screen word, else clear it.
(LOOP)
@KBD
D=M        // read keyboard register
@BLACK
D;JGT      // key code > 0 ?
@SCREEN
M=0        // no key: write 0 to screen word 0 (16 white pixels)
@LOOP
0;JMP
(BLACK)
@SCREEN
M=-1       // key: write 1111111111111111 (16 black pixels)
@LOOP
0;JMP
