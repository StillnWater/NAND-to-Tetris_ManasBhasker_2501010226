// CPU Emulator script for Arithmetic.asm
load Arithmetic.asm,
output-file Arithmetic.out,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2 RAM[3]%D2.6.2 RAM[4]%D2.6.2 RAM[5]%D2.6.2;
set RAM[0] 12, set RAM[1] 5,
repeat 40 {
  ticktock;
}
output;
