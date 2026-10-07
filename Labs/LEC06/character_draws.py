import math
from pico2d import *

open_canvas(800, 600)
character = load_image('character.png')

FRAME_DELAY = 0.001

A = (100, 100)
B = (700, 100)
C = (400, 500)

LEFT, RIGHT = 50, 750
BOTTOM, TOP = 50, 550

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    delay(FRAME_DELAY)

def move_circle():
    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)
        draw_character(x, y)

def move_top():
    for x in range(LEFT, RIGHT + 1, 5):
        draw_character(x, TOP)

def move_right():
    for y in range(TOP - 5, BOTTOM - 1, -5):
        draw_character(RIGHT, y)

def move_bottom():
    for x in range(RIGHT - 5, LEFT - 1, -5):
        draw_character(x, BOTTOM)

def move_left():
    for y in range(BOTTOM + 5, TOP + 1, 5):
        draw_character(LEFT, y)

def move_rectangle():
    move_top()
    move_right()
    move_bottom()
    move_left()

def move_line(x0, y0, x1, y1, steps=100):
    for step in range(1, steps + 1):
        t = step / steps
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        draw_character(x, y)

def move_ab():
    move_line(*A, *B)

def move_bc():
    move_line(*B, *C)

def move_ca():
    move_line(*C, *A)

def move_triangle():
    draw_character(*A)
    move_ab()
    move_bc()
    move_ca()

def run_once():
    move_circle()
    move_rectangle()
    move_triangle()

try:
    while True:
        run_once()
except KeyboardInterrupt:
    pass
finally:
    close_canvas()
