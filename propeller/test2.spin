
'S2 include code version 2015.07.08

'---[Constants]----------------------------------------------------------------

CON

  _clkmode      = xtal1 + pll16x
  _xinfreq      = 5_000_000
  EE_REFLIGHTS  = s2#EE_USER_AREA
  LINE_THLD     = 50
  BAR_THLD      = 32
  OBSTACLE_THLD = 20
  SPKR_VOL      = 35

'---[Global Variables]---------------------------------------------------------

VAR

  long  CoinFlip, LeftMotor, RightMotor, MoveTime, pLeftMotor, pRightMotor, pMoveTime, FMStack[50], stack[30]
  word  WheelSpace, FullCircle, SeqCounter
  byte  LeftLight, CenterLight, RightLight, RefLights[3]
  byte  ResetCount, LineCount, ObstacleCount, StallCount, ObstacleThld
  byte  LineThld, LeftLine, RightLine, LeftObstacle, RightObstacle, Self
  byte  Flag_green, Flag_yellow, Flag_orange, Flag_red, Flag_magenta, Flag_purple, Flag_blue, Stalled, obs[3]

'---[Object Declaration]-------------------------------------------------------

OBJ

  s2    : "S2"
  s2mms : "s2mms"

'---[Start of Program]---------------------------------------------------------

PUB start

  s2.start
  s2mms.start_motors
  s2.start_motors
  s2.start_tones
  s2.button_mode(true, true)
  s2.set_volume(SPKR_VOL)
  s2.set_voices(s2#SAW, s2#SAW)
  ResetCount := s2.reset_button_count
  if (s2.get_line_threshold <> s2#DEFAULT_LINE_THLD)
    LineThld := s2.get_line_threshold
  else
    LineThld := LINE_THLD 
  if (s2.get_obstacle_threshold <> s2#DEFAULT_OBSTACLE_THLD)
    ObstacleThld := s2.get_obstacle_threshold
  else
    ObstacleThld := OBSTACLE_THLD 
  waitcnt(cnt + 10_000_000) 
  CoinFlip :=  s2.light_sensor_raw(s2#LEFT) << 24 | s2.light_sensor_raw(s2#CENTER) << 12 | s2.light_sensor_raw(s2#RIGHT)
  Self := cogid
  long[@WheelSpace] := s2.get_wheel_calibration
  cognew(FaultMonitor, @FMStack)
  cognew(Obstacler, @stack)
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


'---[Battery and Over-current Monitor Cog]-------------------------------------

PUB FaultMonitor : value

  value := $ffff
  waitcnt(cnt + 80_000_000)
  repeat
    value <#= s2.get_adc_results(s2#ADC_VBAT)
    if value > constant((700*2550)/(400*33))      '7.0V
      s2.set_led(s2#POWER,s2#BLUE)
    elseif value > constant((600*2550)/(400*33))  '6.0V
      s2.set_led(s2#POWER,$20)
    else
      s2.set_led(s2#POWER,s2#BLINK_BLUE)
    if s2.get_adc_results(s2#ADC_IMOT) > 210
      cogstop(Self)
      s2.stop_now
      s2.set_leds(s2#BLINK_RED,s2#BLINK_RED,s2#BLINK_RED,s2#OFF)
      repeat

'---[Main Program: Green]------------------------------------------------------

PUB Green

  s2mms.move_timed_mms(-6.0,0.00,2.0)
  MotorSet(128, 128, 3250)
  ReadObstacle
  if (LeftObstacle == 1 and RightObstacle == 1)
    MotorSet(-140, -140, 5000)
  else
    MotorSet(128, 128, 1000)
  MotorSet(128, 128, 2200)

'---[Set Motor Speeds]---------------------------------------------------------

PRI MotorSet(lmotor, rmotor, timer)

  MoveTime := timer #> 0
  LeftMotor := lmotor #> -256 <# 256
  RightMotor := rmotor #> -256 <# 256
  if (LeftMotor <> pLeftMotor or RightMotor <> pRightMotor or MoveTime <> pMoveTime or pMoveTime <> 0)
    if (MoveTime)
      s2.move_now(LeftMotor * MoveTime * FullCircle / 1_024_000, RightMotor * MoveTime * FullCircle / 1_024_000, MoveTime << 1, (||LeftMotor #> ||RightMotor <# 255) >> 4, 0)
      s2.wait_stop
    else  
      s2.wheels_now(LeftMotor, RightMotor, 0)
      waitcnt(cnt + clkfreq / 10)
    pLeftMotor := LeftMotor
    pRightMotor := RightMotor
    pMoveTime := MoveTime

'---[Read Obstacle Sensors]----------------------------------------------------

'---[Read Obstacle Sensors]----------------------------------------------------

PRI ReadObstacle | l, r

  l := obstacle(s2#LEFT, ObstacleThld) & 1
  r := obstacle(s2#RIGHT, ObstacleThld) & 1
  if (l == LeftObstacle and r == RightObstacle)
    ObstacleCount := (Obstaclecount + 1) <# 8
  else
    ObstacleCount := 1
    LeftObstacle := l
    RightObstacle := r

PUB obstacle(side, threshold)

  return obs[side]

'---[End of Program]-----------------------------------------------------------

'---[End of Program]-----------------------------------------------------------
