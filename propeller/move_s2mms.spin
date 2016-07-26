CON

_clkmode      = xtal1 + pll16x
_xinfreq      = 5_000_000

OBJ
  s2mms : "s2mms"

PUB start
  s2mms.start_motors
  repeat
    waitcnt(clkfreq + cnt)
    waitpne(|< s2mms#BUTTON, |< s2mms#BUTTON,0)
    s2mms.move_timed_mms(0.0, 3.0, 2.0)
    s2mms.move_timed_mms(6.0, 0.0, 6.0)
    s2mms.move_timed_mms(6.0, -3.0, 2.0)
    s2mms.move_timed_mms(0.0,0.00,1.0)
    s2mms.move_timed_mms(0.0, -3.0, 2.0)
    s2mms.move_timed_mms(-6.0, 0.0, 6.0)
    s2mms.move_timed_mms(-6.0, 3.0, 2.0)
    s2mms.move_timed_mms(0.0,0.00,1.0)
