load Computer.hdl,
output-file ComputerRect.out,
output-list time%S1.4.1 reset%B2.1.2 PC[]%D0.4.0 RAM16K[0]%D1.7.1 Screen[0]%D1.7.1 Screen[32]%D1.7.1 Screen[64]%D1.7.1 Screen[96]%D1.7.1;

ROM32K load Rect.hack,
set RAM16K[0] 3,
output;

repeat 100 {
  tick, tock;
}
output;
