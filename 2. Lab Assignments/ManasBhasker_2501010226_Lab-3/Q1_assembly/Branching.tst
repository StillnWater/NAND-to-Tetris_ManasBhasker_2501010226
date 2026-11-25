// CPU Emulator script for Branching.asm
load Branching.asm,
output-file Branching.out,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2 RAM[3]%D2.6.2 RAM[4]%D2.6.2 RAM[5]%D2.6.2;
set RAM[0] -7,
repeat 20 {
  ticktock;
}
output;
