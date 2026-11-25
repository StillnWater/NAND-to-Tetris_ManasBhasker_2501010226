// CPU Emulator script for Loop.asm
load Loop.asm,
output-file Loop.out,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2 RAM[3]%D2.6.2 RAM[4]%D2.6.2 RAM[5]%D2.6.2;
set RAM[0] 10,
repeat 200 {
  ticktock;
}
output;
