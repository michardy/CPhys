#Test file opens test.pys, parses it, assembles it and sends it to the robot
#This is a demo of what the windowed application would do
from S2mms import spin

program = spin()

with open("test.pys", "r") as f:
    pdata = f.read()

program.run(pdata)
