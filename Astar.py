from pyarrow import *

tiles = setting(maplist[1])

def fetch(*args):
    v = vec(args)
    target = [tl for tl in tiles if (tl.pos - v).l() < 0.1]
    if len(target) == 0:
        return False
    elif len(target) > 1:
        print("Duplicated at:", target[0].pos.pos)
        quit()
    else:
        return node(target[0])

class node():
    def __init__(self, tile, prev=None):
        self.tile = tile
        self.F = 0
        self.path = prev
    def pos(self):
        return self.tile.pos
    def getPrev(self, t):
        if self.path == None:
            return []
        return self.path.getPrev(t) + [self.tile]

#arrow[0].pos.pos=(2,2)
#fetch(17,12).tile.c=green

open_list = [fetch(arrow[0].pos.pos[0],arrow[0].pos.pos[1])]
closed_list = []
destpos=[t.pos.pos for t in tiles if t.c==green][0]
while not destpos in [t.pos().pos for t in open_list]:
    time.sleep(0.01)
    open_list.sort(key=lambda x: x.F + (x.pos() - vec(17, 12)).l()*1.2)
    c = open_list[0]
    print("curpoint", c.pos().pos)
    print("openlist", [t.pos().pos for t in open_list])
    print("closelist", [t.pos().pos for t in closed_list])
    closed_list.append(open_list.pop(0))
    closed_list[-1].tile.c = (96, 96, 255)
    for x, y in [front, back, right, left]:
        if (x + c.pos().pos[0], y + c.pos().pos[1]) in [t.pos().pos for t in closed_list]:
            continue
        if (x + c.pos().pos[0], y + c.pos().pos[1]) in [t.pos().pos for t in open_list]:
            n = [t for t in open_list if t.pos().pos == (x + c.pos().pos[0], y + c.pos().pos[1])][0]
            if n.F > c.F + sqrt(x ** 2 + y ** 2):
                n.F = c.F + sqrt(x ** 2 + y ** 2)
                n.path = c
        else:
            f = fetch(x + c.pos().pos[0], y + c.pos().pos[1])
            if f:
                f.path = c
                f.F = c.F + sqrt(x ** 2 + y ** 2)
                open_list.append(f)
                if f.tile.pos.pos == destpos: continue
                f.tile.c = (192, 192, 255)
print([t for t in open_list if t.pos().pos == destpos][0].F)
l = [t for t in open_list if t.pos().pos == destpos][0].getPrev([])
l.reverse()
for k in l[1:]:
    k.c = yellow
    time.sleep(0.01)
l.reverse()
for k in l:
    init = k.pos
    dest = arrow[0].pos
    w = outp((dest - init), latovec(1, arrow[0].dir))
    if abs(w) > 0.1:
        if w > 0:
            turn(right)
        else:
            turn(left)
    go()
