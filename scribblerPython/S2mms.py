##:::::::[ python module for Scribbler 2mms ]:::::::::::::::::::::::::::::::::
##File:  bayS2mms.py
##
##
##┌────────────────────────────────────────────────┐
##│     Bay School Python Module Derived from      │
##│       Scribbler II Kinematic GUI               │
##│(c) Copyright 2012 and 2013 Matt Greenwolfe     │
##│   See end of file for terms of use.            │
##└────────────────────────────────────────────────┘
##
##
## This python module contains functions needed
## to program straight line motion of the scribbler 2
## robot.

## Dependencies:
##      Python and Visual Module:  see www.vpython.org for installation instructions
##      Parallax propellent dynamic link library:  http://www.parallax.com/PropellerDownloads
##      Propeller Floatmath.spin library
##      s2mms motor driver
##          Place s2mms.spin, propellent.dll, and FloatMath.spin in a folder called propeller
##          Place all three folders in the same folder as this file.


##=======[ Introduction ]=========================================================

## s2mms.spin provides low-level motor drivers and higher level spin routines
## that move the S2 Robot based on step function velocity and acceleration
## profiles.  Accuracy is close to 1mm/s or 1mm/s^2.
##
## This Python module provides the functions needed to specify a series of
## motions, write a spin program, and send that program to the robot.
##::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

from __future__ import division, print_function
import os
import sys
import ctypes

class spin:
    def __init__(self, output_file = "move_s2mms.spin"):
        self.__indent = 2
        self.__indentation_level = 4
        self.__spinfile = output_file
        self.__sCode = '''CON

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
'''

    def __pad(self, length, padtext=" "):
        out = ""
        for i in range(length):
            out += padtext
        return (out)

    def move(self, speed, time_interval): #move adds an item to list_name
        command = ""
##      string = "move(" + str(speed) + "0, " + str(time)
##      if spaces(string, file_name) != 0:
##          for i in range(spaces(string, file_name)//2):
##              command += " "
        command += (self.__pad(2*self.__indent))+"s2mms.move_timed_mms("
        command += str(speed)
        command += ",0.00,"
        command += str(time_interval)
        command += ")\n"
        self.__sCode += command

    def accel(self, initial_speed, acceleration, time_interval):
        command = ""
        command += (self.__pad(2*self.__indent))+"s2mms.move_timed_mms("
        command += str(initial_speed)
        command += ", "
        command += str(acceleration)
        command += ", "
        command += str(time_interval)
        command += ")\n"
        self.__sCode += command

    def speed_up_to(self, final_speed, time_interval):
        command = ""
        command += (self.__pad(2*self.__indent))+"s2mms.move_timed_mms("
        command += str(0.00)
        command += ", "
        command += str(final_speed/time_interval)
        command += ", "
        command += str(time_interval)
        command += ")\n"
        self.__sCode += command

    def cruise_at(self, cruising_speed, time_interval):
        command = ""
        command += (self.__pad(2*self.__indent))+"s2mms.move_timed_mms("
        command += str(cruising_speed)
        command += ", "
        command += str(0.00)
        command += ", "
        command += str(time_interval)
        command += ")\n"
        self.__sCode += command

    def stop_from(self, initial_speed, time_interval):
        command = ""
        command += (self.__pad(2*self.__indent))+"s2mms.move_timed_mms("
        command += str(initial_speed)
        command += ", "
        command += str(-initial_speed/time_interval)
        command += ", "
        command += str(time_interval)
        command += ")\n"
        self.__sCode += command

    def pause_for(self, time):
        self.move(0.00, time)

    def __convert(self, inputC):
        for line in inputC.split('\n'):
            if line.startswith("#indentation level:"):
                self.__indentation_level = int(line[len(line)-1:])
            elif line == "":
                pass
            else:
                command = ""
                inWS = True
                self.__indent = 2
                for char in line:
                    if char == " " and inWS:
                        self.__indent += (1/self.__indentation_level)
                    elif char == '\t' and inWS:
                        self.__indent += 1
                    elif inWS:
                        inWS = False
                        command += char
                    else:
                        command += char
                exec("self."+command)#Someone will kill me for this

    def run(self, inputC, run_mode=3):
        self.__convert(inputC)
        try:
            ctype_spinfile = ctypes.c_char_p(self.__spinfile)
        except TypeError:
            ctype_spinfile = ctypes.c_char_p(self.__spinfile.encode('utf-8'))
        with open(self.__spinfile,"w") as ms2: #This is the safe way to open files
            ms2.write(self.__sCode)
        path = os.path.abspath(os.path.dirname(sys.argv[0])) #points to curr working dir
        prop = ctypes.cdll.LoadLibrary(path + "\Propellent.dll")
        prop.InitPropellent(None)
        libdir = ctypes.c_char_p(os.path.realpath(path))
        prop.SetLibraryPath(libdir)
        prop.CompileSource(ctype_spinfile,True)
        prop.DownloadToPropeller(0, run_mode)
        prop.FinalizePropellent

##def obstacle(list_name=commands):
##    command = "ReadObstacle\n"
##    list_name += [command]
##    command2 = "if (LeftObstacle == 1 and RightObstacle == 1)\n"
##    list_name += [command2]
##    return True
##

##=======[ License ]===========================================================
##
##┌──────────────────────────────────────────────────────────────────────────────────────┐
##│                            TERMS OF USE: Software License                            │
##├──────────────────────────────────────────────────────────────────────────────────────┤
##│The purchase of one copy of S2mmsKinematicGUI and it's dependent files S2Curve.py,    │
##│S2graph.py, S2Segment.py, S2StatusBar.py, S2ToolBar.py, S2VecAdd.py and     s2mms.spin│
##│entitles you to install it on every computer in your school or, for                   │
##│post-secondary institutions, department. Installation to local machines over a network│
##│is allowed. Purchasers are also permitted to distribute these programs to their       │
##│students and instructors for home use. The license is limited to a single campus if   │
##│your institution has multiple campuses.                                               │
##│                                                                                      │
##│The above copyright notice and this permission notice shall be included in all copies │
##│or substantial portions of the Software.                                              │
##│                                                                                      │
##│THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,   │
##│INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A         │
##│PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT    │
##│HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF  │
##│CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE  │
##│OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                         │
##└──────────────────────────────────────────────────────────────────────────────────────┘
##
