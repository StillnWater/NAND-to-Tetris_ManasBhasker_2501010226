// Hardware Simulator script: run Sample.hack on the Lab 3 Computer chip, log signals each half-cycle.
// Copy Sample.hack next to Computer.hdl first.
load Computer.hdl,
output-file ComputerWave.out,
output-list time%S1.4.1 reset%B2.1.2 PC[]%D0.4.0 ARegister[]%D1.7.1 DRegister[]%D1.7.1 RAM16K[0]%D1.7.1 RAM16K[1]%D1.7.1;

ROM32K load Sample.hack,
output;

repeat 12 {
  tick, output, tock, output;
}
