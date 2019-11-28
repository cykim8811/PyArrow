from pyarrow import *

setting(maplist[1])
set_speed(6)

while not get()==green:
    if get(right):
        turn(right)
        go(front)
    elif get(front):
        go(front)
    else:
        turn(left)