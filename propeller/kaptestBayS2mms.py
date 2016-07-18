from bayS2mms import move
from bayS2mms import end_program
from bayS2mms import commands
from bayS2mms import get_line_number
from bayS2mms import spaces
from bayS2mms import obstacle

move(6.00, 4.00, commands, "kaptesting")
if obstacle():
    move(-6.00, 2.00, commands, "kaptesting")
move(6.00, 3.00, commands, "kaptesting")

end_program()

