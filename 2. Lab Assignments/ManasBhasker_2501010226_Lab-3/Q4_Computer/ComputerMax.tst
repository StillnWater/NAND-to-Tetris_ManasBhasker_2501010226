load Computer.hdl,
output-file ComputerMax.out,
output-list time%S1.4.1 reset%B2.1.2 ARegister[]%D1.7.1 DRegister[]%D1.7.1 PC[]%D0.4.0 RAM16K[0]%D1.7.1 RAM16K[1]%D1.7.1 RAM16K[2]%D1.7.1;

ROM32K load Max.hack,
set RAM16K[0] 3,
set RAM16K[1] 5,
output;

repeat 14 {
  tick, tock, output;
}

set PC 0,
set RAM16K[0] 23456,
set RAM16K[1] 12345,
set RAM16K[2] 0,
repeat 14 {
  tick, tock, output;
}
