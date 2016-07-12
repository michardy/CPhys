CON

_clkmode      = xtal1 + pll16x
_xinfreq      = 5_000_000

OBJ

  s2mms : "s2mms"
  s2 : "s2"

PUB start
  s2mms.start_motors
  repeat
    waitcnt(clkfreq + cnt)
    waitpne(|< s2#BUTTON, |< s2#BUTTON,0)
    s2mms.move_timed_mms(6.0,0.00,5.0)
    s2.delay_tenths(30)
    s2mms.move_timed_mms(-6.0,0.00,5.0)
