CON

_clkmode      = xtal1 + pll16x
_xinfreq      = 5_000_000

OBJ

  s2 : "s2mms"

PUB start
  s2.start_motors
  repeat
    waitcnt(clkfreq + cnt)
    waitpne(|< s2#BUTTON, |< s2#BUTTON,0)
    s2.move_timed_mms(8.0,0.0,2.0)
    s2.move_timed_mms(-4.0,0.0,4.0)
    s2.move_timed_mms(8.0,0.0,2.0)
    s2.move_timed_mms(-4.0,0.0,4.0)
