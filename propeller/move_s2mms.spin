CON

_clkmode      = xtal1 + pll16x
_xinfreq      = 5_000_000
OBSTACLE_THLD = 20

VAR

long CoinFlip, LeftMotor, RightMotor, MoveTime, pLeftMotor, pRightMotor, pMoveTime, FMStack[50], stack[30]
byte  ResetCount, LineCount, ObstacleCount, StallCount, ObstacleThld
byte LineThld, LeftLine, RightLine, LeftObstacle, RightObstacle, Self
byte  Flag_green, Flag_yellow, Flag_orange, Flag_red, Flag_magenta, Flag_purple, Flag_blue, Stalled, obs[3]

OBJ

  s2mms : "s2mms"
  S2 : "s2"

PUB start
  s2.start
  s2.start_motors
  if (s2.get_obstacle_threshold <> s2#DEFAULT_OBSTACLE_THLD)
    ObstacleThld := s2.get_obstacle_threshold
  else
    ObstacleThld := OBSTACLE_THLD
  CoinFlip := s2.light_sensor_raw(s2#LEFT) << 24 | s2.light_sensor_raw(s2#CENTER) << 12 | s2.light_sensor_raw(s2#RIGHT)
  Self := cogid
  cognew(Obstacler, @stack)
  s2mms.start_motors
  \Green
  repeat

PUB Obstacler | side

  repeat
    repeat side from s2#OBS_TX_LEFT to s2#OBS_TX_RIGHT step constant(s2#OBS_TX_RIGHT - s2#OBS_TX_LEFT)
      frqa := 14000 * ObstacleThld + 20607 * (100 - ObstacleThld)
      ctra := %00100 << 26 | side
      dira[side]~~
      waitcnt(cnt + 24000)
      obs[-(side == s2#OBS_TX_RIGHT) + 1] := ina[s2#OBS_RX] == 0
      dira[side]~
      waitcnt(cnt + clkfreq / 8)

PUB Green
  repeat
    waitcnt(clkfreq + cnt)
    waitpne(|< s2#BUTTON, |< s2#BUTTON,0)
    s2mms.move_timed_mms(0.0, 3.0, 2.0)
    s2mms.move_timed_mms(6.0, 0.0, 6.0)
    s2mms.move_timed_mms(6.0, -3.0, 2.0)
    s2mms.move_timed_mms(0.0,0.00,1.0)
    s2mms.move_timed_mms(0.0, -3.0, 2.0)
    s2mms.move_timed_mms(-6.0, 0.0, 6.0)
    s2mms.move_timed_mms(-6.0, 3.0, 2.0)
    s2mms.move_timed_mms(0.0,0.00,1.0)
