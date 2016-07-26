# Program the Scribbler II robot by writing a little Python code!
# Developed at The Bay School of San Francisco, Summer 2016
# Thanks to:
#   Matt Greenwolfe, Cary Academy, Cary, NC
#   Katie Partington '17 The Bay School of San Francisco
#   and drP.
#
#############################################################
# If you want your program to work, don't change this part! #
#                                                           #
from mihbayS2mms import speed_up_to                         #
from mihbayS2mms import cruise_at                           #
from mihbayS2mms import stop_from                           #
from mihbayS2mms import pause_for                           #
from mihbayS2mms import run_program                         #
from mihbayS2mms import commands                            #
from mihbayS2mms import spin                                #
                                                            #
program = spin()                                            #
#                                                           #
#############################################################
## To control your robot, you will be sending it a list of  #
## commands.  You can do that by editing (and then running) #
## this nifty Python program.  Make sure the robot's power  #
## switch is in the on ("|") position and its cable is      #
## connected to a USB port of this computer.                #
##                                                          #
## To include a command in your list, you need to type it   #
## into the space below all this text.                      #
##                                                          #
## Initially, the robot is stationary.  So that it doesn't  #
## take off while you are still pushing the blue button,    #
## it's a good idea to enter:                               #
##    pause_for(Dt)                                         #
## where Dt is the number of seconds you want to elapse     #
## before the robot starts to move, after you push the blue #
## button                                                   #
## First, we have to tell the robot to speed up. To do that #
## just enter:                                              #
##    speed_up_to(v, Dt)                                    #
## where v is the speed you want to reach and Dt is the     #
## number of seconds you want the robot to take to reach    #
## that speed.                                              #
##                                                          #
## To tell the robot to cruise at constant speed, enter:    #
##    cruise_at(v, Dt)                                      #
## where v is the cruising speed and Dt is the number of    #
## seconds you want the robot to cruise for.                #
##                                                          #
## To get the robot to come to a gentle stop, enter:        #
##    stop_from(v, Dt)                                      #
## where v is the speed before the robot begins to slow     #
## down and Dt is the amount of time you want the robot to  #
## take to come to a stop.                                  #
##                                                          #
## If you want the robot to move backwards (or it is moving #
## backwards and you want it to come to a stop), just put a #
## negative sign in from of every value v.                  #
##                                                          #
#############################################################

speed_up_to(6.00, 2.00)
cruise_at(6.00, 6.00)
stop_from(6.00, 2.00)
pause_for(1.00)
speed_up_to(-6.00, 2.00)
cruise_at(-6.00, 6.00)
stop_from(-6.00, 2.00)
pause_for(1.00)


#############################################################
# If you want your program to work, don't change this part! #
#                                                           #
run_program(program)                                        #
#                                                           #
#############################################################
