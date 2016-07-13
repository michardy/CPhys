CON

_clkmode      = xtal1 + pll16x
_xinfreq      = 5_000_000

OBJ

  s2mms : "s2mms"
  S2 : "s2"

PUB start
  s2.start
  s2.start_motors
  s2mms.start_motors
  repeat
    waitcnt(clkfreq + cnt)
    waitpne(|< s2#BUTTON, |< s2#BUTTON,0)
    s2mms.move_timed_mms(8.0,0.00,2.0)
    s2mms.move_timed_mms(-4.0,0.00,4.0)
    s2mms.move_timed_mms(8.0,0.00,2.0)
    s2mms.move_timed_mms(-4.0,0.00,4.0)
