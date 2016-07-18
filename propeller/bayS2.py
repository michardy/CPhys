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

def S2tbSend_To_S2(commands):    
    spinfile = "move_s2.spin"
    ctype_spinfile = ctypes.c_char_p(spinfile)
    ms2 = open(spinfile,"w")
    ms2.write("CON\n\n")
    ms2.write("_clkmode      = xtal1 + pll16x\n")
    ms2.write("_xinfreq      = 5_000_000\n")
    ms2.write("OBSTACLE_THLD = 20\n\n")
    ms2.write("VAR\n\n")
    ms2.write("long CoinFlip, LeftMotor, RightMotor, MoveTime, pLeftMotor, pRightMotor, pMoveTime, FMStack[50], stack[30]\n")
    ms2.write("byte  ResetCount, LineCount, ObstacleCount, StallCount, ObstacleThld\n")
    ms2.write("byte LineThld, LeftLine, RightLine, LeftObstacle, RightObstacle, Self\n")
    ms2.write("byte  Flag_green, Flag_yellow, Flag_orange, Flag_red, Flag_magenta, Flag_purple, Flag_blue, Stalled, obs[3]\n\n")
    ms2.write("OBJ\n\n")
    ms2.write('  S2 : "s2"\n\n')
    ms2.write('PUB start\n')
    ms2.write('  s2.start\n')
    ms2.write('  s2.start_motors\n')
    ms2.write('  if (s2.get_obstacle_threshold <> s2#DEFAULT_OBSTACLE_THLD)\n')
    ms2.write('    ObstacleThld := s2.get_obstacle_threshold\n')
    ms2.write('  else\n')
    ms2.write('    ObstacleThld := OBSTACLE_THLD\n')
    ms2.write('  CoinFlip := s2.light_sensor_raw(s2#LEFT) << 24 | s2.light_sensor_raw(s2#CENTER) << 12 | s2.light_sensor_raw(s2#RIGHT)\n')
    ms2.write('  Self := cogid\n')
    ms2.write('  cognew(Obstacler, @stack)\n')
    ms2.write('  \Green\n')
    ms2.write('  repeat\n\n')
    ms2.write('PUB Obstacler | side\n\n')
    ms2.write('  repeat\n')
    ms2.write('    repeat side from s2#OBS_TX_LEFT to s2#OBS_TX_RIGHT step constant(s2#OBS_TX_RIGHT - s2#OBS_TX_LEFT)\n')
    ms2.write('      frqa := 14000 * ObstacleThld + 20607 * (100 - ObstacleThld)\n')
    ms2.write('      ctra := %00100 << 26 | side\n')
    ms2.write('      dira[side]~~\n')
    ms2.write('      waitcnt(cnt + 24000)\n')
    ms2.write('      obs[-(side == s2#OBS_TX_RIGHT) + 1] := ina[s2#OBS_RX] == 0\n')
    ms2.write('      dira[side]~\n')
    ms2.write('      waitcnt(cnt + clkfreq / 8)\n\n')
    ms2.write('PUB Green\n')
    ms2.write('  repeat\n')
    ms2.write('    waitcnt(clkfreq + cnt)\n')
    ms2.write('    waitpne(|< s2#BUTTON, |< s2#BUTTON,0)\n')
    indent = '    '

    for command in commands:         
        ms2.write(indent + command)

    ms2.close()
    
    path = os.path.abspath(os.path.dirname(sys.argv[0])) #points to curr working dir
    prop = ctypes.cdll.LoadLibrary(path + "\Propellent.dll")
    prop.InitPropellent(None)
    libdir = ctypes.c_char_p(os.path.realpath(path))
    prop.SetLibraryPath(libdir)
    prop.CompileSource(ctype_spinfile,True)
#    prop.DownloadToPropeller(0,1) #store in RAM only, and run
    prop.DownloadToPropeller(0,3)  #store in RAM and EEPROM, and run
    prop.FinalizePropellent
     
commands = []

def get_line_number(phrase, file_name):
    with open(file_name) as f:
        for i, line in enumerate(f, 1):
            if phrase in line:
                return i

def spaces(phrase, file_name="stuCodeBayS2.py"):
    line_number = get_line_number(phrase, file_name)
    with open(file_name) as afile:
        line_lengths = [len(line) - len(line.lstrip()) for line in afile]
    spaces = line_lengths[line_number - 1]
    return spaces

def move(speed, time, list_name=commands, file_name="stuCodeBayS2.py"): #move adds an item to list_name
    command = ""
    string = "move(" + str(speed) + "0, " + str(time)
    if spaces(string, file_name) != 0:
        for i in range(spaces(string, file_name)//2):
            command += " "
    command += "MotorSet("
    command += str(speed)
    command += ", "
    command += str(speed)
    command += ", "
    command += str(time*1000)
    command += ")\n"
    list_name += [command]
        
def pause(time, list_name=commands, file_name="stuCodeBayS2.py"):
    command = ""
    string = "pause(" + str(time)
    if spaces(string, file_name) != 0:
        for i in range(spaces(string, file_name)//2):
            command += " "
    command += "MotorSet(0, 0, "
    command += str(time*1000)
    command += ")\n"
    list_name += [command]

def obstacle(list_name=commands):
    command = "ReadObstacle\n"
    list_name += [command]
    command2 = "if (LeftObstacle == 1 and RightObstacle == 1)\n"
    list_name += [command2]
    return True

def end_program(list_name=commands):
    S2tbSend_To_S2(list_name)

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
