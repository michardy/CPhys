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
    spinfile = "move_s2mms.spin"
    ctype_spinfile = ctypes.c_char_p(spinfile)
    ms2 = open(spinfile,"w")
    ms2.write("CON\n\n")
    ms2.write("_clkmode      = xtal1 + pll16x\n")
    ms2.write("_xinfreq      = 5_000_000\n\n")
    ms2.write("OBJ\n\n")
    ms2.write('  s2mms : "s2mms"\n')
    ms2.write('  s2 : "s2"\n\n')
    ms2.write('PUB start\n')
    ms2.write('  s2mms.start_motors\n')
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

def move(speed, time, list_name=commands): #move adds an item to list_name
    command = "s2mms.move_timed_mms("
    command += str(speed)
    command += ",0.00,"
    command += str(time)
    command += ")\n"
    list_name += [command]

def pause(time, list_name=commands): #time is in tenths of a second
    command = "s2.delay_tenths("
    command += str(time)
    command += ")\n"
    list_name += [command]

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
