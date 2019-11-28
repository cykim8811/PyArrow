

import code
import threading
import time
import typing
from itertools import product
from math import *

import pygame

# Initialize Pygame
pygame.init()
size = [960, 720]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("PyArrow")
font_d = pygame.font.SysFont("comicsansms", 24)
# Define variables
bg_color = (64, 68, 74)
fps = 100
speed = 2
unit = 48
ret_seed = 0
ret_queue = []
G, T = 0, 1

# Interactive Shell in Thread
def start_interact(loc):
    threading.Thread(target=code.interact, args=(None, None, loc)).start()

def start_pygame(loc):
    threading.Thread(target=t_pygame).start()

def outp(v1,v2):
    v1=v1.pos
    v2=v2.pos
    return (v1[0]*v2[1]-v1[1]*v2[0])

class vec():
    def __init__(self, *args):
        if len(args) == 1:
            self.pos = args[0]
        else:
            self.pos = args
    def l(self):
        return sqrt(sum([x ** 2 for x in self.pos]))
    def __mul__(self, other):
        if type(other) in [int, float]:
            return vec([x * other for x in self.pos])
        elif type(other) is vec:
            return sum([self.pos[i] * other.pos[i] for i in range(len(self.pos))])
    def __add__(self, other):
        return vec([self.pos[i] + other.pos[i] for i in range(len(self.pos))])
    def __sub__(self, other):
        return vec([self.pos[i] - other.pos[i] for i in range(len(self.pos))])
    def __neg__(self):
        return vec([-x for x in self.pos])
    def angle(self):
        return atan2(self.pos[1], self.pos[0])

# =======================================
# Program Code
# =======================================

# Define classes
class o_arrow():
    def __init__(self, v=vec(5, 8)):
        self.pos = v
        self.dir = 0

        self._fade = 0
        self.state = -1
        self.phase = 0
        self.spr_u = [(0.3, 0.0), (-0.3, 0.3), (-0.1, 0.0)]
        self.spr_d = [(0.3, 0.0), (-0.3, -0.3), (-0.1, 0.0)]
        self.spr_b = [(-0.1, 0.0), (-0.3, -0.3), (-0.2, 0.0), (-0.3, 0.3)]
    def move(self, x, t, seed):
        t = floor(t * fps / speed)
        initial = self.pos
        for k in [(pi / (2 * t)) * cos((pi / 2) * i / t) for i in range(t)]:
            self.pos = self.pos + latovec(k * x.l(), self.dir + x.angle())
            yield None
        self.pos = initial + latovec(x.l(), self.dir + x.angle())
        if not any([(tl.pos - self.pos).l() < 0.1 for tl in tiles]):
            global routines
            routines = [routines[0], self.fade(-1)]
        yield (seed, 0)
    def turn(self, x, t, seed):
        t = floor(t * fps / speed)
        initial = self.dir
        for k in [(pi / (2 * t)) * cos((pi / 2) * i / t) for i in range(t)]:
            self.dir = self.dir + k * x
            yield None
        self.dir = initial + x
        yield (seed, 0)
    def get(self, x, seed):
        x = latovec(vec(x).l(), atan2(x[1], x[0]) + self.dir)
        ctl = [tl for tl in tiles if (tl.pos - self.pos - x).l() < 0.1]
        if len(ctl) > 0:
            ctl = ctl[0]
            yield (seed, ctl.c)
        else:
            yield (seed, False)
    def paint(self, x, col, seed):
        x = latovec(x.l(), atan2(x.pos[1], x.pos[0]) + self.dir)
        tar = [p for p in tiles if (p.pos - self.pos - x).l() < 0.1]
        if len(tar) > 0:
            tar = tar[0]
        else:
            print("No tile at:",x.pos)
        t = floor(fps * 0.3 / speed)
        initial = tar.c
        for i in range(t):
            tar.c = tuple([initial[w] * (1 - sin((pi / 2) * i / t)) + col[w] * sin((pi / 2) * i / t) for w in range(3)])
            yield None
        tar.c = col
        yield (seed, 0)
    def fade(self, seed):
        t = fps / speed
        for _ in range(floor(t / 2)):
            self._fade += 2 / fps
            yield None
        while True:
            yield None

class tile():
    def __init__(self, v: vec, c=(255, 255, 255)):
        self.pos = v
        self.c = c
    def draw(self):
        x, y = self.pos.pos
        pygame.draw.rect(screen, self.c, [(x + 0.05) * unit, (y + 0.05) * unit, unit * 0.9, unit * 0.9])

# Define variables
tiles: typing.List[tile] = [tile(vec(x, y)) for x, y in
                            product(range(2, floor(size[0] / unit) - 2), range(2, floor(size[1] / unit) - 2))]
routines = []

# Define functions
maplist = [
    '3,7/999999999990000099999999999999909990999999999990009090000099999999909090909090999999999000000000909999990009909090999099999909099090000000999990000990999099999999990999909990000299990000999099999999999909009990999999999999099999909999999999990000000099999999999999999999999999999999999999999999999999',
    '2,2/99999999999999999999999999999999999999999900090000000090909999990999099090900099990900000900099090999900099909090009909999099909000999090099990909000900090009999900099909999909009999090009090900099099990909990009090900999909990909990909999999000900000009000299999999999999999999999999999999999999999999999',
    '2,7/9999999999999999999999999999999999999999999000000000000002999990000000000090029999900000009000009299999000009000090002999990009000090090029999000900009000000299999000090000900902999990000009000090029999900000000900000299999000000000000902999990000000000000029999999999999999999999999999999999999999999999',
    '2,2/9999999999999999999999999999999999999999990009009000009090999999090900909090009999090000099099909099990009990900009990999909990900099009009999090900090009000999990009990999990900999909009000090009909999090900999909090099990999090009090999999900090009000900029999999999999999999999999999999999999999999999'
]

def setting(p=None):
    w, h = floor(size[0] / unit), floor(size[1] / unit)
    global tiles, arrow
    if p == None:
        t = [str(arrow[0].pos.pos[0]), ",", str(arrow[0].pos.pos[1]), "/"] + ["9"] * (w * h)
        for tl in tiles:
            t[tl.pos.pos[0] + tl.pos.pos[1] * w] = str(col_l.index(tl.c))
        return "".join(t)
    else:
        k = p.split("/")
        t=k[0]
        arrow[0].pos= (vec(int(t.split(",")[0]), int(t.split(",")[1])))
        tiles = [tile(vec(i % w, i // w), col_l[int(t)]) for i, t in enumerate(k[-1]) if t != "9"]
        return tiles

def set_speed(spd):
    global speed
    speed = spd

def draw_arrow(arw: o_arrow):
    pos = tocoord(arw.pos + vec(0.5, 0.5))
    pl = [tocoord(vec(p, q)) for p, q in arw.spr_b]
    pl = [(latovec(t.l(), t.angle() + arw.dir) + pos).pos for t in pl]
    c = (vec(64, 68, 70) * arw._fade + vec(48, 48, 48) * (1 - arw._fade)).pos
    c = (max(0, c[0]), max(0, c[1]), max(0, c[2]))
    pygame.draw.polygon(screen, c, pl)
    pl = [tocoord(vec(p, q)) for p, q in arw.spr_u]
    pl = [(latovec(t.l(), t.angle() + arw.dir) + pos).pos for t in pl]
    c = (vec(64, 68, 70) * arw._fade + vec(96, 96, 96) * (1 - arw._fade)).pos
    c = (max(0, c[0]), max(0, c[1]), max(0, c[2]))
    pygame.draw.polygon(screen, c, pl)
    pl = [tocoord(vec(p, q)) for p, q in arw.spr_d]
    pl = [(latovec(t.l(), t.angle() + arw.dir) + pos).pos for t in pl]
    c = (vec(64, 68, 70) * arw._fade + vec(128, 128, 128) * (1 - arw._fade)).pos
    c = (max(0, c[0]), max(0, c[1]), max(0, c[2]))
    pygame.draw.polygon(screen, c, pl)

def latovec(l, a):
    return vec(cos(a), sin(a)) * l

def tocoord(v):
    return v * unit

def draw_text(v, t, s=24, c=(255, 255, 255)):
    if s == 24:
        font = font_d
    else:
        font = pygame.font.SysFont("comicsansms", s)
    text = font.render(t, True, c)
    screen.blit(text, tocoord(v).pos)

def draw_rect(x, y, c=(255, 255, 255)):
    pygame.draw.rect(screen, c, tocoord(vec(x, y) + vec(0.1, 0.1)).pos + tocoord(vec(0.8, 0.8)).pos)

def onTick():
    global routines
    while len(routines) > 0:
        ret = next(routines[0])
        if ret != None:
            ret_queue.append(ret)
            routines.pop(0)
        else:
            break
    for tl in tiles:
        tl.draw()
    for arw in arrow:
        if not type(arw) is o_arrow: print(arw)
        draw_arrow(arw)

# Definition for Interpreter

front, back, left, right, here = (1, 0), (-1, 0), (0, -1), (0, 1), (0, 0)
white, black, green, yellow, red, blue = \
    (255, 255, 255), (31, 31, 31), (32, 224, 32), \
    (234, 234, 32), (212, 32, 32), (32, 32, 255)
col_l = [white, black, green, yellow, red, blue]

def go(x=front):
    global ret_seed
    seed = ret_seed
    ret_seed += 1
    routines.append(arrow[0].move(vec(x), 0.5, seed))
    while not any((t[0] == seed for t in ret_queue)):
        time.sleep(0.01)
    for t in ret_queue:
        if t[0] == seed:
            return

def turn(x=right):
    global ret_seed
    seed = ret_seed
    ret_seed += 1
    if x in [right, left]:
        x = x[1] * pi / 2
    routines.append(arrow[0].turn(x, 0.5, seed))
    while not any((t[0] == seed for t in ret_queue)):
        time.sleep(0.1)
    for t in ret_queue:
        if t[0] == seed:
            return

def get(x=here):
    global ret_seed
    seed = ret_seed
    ret_seed += 1
    routines.append(arrow[0].get(x, seed))
    while not any((t[0] == seed for t in ret_queue)):
        time.sleep(0.1)
    for t in ret_queue:
        if t[0] == seed:
            return t[1]

def paint( col=green,x=here):
    global ret_seed
    seed = ret_seed
    ret_seed += 1
    routines.append(arrow[0].paint(vec(x), col, seed))
    while not any((t[0] == seed for t in ret_queue)):
        time.sleep(0.01)
    for t in ret_queue:
        if t[0] == seed:
            return

# =======================================
# Run Program
# =======================================
arrow = [o_arrow()]

def t_pygame():
    done = False
    clock = pygame.time.Clock()
    while not done:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ctl = [tl for tl in tiles if
                       (tl.pos - vec(pygame.mouse.get_pos()) * (1 / unit) + vec(0.5, 0.5)).l() < 0.5]
                if len(ctl) > 0:
                    if event.button == pygame.BUTTON_RIGHT:
                        tiles.remove(ctl[0])
                elif event.button == pygame.BUTTON_LEFT:
                    pp = (vec(pygame.mouse.get_pos()) * (1 / unit)).pos
                    tiles.append(tile(vec(floor(pp[0]), floor(pp[1]))))
        screen.fill(bg_color)
        onTick()
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    start_interact(globals())
    t_pygame()
else:
    start_pygame(globals())


