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
from __future__ import division, print_function
#from visual import *
#from visual.filedialog import get_file, save_file
#import wx
import os
import sys
import ctypes
#import pickle
#import copy as cpm
          

def S2tbSend_To_S2():
    commands = ["s2.move_timed_mms(10.00,0.00,1.00)"]
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

    ms2.close()
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    prop = ctypes.cdll.LoadLibrary(path + "\Propellent.dll")
    prop.InitPropellent(None)
    libdir = ctypes.c_char_p(os.path.realpath(path))
    prop.SetLibraryPath(libdir)
    prop.CompileSource(ctype_spinfile,True)
    prop.DownloadToPropeller(0,1)  #store in RAM and run
    prop.FinalizePropellent
 
S2tbSend_To_S2()
    

