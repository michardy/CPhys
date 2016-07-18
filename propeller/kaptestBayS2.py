from bayS2 import move
from bayS2 import get_line_number
from bayS2 import spaces
from bayS2 import pause
from bayS2 import obstacle
from bayS2 import end_program
from bayS2 import commands

move(128.00, 5, commands, "kaptestingBays2")
pause(5, commands, "kaptestingBays2")
move(-128.00, 5, commands, "kaptestingBays2")
move(128.00, 5, commands, "kaptestingBays2")
end_program()

