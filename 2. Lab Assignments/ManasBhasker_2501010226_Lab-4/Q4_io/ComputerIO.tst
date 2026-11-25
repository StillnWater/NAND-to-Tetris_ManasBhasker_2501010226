// Hardware Simulator: copy IO.hack next to Computer.hdl.  Press a key in the simulator keyboard
// (set Keyboard 75 below to simulate) and watch Screen[0].
load Computer.hdl,
output-file ComputerIO.out,
output-list time%S1.4.1 PC[]%D0.4.0 Screen[0]%B1.16.1 Keyboard%D1.5.1;

ROM32K load IO.hack,
set Keyboard 0,
repeat 8 { tick, tock, output; }

set Keyboard 75,
repeat 8 { tick, tock, output; }
