##:::::::[ python module for Scribbler 2mms ]::::::::::::::::::::::::::::::::: 
##File:  drpBayS2mms.py
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
##This python module contains functions needed
##to program straight line motion of the scribbler 2
##robot.

##dependencies:
##      Python and Visual Module:  see www.vpython.org for installation instructions
##      Parallax propellent dynamic link library:  http://www.parallax.com/PropellerDownloads
##      Propeller Floatmath.spin library 
##      wxpython (included with the latest versions of vpython)
##      s2mms motor driver 
##          Place s2mms.spin, propellent.dll, and FloatMath.spin in a folder called propeller
##          Place all three folders in the same folder as this file.


##=======[ Introduction ]=========================================================

##s2mms.spin provides low-level motor drivers and higher level spin routines
##that move the S2 Robot based on step function velocity and acceleration
##profiles.  Accuracy is close to 1mm/s or 1mm/s^2.
##
##This Python module provides the functions needed to specify a series of
##motions, write a spin program, and send that program to the robot.
##::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#from __future__ import division, print_function
#from visual import *
#from visual.filedialog import get_file, save_file
#import wx
import os
import sys
import ctypes
#import pickle
#import copy as cpm
          

def S2tbSend_To_S2(commands):
    #EEPROM = wx.GetKeyState(wx.WXK_CONTROL)
    #commands = ["s2.move_timed_mms(6.00,0.00,6.00)"]
    
    spinfile = "move_s2mms.spin"

    ctype_spinfile = ctypes.c_char_p(spinfile)

    ms2 = open(spinfile,"w")

    ms2.write("CON\n\n")
    ms2.write("_clkmode      = xtal1 + pll16x\n")
    ms2.write("_xinfreq      = 5_000_000\n\n")
    ms2.write("OBJ\n\n")
    ms2.write('  s2 : "s2mms"\n\n')
    ms2.write('PUB start\n')
    ms2.write('  s2.start_motors\n')
    ms2.write('  repeat\n')
    ms2.write('    waitcnt(clkfreq + cnt)\n')
    ms2.write('    waitpne(|< s2#BUTTON, |< s2#BUTTON,0)\n')
    indent = '    '

    for command in commands:         
        ms2.write(indent + command)
    ms2.close()  # This *.spin file does work when sent to the S2 using Propeller Tool

##    os.system("./bstc.osx -p0 -L ./propeller " + spinfile)        

##    print(os.getcwd())
##
##    prop = ctypes.cdll.LoadLibrary("Propellent.dll")
##    prop.InitPropellent(ctypes.c_long('2f00000'),True,"") 
##    libdir = ctypes.c_char_p()
##    prop.SetLibraryPath(libdir)
##    prop.CompileSource(ctype_spinfile,True)
##    prop.DownloadToPropeller(0,1)  #store in RAM and run
##    prop.FinalizePropellent

    path = os.path.abspath(os.path.dirname(sys.argv[0])) #points to correct directory
                                                             #even if load or save as changed
                                                             #the current working directory
    prop = ctypes.cdll.LoadLibrary(path + "\Propellent.dll")
    prop.InitPropellent(None)
    libdir = ctypes.c_char_p(os.path.realpath(path))
    prop.SetLibraryPath(libdir)
    prop.CompileSource(ctype_spinfile,True)
    #if (EEPROM):
        #prop.DownloadToPropeller(0,3) #store in EEPROM and run
    #else:
    prop.DownloadToPropeller(0,3)  #store in RAM and run
    prop.FinalizePropellent
 
#S2tbSend_To_S2()
    
commands = []

def forward(speed, acceleration, time, list_name=commands): #forward adds an item to list_name
    command = "s2.move_timed_mms("
    command += str(speed)
    command += ","
    command += str(acceleration)
    command += ","
    command += str(time)
    command += ")\n"
    list_name += [command]

def end_program(list_name=commands):
    S2tbSend_To_S2(list_name)

#listx = []
#forward(6.00, 0.00, 2.00, listx)
#end_program(listx)
