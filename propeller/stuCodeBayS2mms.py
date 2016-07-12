# Program the Scribbler II robot by writing a little Python code!
# Developed at The Bay School of San Francisco, Summer 2016
# Thanks to:
#   Matt Greenwolfe, Cary Academy, NC
#   Katie Partington '17
#   and drP.
#
#############################################################
# If you want your program to work, don't change this part! #
#                                                           #
from bayS2mms import move                                   #
from bayS2mms import end_program                            #
from bayS2mms import commands                               #
#                                                           #
#############################################################
#
#  Ok: so suppose you want the robot move at a speed v for a time
#  interval Dt. Then, in the space below, just type the following:
#
#         move(v, Dt)
#
#  Negative values for v will move the robot backwards at speed -v.
#  Note you can include any number of these move statements, each
#  on its own line, as well as any other Python code.

move(8.00, 2.00)
move(-4.00, 4.00)
move(8.00, 2.00)
move(-4.00, 4.00)

#
#############################################################
# If you want your program to work, don't change this part! #
#                                                           #
end_program()                                               #
#                                                           #
#############################################################
