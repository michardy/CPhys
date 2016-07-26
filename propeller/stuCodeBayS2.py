from bayS2 import move
from bayS2 import get_line_number
from bayS2 import spaces
from bayS2 import pause
from bayS2 import obstacle
from bayS2 import end_program
from bayS2 import commands

move(128, 5, commands, "stuCodeBayS2.py")
if obstacle():
    move(-128, 5, commands, "stuCodeBayS2.py")
move(128, 3, commands, "stuCodeBayS2.py")
end_program()
